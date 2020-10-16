import os
import configparser


class Cfg_Parser:

    def __init__(self, hostname):
        self.hostname = hostname
        self.parser = configparser.ConfigParser()
        self.conf = os.path.abspath(os.path.join(os.path.split(os.path.realpath(__file__))[0], "../../conf/dbMon.conf"))
        self.parser.read(self.conf, encoding='UTF8')

    def get_mon_list(self):
        if self.parser.get(self.hostname, 'monlst') != "all":
            return self.parser.get(self.hostname, 'monlst').split(',')
        else:
            return "all"

    def get_skip_list(self):
        return self.parser.get(self.hostname, 'skiplst').split(',')

    def get_dsn(self):
        return self.parser.get(self.hostname, 'dsn')

    def get_ssh_ip(self):
        return str(self.parser.get(self.hostname, 'ssh_ip'))

    def get_ssh_port(self):
        return str(self.parser.get(self.hostname, 'ssh_port'))

    def get_username(self):
        return self.parser.get(self.hostname, 'username')

    def get_password(self):
        return self.parser.get(self.hostname, 'password')

    def get_time_out(self):
        return int(self.parser.get(self.hostname, 'timeout'))

    def get_srv_lst(self):
        return (self.parser.get(self.hostname, 'prometheus_lst')).split(',')

    def get_maxconn(self):
        return int(self.parser.get(self.hostname, 'maxconn'))

    def get_porfile(self):
        return self.parser.get(self.hostname, 'profile')

    def get_es_url(self):
        return self.parser.get(self.hostname, 'es_url')

    def get_es_retention(self):
        return self.parser.get(self.hostname, 'es_retention')

    def get_srv_dir(self):
        return self.parser.get(self.hostname, 'ifxsrvdir')

    def get_cli_dir(self):
        return self.parser.get(self.hostname, 'ifxclidir')

    def get_local_ip(self):
        return self.parser.get(self.hostname, 'local_ip')


if __name__ == "__main__":
    cfg = Cfg_Parser()
    print(cfg.get_mon_list('jsvfpredbs'))
