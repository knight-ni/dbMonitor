# -*- coding: utf-8 -*-
import json
from file_parser import dbmon_jsonparser

def susexp(filename):
    js = dbmon_jsonparser.Json_Parser('GOODKNIGHT')
    j = js.get_all_obj()
    for obj in j:
        file = obj.get('NAME')
        with open("../indicators/"+file+".json","w") as f:
            json.dump(obj,f,indent=4)

if __name__ == "__main__":
    susexp('/home/dbmon/dbMonitor/conf/suspects.json')
