import configparser
import JsonParser
import os


class CfgParser:
    def __init__(self):
        self.parser = configparser.ConfigParser()
        self.conf = os.path.abspath(os.path.join(os.path.split(os.path.realpath(__file__))[0], "../conf/dbMon.conf"))
        self.parser.read(self.conf, encoding='UTF8')

    def get_mon_list(self, hostname):
        if self.parser.get(hostname, 'monlst') != "all":
            return self.parser.get(hostname, 'monlst').split(',')
        else:
            return JsonParser.JSONParser(hostname).get_all_mon()
    
    def get_skip_list(self, hostname):
        return self.parser.get(hostname, 'skiplst').split(',')

    def get_dsn(self, hostname):
        return self.parser.get(hostname, 'dsn')

    def get_ssh_ip(self, hostname):
        return str(self.parser.get(hostname, 'ssh_ip'))

    def get_ssh_port(self, hostname):
        return str(self.parser.get(hostname, 'ssh_port'))

    def get_username(self, hostname):
        return self.parser.get(hostname, 'username')

    def get_password(self, hostname):
        return self.parser.get(hostname, 'password')

    def get_hosts(self):
        return self.parser.sections()

    def get_time_out(self, hostname):
        return int(self.parser.get(hostname, 'timeout'))

    def get_srv_lst(self, hostname):
        return (self.parser.get(hostname, 'prometheus_lst')).split(',')

    def get_maxconn(self, hostname):
        return int(self.parser.get(hostname, 'maxconn'))

    def get_porfile(self, hostname):
        return self.parser.get(hostname, 'profile')

    def get_es_url(self, hostname):
        return self.parser.get(hostname, 'es_url')

    def get_es_retention(self, hostname):
        return self.parser.get(hostname, 'es_retention')

    def get_srv_dir(self, hostname):
        return self.parser.get(hostname, 'ifxsrvdir')

    def get_cli_dir(self, hostname):
        return self.parser.get(hostname, 'ifxclidir')

    def get_local_ip(self, hostname):
        return self.parser.get(hostname, 'local_ip')

if __name__ == "__main__":
    cfg = CfgParser()
    print(type(cfg))
