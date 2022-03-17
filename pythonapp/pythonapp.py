from flask import Flask, Response
import time
import setup_prometheus
import prometheus_client
import requests

CONTENT_TYPE_LATEST = str('text/plain; version=0.0.4; charset=utf-8')


app = Flask(__name__)
setup_prometheus.setup_metrics(app)

@app.route('/503')
def func1():
    response=requests.get("https://httpstat.us/503")
    return {"sample_external_url_up":0,"sample_external_url_response_ms":response.elapsed.total_seconds()*1000}

@app.route('/200')
def func2():
    response=requests.get("https://httpstat.us/200")
    return {"sample_external_url_up":1,"sample_external_url_response_ms":response.elapsed.total_seconds()*1000}


@app.errorhandler(500)
def handle_500(error):
    return str(error), 500

@app.route('/metrics')
def metrics():
    return Response(prometheus_client.generate_latest(), mimetype=CONTENT_TYPE_LATEST)

if __name__ == '__main__':
     app.run(host='0.0.0.0',port=5000,debug=True,threaded=True)

