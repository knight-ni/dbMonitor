import os
import json

class Json_Parser:

    def __init__(self, hostname):
        file_name = []
        self.load_dict = []
        self.hostname = hostname
        path = os.path.abspath(os.path.join(os.path.split(os.path.realpath(__file__))[0], "../../indicators"))
        for _,_,files in os.walk(path):
            for file in files:
                if file[-4:]=='json':
                    file_name.append(file)
        for name in file_name:
            with open(path + '/' + name,'r') as f:
                k = json.load(f)
            self.load_dict.append(k)

    def get_json_obj(self, name):
        for jn in self.load_dict:
            if name in jn.values():
                return jn

    def get_all_mon(self):
        return [js.get('NAME') for js in self.load_dict if js]

    def get_top_mon(self):
        return [js.get('NAME') for js in self.load_dict if js.get('API') == 'ifx_top']

    def get_cmd_mon(self):
        return [js.get('NAME') for js in self.load_dict if js.get('API') == 'ifx_cmd']

    def get_smi_mon(self):
        return [js.get('NAME') for js in self.load_dict if js.get('API') == 'ifx_smi']

    def get_onstat_mon(self):
        return [js.get('NAME') for js in self.load_dict if js.get('API') == 'ifx_onstat']

    def get_all_obj(self):
        return self.load_dict

if __name__ == "__main__":
    jn = Json_Parser('jsvfpredbs').get_all_obj()
    print(jn)
