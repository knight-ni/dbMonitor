import json

import CfgParser
import os


class JSONParser:
    def __init__(self, hostname):
        self.hostname = hostname
        self.cfg = CfgParser.CfgParser()
        self.susp = os.path.abspath(os.path.join(os.path.split(os.path.realpath(__file__))[0], "../conf/suspects.json"))

    def get_mon_list(self):
        # cfg = CfgParser.CfgParser(hostname)
        mon_list = self.cfg.get_mon_list(self.hostname)
        return mon_list
   
    def get_skip_list(self):
        skip_list = self.cfg.get_skip_list(self.hostname)
        return skip_list

    def get_json_obj(self, name):
        with open(self.susp, 'r') as load_f:
            load_dict = json.load(load_f)
        for jn in load_dict:
            if name in jn.values():
                return jn

    def get_all_mon(self):
        with open(self.susp, 'r') as load_f:
            load_dict = json.load(load_f)
            return [js.get('NAME') for js in load_dict if js]

    def get_top_mon(self):
        with open(self.susp, 'r') as load_f:
            load_dict = json.load(load_f)
            return [js for js in load_dict if js.get('API') == 'ifx_top']

    def get_cmd_mon(self):
        with open(self.susp, 'r') as load_f:
            load_dict = json.load(load_f)
            return [js for js in load_dict if js.get('API') == 'ifx_cmd']


if __name__ == "__main__":
    jn = JSONParser('jsvfpredbs').get_json_obj('top_ses')
    print(jn)
