import pyodbc
from DBUtils.PooledDB import PooledDB
import CfgParser
import GloVal

GloVal.init()

class DBConnection:
    def __init__(self, hostname):
        self.hostname = hostname
        self.cfg = CfgParser.CfgParser()
        self.dsn = self.cfg.get_dsn(hostname)
        self.pwd = self.cfg.get_password(hostname)
        self.timetout = self.cfg.get_time_out(hostname)
        self.srvlst = self.cfg.get_srv_lst(hostname)
        self.maxconn = self.cfg.get_maxconn(hostname)
        pooldb = PooledDB(pyodbc, maxconnections=self.maxconn, mincached=self.maxconn, maxshared=self.maxconn,maxusage=None, setsession=[], ping=0, DSN=self.dsn, PWD=self.pwd, timeout=self.timetout)
        GloVal.set_value('pool', pooldb)

    def getconn(self):
        conn = GloVal.get_value('pool').connection()
        return conn

    def closeconn(self):
        res = GloVal.get_value('pool').close
        return res

'''''
    def getSSHConn(self):
        if (not gloval.get_value('ssh_conn')):
            ssh_ip = self.cfg.get_ssh_ip(self.hostname)
            ssh_port = self.cfg.get_ssh_port(self.hostname)
            username = self.cfg.get_username(self.hostname)
            password = self.cfg.get_password(self.hostname)
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(hostname=ssh_ip, port=ssh_port, username=username, password=password, timeout=300)
            gloval.set_value('ssh_conn', ssh)
        ssh_conn = gloval.get_value('ssh_conn')
        try:
            ssh_conn.exec_command('ls')
        except Exception as e:
            ssh_ip = self.cfg.get_ssh_ip(self.hostname)
            ssh_port = self.cfg.get_ssh_port(self.hostname)
            username = self.cfg.get_username(self.hostname)
            password = self.cfg.get_password(self.hostname)
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(hostname=ssh_ip, port=ssh_port, username=username, password=password, timeout=300)
            gloval.set_value('ssh_conn', ssh)
        return ssh_conn
'''''


if __name__ == "__main__":
    conn = DBConnection('jsvftestdbs')
    print(type(conn))
