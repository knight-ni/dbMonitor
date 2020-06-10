import prometheus_client
from flask import Flask, request, render_template
from flask import Response
from retrying import retry
import socket
import time
import CfgParser
import CollectData

work_host_list = []
app = Flask(__name__, static_folder='templates')
cfg = CfgParser.CfgParser()


#@retry(stop_max_attempt_number=5, wait_fixed=2000)
def run_col(hostname):
    try:
        reg = CollectData.CollectData(hostname).collect()
        return reg
    finally:
        try:
            work_host_list.remove(hostname)
        except Exception:
            pass


@app.route("/metrics/<hostname>", methods=['GET', 'POST'])
def main(hostname):
    ip = request.remote_addr
    addrs = [add[4][0] for add in socket.getaddrinfo(socket.gethostname(), None)]
    srvlst = cfg.get_srv_lst(hostname)
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
    data = ['<li><a href="' + base_url + 'metrics/' + hostname + '">' + base_url + 'metrics/' + hostname + '</a></li>'
            for hostname in CfgParser.CfgParser().get_hosts()]
    return Response('<ur>''<br>'.join(data) + '</ur>')


@app.errorhandler(500)
def handle_500():
    return "Internal Error"


@app.errorhandler(404)
def handle_404():
    return render_template("index.html")

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
