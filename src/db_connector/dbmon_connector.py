import pyodbc
from DBUtils.PooledDB import PooledDB
import os
from file_parser import dbmon_cfgparser


class DBConnection:

    global_dict = {}

    def __init__(self, hostname):
        self.cfg = dbmon_cfgparser.Cfg_Parser(hostname)
        self.dsn = self.cfg.get_dsn()
        self.pwd = self.cfg.get_password()
        self.timetout = self.cfg.get_time_out()
        self.srvlst = self.cfg.get_srv_lst()
        self.maxconn = self.cfg.get_maxconn()
        os.environ['ODBCINI'] = os.path.abspath(os.path.join(os.path.split(os.path.realpath(__file__))[0], "../../conf/odbc.ini"))
        pooldb = PooledDB(pyodbc, maxconnections=self.maxconn, mincached=self.maxconn, maxshared=self.maxconn, maxusage=None, setsession=[], ping=0, DSN=self.dsn, PWD=self.pwd, timeout=self.timetout)
        self.set_value('pool', pooldb)

    def getconn(self):
        conn = self.get_value('pool').connection()
        return conn

    def closeconn(self):
        res = self.get_value('pool').close
        return res

    def set_value(self, key, value):
        self.global_dict[key] = value

    def get_value(self, key, defvalue=None):
        try:
            return self.global_dict[key]
        except KeyError:
            return defvalue

if __name__ == "__main__":
    conn = DBConnection('jsvfpredbs')
    print(conn.dsn)
