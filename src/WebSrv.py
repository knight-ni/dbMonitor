import prometheus_client
from flask import Flask, request
from flask import Response
import socket
import time
from file_parser import dbmon_cfgparser
from collector import dbmon_collector
from db_connector import dbmon_connector


work_host_list = []
app = Flask(__name__, static_folder='templates')

def run_col(hostname):
    try:
        dbconn = dbmon_connector.DBConnection(hostname)
        col = dbmon_collector.Data_Collector(dbconn, hostname)
        col.collect2elastic()
        reg = col.collect2promethus
        return reg
    finally:
        try:
            work_host_list.remove(hostname)
            dbconn.closeconn()
        except Exception:
            pass


@app.route("/metrics/<hostname>", methods=['GET', 'POST'])
def main(hostname):
    ip = request.remote_addr
    addrs = [add[4][0] for add in socket.getaddrinfo(socket.gethostname(), None)]
    cfg = dbmon_cfgparser.Cfg_Parser(hostname)
    srvlst = cfg.get_srv_lst()
    srvlst += addrs
    try:
        if ip not in srvlst:
            return "Invalid Server Request from " + ip
        if hostname in work_host_list:
            time.sleep(10)
            if hostname in work_host_list:
                return "Collect Already Running,Please Wait For Complete"
            else:
                work_host_list.append(hostname)
                res = run_col(hostname)
        else:
            work_host_list.append(hostname)
            res = run_col(hostname)
        return Response(prometheus_client.generate_latest(res), mimetype="text/plain")
    finally:
        try:
            work_host_list.remove(hostname)
        except Exception:
            pass


@app.route("/", methods=['GET', 'POST'])
@app.route("/metrics", methods=['GET', 'POST'])
@app.route("/metrics/", methods=['GET', 'POST'])
def show_urls():
    base_url = request.url_root
    cfg = dbmon_cfgparser.Cfg_Parser('GoodKnight')
    data = ['<li><a href="' + base_url + 'metrics/' + hostname + '">' + base_url + 'metrics/' + hostname + '</a></li>'
            for hostname in cfg.get_hosts()]
    return Response('<ur>''<br>'.join(data) + '</ur>')


def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()

@app.route('/shutdown', methods=['POST'])
def shutdown():
    shutdown_server()
    return 'Server shutting down...'

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=False, threaded=True)
    # t = threading.Thread(target=collectData.collectData(hostname).collect())
    # t.start()
