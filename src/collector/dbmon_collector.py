import datetime
from prometheus_client import Counter, Gauge, Histogram, Info, Summary
from prometheus_client.core import CollectorRegistry
from cmd_runner import dbmon_cmdrunner
from sql_runner import dbmon_sqlrunner
from file_parser import dbmon_jsonparser
from file_parser import dbmon_cfgparser
import os
import copy
import sys
import elasticsearch
from elasticsearch import helpers


class Data_Collector:
    def __init__(self, dbconn, hostname):
        self.hostname = hostname
        self.cfg = dbmon_cfgparser.Cfg_Parser(self.hostname)
        self.js = dbmon_jsonparser.Json_Parser(self.hostname)
        self.hostname = hostname
        self.srunner = dbmon_sqlrunner.SQL_Runner(dbconn)
        self.crunner = dbmon_cmdrunner.Cmd_Runner(self.hostname)
        self.es = elasticsearch.Elasticsearch(self.cfg.get_es_url(), http_compress=True)
        self.local_ip = self.cfg.get_local_ip()

    def makelabels(self, lablst, ifx):
        tmplst = None
        if len(lablst) > 1:
            for labstr in lablst:
                print(ifx.get(labstr))
                if not tmplst:
                    tmplst = [val for val in ifx.get(labstr)]
                else:
                    tmplst = [[tmplst[idx], ifx.get(labstr)[idx]] for idx, val in enumerate(tmplst)]
        else:
            for labstr in lablst:
                tmplst = [[val] for val in ifx.get(labstr)]
        return tmplst

    @property
    def collect2promethus(self):
        starttime = datetime.datetime.now()
        registry = CollectorRegistry(auto_describe=False)
        is_alive = self.srunner.conn_is_alive()
        succ = Histogram('collect_succ', 'collect successful', ['hostname', 'metric'], registry=registry,
                         buckets=(0, 1))
        time = Gauge('collect_time', 'collect time', ['hostname', 'metric'], registry=registry)
        successful = 0
        ifx = None
        if not is_alive:
            endtime = datetime.datetime.now()
            elapsedtime = (endtime - starttime).seconds
            print("database server can not be connected.", file=sys.stderr)
        else:
            conntime = Gauge('conn_time', 'connect time', ['hostname', 'metric'], registry=registry)
            conntime.labels(self.hostname, 'connect time').set((datetime.datetime.now() - starttime).microseconds)
            mon_list = self.cfg.get_mon_list()
            if (mon_list == "all"):
                mon_list = self.js.get_smi_mon() + self.js.get_onstat_mon()
            else:
                mon_list = list(set(mon_list).intersection(set(self.js.get_smi_mon() + self.js.get_onstat_mon())))
            skip_list = self.cfg.get_skip_list()
            for mon in list(set(mon_list).difference(set(skip_list))):
                value_dict = {}
                api = self.js.get_json_obj(mon)['API']
                name = self.js.get_json_obj(mon)['NAME']
                cmd = self.js.get_json_obj(mon)['CMD']
                metrics = self.js.get_json_obj(mon)['METRICS']
                labels = self.js.get_json_obj(mon)['LABEL']
                metype = self.js.get_json_obj(mon)['TYPE']
                if api == "ifx_smi":
                    ifx = self.srunner.runsql(cmd)
                elif api == "ifx_onstat":
                    ifx = self.crunner.runcmd(cmd, metype)
                try:
                    if len(list(ifx.values())[0]) == 0:
                        continue
                except Exception:
                    continue
                if metrics == ['name', 'value']:
                    metrics = ifx.get('name')
                    values = [[value] for value in ifx.get('value')]
                    ifx = dict(zip(ifx.get('name'), values))
                elif metrics == ['key', 'value']:
                    metrics = ifx.keys()
                    values = ifx.values()
                    ifx = dict(zip(metrics, values))
                if labels.strip() != "":
                    lablst = labels.split(',')
                    labbld = copy.copy(lablst)
                    labbld.append('hostname')
                    labbld.append('metric')
                    tmplst = self.makelabels(lablst, ifx)
                    if metype == "gauge":
                        value_dict[name] = Gauge(name, '', labbld, registry=registry)
                        for idx, labval in enumerate(tmplst):
                            for metric in metrics:
                                tmp = [*labval, self.hostname, metric]
                                value_dict[name].labels(*tmp).set(ifx.get(metric)[idx])
                    elif metype == "counter":
                        value_dict[name] = Counter(name, '', lablst, registry=registry)
                        # tmplst = self.makelabels(lablst, ifx)
                        for idx, labval in enumerate(tmplst):
                            for metric in metrics:
                                tmp = [*labval, self.hostname, metric]
                                value_dict[name].labels(*tmp).set(ifx.get(metric)[idx])
                    elif metype == "info":
                        value_dict[name] = Info(name, '', lablst, registry=registry)
                        # tmplst = self.makelabels(lablst, ifx)
                        for idx, labval in enumerate(tmplst):
                            for metric in metrics:
                                tmp = [*labval, self.hostname, metric]
                                value_dict[name].labels(*tmp).info({name: ifx.get(metric)[idx]})
                    elif metype == "histogram":
                        value_dict[name] = Histogram(name, '', lablst, registry=registry)
                        # tmplst = self.makelabels(lablst, ifx)
                        for idx, labval in enumerate(tmplst):
                            for metric in metrics:
                                tmp = [*labval, self.hostname, metric]
                                value_dict[name].labels(*tmp).observe(ifx.get(metric)[idx])
                    elif metype == "summary":
                        value_dict[name] = Summary(name, '', lablst, registry=registry)
                        # tmplst = self.makelabels(lablst, ifx)
                        for idx, labval in enumerate(tmplst):
                            for metric in metrics:
                                tmp = [*labval, self.hostname, metric]
                                value_dict[name].labels(*tmp).observe(ifx.get(metric)[idx])
                else:
                    if metype == "gauge":
                        value_dict = {name: Gauge(name, '', ['hostname', 'metric'], registry=registry)}
                        for metric in metrics:
                            try:
                                value_dict[name].labels(self.hostname, metric).set(ifx.get(metric)[0])
                            except Exception:
                                print(name, file=sys.stderr)
                                print(metric, file=sys.stderr)
                                print(ifx.get(metric), file=sys.stderr)
                    elif metype == "counter":
                        value_dict = {name: Counter(name, '', ['hostname', 'metric'], registry=registry)}
                        for metric in metrics:
                            value_dict[name].labels(self.hostname, metric).inc(ifx.get(metric)[0])
                    elif metype == "info":
                        value_dict = {name: Info(name, '', ['hostname', 'metric'], registry=registry)}
                        for metric in metrics:
                            value_dict[name].labels(self.hostname, metric).info({metric: ifx.get(metric)[0].strip()})
                    elif metype == "histogram":
                        value_dict = {name: Histogram(name, '', ['hostname', 'metric'], registry=registry)}
                        for metric in metrics:
                            for kv in ifx.get(metric):
                                value_dict[name].labels(self.hostname, metric).observe(kv)
                    elif metype == "summary":
                        value_dict = {name: Summary(name, '', ['hostname', 'metric'], registry=registry)}
                        for metric in metrics:
                            for kv in ifx.get(metric):
                                value_dict[name].labels(self.hostname, metric).observe(kv)
            endtime = datetime.datetime.now()
            elapsedtime = (endtime - starttime).seconds
            successful = 1
        time.labels(self.hostname, 'collect time').set(elapsedtime)
        succ.labels(self.hostname, 'collect successful').observe(successful)
        return registry

    def collect2elastic(self):
        es_alive = self.es.ping()
        if not es_alive:
            print("elasticsearch server can not be connected.", file=sys.stderr)
        else:
            jsdata = []
            mon_list = self.cfg.get_mon_list()
            if (mon_list == "all"):
                mon_list = self.js.get_top_mon()
            else:
                mon_list = list(set(mon_list).intersection(set(self.js.get_top_mon())))
            skip_list = self.cfg.get_skip_list()
            for mon in list(set(mon_list).difference(set(skip_list))):
                api = self.js.get_json_obj(mon)['API']
                name = self.js.get_json_obj(mon)['NAME']
                cmd = self.js.get_json_obj(mon)['CMD']
                utc_datetime = datetime.datetime.utcnow()
                idxname = utc_datetime.strftime('%Y.%m.%d')
                mydict = self.srunner.runsql(cmd)
                for i in range(len(list(mydict.values())[0])):
                    tmp = {"@timestamp": datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.000+0800")}
                    for k, v in mydict.items():
                        if v[i]:
                            tmp[k] = v[i]
                    jsdata.append({"_index": name.lower() + '-' + self.local_ip + '-' + str(idxname),
                                   "_type": api.lower(), "_source": tmp})
            helpers.bulk(self.es, jsdata)
            script_file = os.path.join(os.path.split(os.path.realpath(__file__))[0],
                                       "../scripts/clean_es.sh >/dev/null 2>&1")
            cmd = "sh " + script_file
            return os.system(cmd)


if __name__ == "__main__":
    reg = Data_Collector('jsvfpredbs').collect2elastic()
    print(type(reg), file=sys.stderr)
