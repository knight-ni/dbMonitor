import QueryRunner
import JsonParser
import datetime
import elasticsearch
import CfgParser
from elasticsearch import helpers
import os


class TOPMonitor:
    def __init__(self, hostname):
        self.cfg = CfgParser.CfgParser()
        self.hostname = hostname
        self.query = QueryRunner.QryRunner(hostname)
        self.js = JsonParser.JSONParser(hostname)
        self.url = self.cfg.get_es_url(hostname)
        self.es = elasticsearch.Elasticsearch(self.url, http_compress=True)
        self.local_ip = self.cfg.get_local_ip(hostname)

    def getmon(self):
        jsdata = []
        jslst = self.js.get_top_mon()
        utc_datetime = datetime.datetime.utcnow()
        idxname = utc_datetime.strftime('%Y.%m.%d')
        for js in jslst:
            cmd = js['CMD']
            mydict = self.query.runsql(cmd)
            for i in range(len(list(mydict.values())[0])):
                tmp = {"@timestamp": datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.000+0800")}
                for k, v in mydict.items():
                    if v[i]:
                        tmp[k] = v[i]
                jsdata.append({"_index": js['NAME'].lower() + '-' + self.local_ip + '-' + str(idxname), "_type": js['API'].lower(), "_source": tmp})
        helpers.bulk(self.es, jsdata)
        cmd = "sh scripts/clean_es.sh >/dev/null 2>&1"
        return os.system(cmd)
 
    def ping(self):
        return self.es.ping()
  
    def conn_exit(self):
        self.query.conn_exit()


if __name__ == "__main__":
    mon = TOPMonitor('jsvfpredbs').ping()
    print(mon)
    # print(str(datetime.now().strftime('%Y%m%d-%H%M%S-0000-800')))
    # self.query.runSQL(self.hostname, cmd)
