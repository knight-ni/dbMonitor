# -*- coding:UTF-8 -*-
from file_parser import dbmon_cfgparser
import os
import subprocess
import sys


class Cmd_Runner:

    def __init__(self, hostname):
        self.cfg = dbmon_cfgparser.Cfg_Parser(hostname)
        self.new_env = os.environ.copy()
        self.new_env['INFORMIXDIR'] = self.cfg.get_srv_dir()
        self.new_env['PATH'] += os.pathsep + self.cfg.get_srv_dir() + '/bin'

    def runcmd(self, cmd, outtype):
        data = {}
        p = subprocess.Popen([cmd], env=self.new_env, stdout=subprocess.PIPE, stdin=subprocess.PIPE, shell=True)
        stdout, stderr = p.communicate()
        if outtype == 'gauge':
            try:
                data = {row.split(':')[0]: [int(row.split(':')[1])] for row in bytes.decode(stdout).split('\n') if row}
            except:
                print('error',file=sys.stderr)
                print(cmd,file=sys.stderr)
                print(stdout,file=sys.stderr)
                print(stderr,file=sys.dtderr)
        elif outtype == 'info':
            data = {row.split(':')[0]: [' '.join(row.split(':')[1:])] for row in bytes.decode(stdout).split('\n') if row}
        return data


if __name__ == "__main__":
    res = Cmd_Runner('jsvfpredbs').runcmd('onstat -version|grep -v onstat|sed -e \'s/\t\t*//g\' -e \'s/Build /Build_/g\' -e \'s/GLS /GLS_/g\'', 'info')
    print(res)
