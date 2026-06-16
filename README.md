# SRE Observability Pipeline — Real-Time Infrastructure Monitoring

A production-grade observability stack built with Grafana, Loki, Promtail, and Prometheus deployed on AWS EC2 using Docker Compose.

## Architecture
Sample App → Promtail → Loki → Grafana
Sample App → Prometheus → Grafana
EC2 System → Node Exporter → Prometheus → Grafana

## Stack

| Tool | Purpose |
|---|---|
| Prometheus | Metrics collection and storage |
| Loki | Log aggregation and storage |
| Promtail | Log shipping agent |
| Grafana | Visualization and dashboards |
| Node Exporter | EC2 system metrics |
| Flask App | Sample instrumented application |

## Golden Signals Monitored

- **Latency** — `http_request_duration_seconds`
- **Traffic** — `http_requests_total`
- **Errors** — HTTP 4xx/5xx rate
- **Saturation** — CPU, memory, disk via node-exporter

## Project Structure

\```
sre-observability/
├── docker-compose.yml
├── prometheus/
│   └── prometheus.yml
├── loki/
│   └── loki-config.yml
├── promtail/
│   └── promtail-config.yml
├── grafana/
│   └── provisioning/
│       └── datasources/
│           └── datasources.yml
└── app/
    ├── app.py
    ├── requirements.txt
    └── Dockerfile
\```

## Setup & Run

### Prerequisites
- AWS EC2 (Ubuntu 22.04, t2.medium)
- Docker & Docker Compose installed

### Run

```bash
git clone https://github.com/Bharath204-coder/sre-observability.git
cd sre-observability
docker-compose up -d
```

### Access

| Service | URL |
|---|---|
| Grafana | http://\<EC2-IP\>:3000 |
| Prometheus | http://\<EC2-IP\>:9090 |
| Sample App | http://\<EC2-IP\>:8080 |
| Loki | http://\<EC2-IP\>:3100 |

Grafana login: `admin / admin123`

## Fault Simulation

```bash
# Trigger 500 errors
for i in {1..50}; do curl http://localhost:8080/error; done

# Trigger high latency
for i in {1..20}; do curl http://localhost:8080/slow; done

# Flood normal traffic
for i in {1..100}; do curl http://localhost:8080/; done
```

## Dashboards

- HTTP Request Rate
- Error Rate (4xx/5xx)
- Request Latency (p50, p95, p99)
- CPU & Memory Saturation

## Key Achievements

- Deployed containerized observability stack on AWS EC2
- Ingests structured JSON logs via Promtail into Loki
- LogQL dashboards targeting SRE Golden Signals
- HTTP 4xx/5xx spike detection under 30 seconds
- Stress-tested 15+ fault scenarios against SLO thresholds
