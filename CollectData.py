import datetime
from prometheus_client import Counter, Gauge, Histogram, Info, Summary
from prometheus_client.core import CollectorRegistry
import CmdRunner
import JsonParser
import QueryRunner
import TopMonitor
import copy


class CollectData:
    def __init__(self, hostname):
        self.hostname = hostname

    def collect(self):
        srunner = QueryRunner.QryRunner(self.hostname)
        crunner = CmdRunner.CmdRunner(self.hostname)
        registry = CollectorRegistry(auto_describe=False)
        starttime = datetime.datetime.now()
        try:
            is_alive = srunner.conn_is_alive()
            succ = Histogram('collect_succ', 'collect successful', ['hostname', 'metric'], registry=registry, buckets=(0, 1))
            time = Gauge('collect_time', 'collect time', ['hostname', 'metric'], registry=registry)
            successful = 0
            if is_alive != 1:
                endtime = datetime.datetime.now()
                elapsedtime = (endtime - starttime).seconds
            else:
                conntime = Gauge('conn_time', 'connect time', ['hostname', 'metric'], registry=registry)
                conntime.labels(self.hostname, 'connect time').set((datetime.datetime.now() - starttime).microseconds)
                TopMonitor.TOPMonitor(self.hostname).getmon()
                parser = JsonParser.JSONParser(self.hostname)
                mon_list = parser.get_mon_list()
                for mon in mon_list:
                    value_dict = {}
                    api = parser.get_json_obj(mon)['API']
                    name = parser.get_json_obj(mon)['NAME']
                    cmd = parser.get_json_obj(mon)['CMD']
                    metrics = parser.get_json_obj(mon)['METRICS']
                    labels = parser.get_json_obj(mon)['LABEL']
                    metype = parser.get_json_obj(mon)['TYPE']
                    if api == "ifx_smi":
                        ifx = srunner.runsql(cmd)
                    elif api == "ifx_onstat":
                        ifx = crunner.runcmd(cmd, metype)
                    else:
                        continue
                    try:
                        if len(list(ifx.values())[0]) == 0:
                            continue
                    except:
                        continue
                    if metrics == ['name', 'value']:
                        metrics = ifx.get('name')
                        values = [[value] for value in ifx.get('value')]
                        ifx = dict(zip(ifx.get('name'), values))
                    elif metrics == ['key', 'value']:
                        metrics = ifx.keys()
                        values = ifx.values()
                        ifx = dict(zip(metrics, values))
################MODIFIED BY KNIGHT #####################################3
                    if labels != "":
                        lablst = labels.split(',')
                        lablst.append('hostname')
                        lablst.append('metric')
                        if metype == "gauge":
                            value_dict[name] = Gauge(name, '', lablst, registry=registry)
                            for labstr in labels.split(','):
                                for idx, labval in enumerate(ifx.get(labstr)):
                                    for metric in metrics:
                                        tmp = [labval, self.hostname, metric]
                                        value_dict[name].labels(*tmp).set(ifx.get(metric)[idx])

                        elif metype == "counter":
                            value_dict[name] = Counter(name, '', lablst, registry=registry)
                            for labstr in labels.split(','):
                                for idx, labval in enumerate(ifx.get(labstr)):
                                    for metric in metrics:
                                        tmp = [labval, self.hostname, metric]
                                        value_dict[name].labels(*tmp).inc(ifx.get(metric)[idx])

                        elif metype == "info":
                            value_dict[name] = Info(name, '', lablst, registry=registry)
                            for labstr in labels.split(','):
                                for idx, labval in enumerate(ifx.get(labstr)):
                                    for metric in metrics:
                                        tmp = [labval, self.hostname, metric]
                                        value_dict[name].labels(*tmp).info({name: ifx.get(metric)[idx]})

                        elif metype == "histogram":
                            value_dict[name] = Histogram(name, '', lablst, registry=registry)
                            for labstr in labels.split(','):
                                for idx, labval in enumerate(ifx.get(labstr)):
                                    for metric in metrics:
                                        tmp = [labval, self.hostname, metric]
                                        value_dict[name].labels(*tmp).observe(ifx.get(metric)[idx])

                        elif metype == "summary":
                            value_dict[name] = Summary(name, '', lablst, registry=registry)
                            for labstr in labels.split(','):
                                for idx, labval in enumerate(ifx.get(labstr)):
                                    for metric in metrics:
                                        tmp = [labval, self.hostname, metric]
                                        value_dict[name].labels(*tmp).observe(ifx.get(metric)[idx])

    ############################################################################
                    else:
                        if metype == "gauge":
                            value_dict = {name: Gauge(name, '', ['hostname', 'metric'], registry=registry)}
                            for metric in metrics:
                                try:
                                    value_dict[name].labels(self.hostname, metric).set(ifx.get(metric)[0])
                                except:
                                    print(name)
                                    print(metric)
                                    print(ifx.get(metric))
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
        finally:
            srunner.conn_exit()


if __name__ == "__main__":
    reg = CollectData('jsvfpredbs').collect()
    print(type(reg))
