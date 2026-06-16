import time
import random
import logging
import json
from flask import Flask, Response, jsonify
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)

# ---- Logging setup (JSON format for Promtail) ----
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ---- Prometheus Metrics ----
REQUEST_COUNT = Counter(
    'http_requests_total',
    'Total HTTP Requests',
    ['method', 'endpoint', 'status']
)

REQUEST_LATENCY = Histogram(
    'http_request_duration_seconds',
    'HTTP Request Latency',
    ['endpoint']
)

# ---- Routes ----
@app.route('/')
def home():
    start = time.time()
    REQUEST_COUNT.labels(method='GET', endpoint='/', status='200').inc()
    REQUEST_LATENCY.labels(endpoint='/').observe(time.time() - start)
    logger.info(json.dumps({"endpoint": "/", "status": 200, "message": "home hit"}))
    return jsonify({"status": "ok", "message": "SRE Observability App Running"})

@app.route('/healthy')
def healthy():
    REQUEST_COUNT.labels(method='GET', endpoint='/healthy', status='200').inc()
    logger.info(json.dumps({"endpoint": "/healthy", "status": 200}))
    return jsonify({"status": "healthy"})

@app.route('/error')
def error():
    REQUEST_COUNT.labels(method='GET', endpoint='/error', status='500').inc()
    logger.error(json.dumps({"endpoint": "/error", "status": 500, "message": "simulated error"}))
    return jsonify({"status": "error", "message": "Simulated 500 error"}), 500

@app.route('/slow')
def slow():
    delay = random.uniform(1, 3)
    time.sleep(delay)
    REQUEST_COUNT.labels(method='GET', endpoint='/slow', status='200').inc()
    REQUEST_LATENCY.labels(endpoint='/slow').observe(delay)
    logger.warning(json.dumps({"endpoint": "/slow", "status": 200, "latency": delay}))
    return jsonify({"status": "ok", "latency": delay})

@app.route('/metrics')
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)