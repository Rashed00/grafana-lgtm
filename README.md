# Grafana LGTM Stack

![Grafana LGTM](https://grafana.com/mw/_next/image/?url=https%3A%2F%2Fs3.amazonaws.com%2Fa-us.storyblok.com%2Ff%2F1022730%2F55a072e861%2Fgrafana-labs-lgtm-graphic.png&w=1152&q=75)

Hands-on follow-along repository for the [DevOps Hobbies – Grafana LGTM Stack](https://www.youtube.com/playlist?list=PLYrn63eEqAzZL2TaS0pXXw-_DEl3SsAF_) YouTube series.

## What is the LGTM Stack?

| Letter | Tool | Role |
|--------|------|------|
| **L** | [Grafana Loki](https://grafana.com/oss/loki/) | Log aggregation system |
| **G** | [Grafana](https://grafana.com/oss/grafana/) | Dashboards & visualization |
| **T** | [Grafana Tempo](https://grafana.com/oss/tempo/) | Distributed tracing backend |
| **M** | [Grafana Mimir](https://grafana.com/oss/mimir/) | Long-term metrics storage (Prometheus-compatible) |

Collector layer:
- **Grafana Agent** – legacy telemetry collector (deprecated, use Alloy)
- **Grafana Alloy** – next-gen OpenTelemetry collector (replacement for Agent)

---

## Prerequisites

- A running Kubernetes cluster (e.g. kind, minikube, or a cloud cluster)
- `kubectl` configured to point at that cluster
- `helm` v3+
- `docker` (for building the tracing demo app)

Add the Grafana Helm repo once:

```bash
helm repo add grafana https://grafana.github.io/helm-charts
helm repo update
```

---

## Scenarios

### 📋 Loki Scenario – Log Aggregation (Videos 1–3)

Covers:
- Deploying Grafana Loki on Kubernetes with Helm (SingleBinary + MinIO)
- Adding Loki as a Grafana datasource
- Collecting pod logs with Grafana Agent Operator
- Pipeline stages (regex, labels) to enrich Nginx logs
- Migrating from Grafana Agent to Grafana Alloy (logs)
- LogQL queries and alerting

→ See [loki-scenario/README.md](loki-scenario/README.md)

---

### 📊 Mimir Scenario – Metrics Storage (Videos 4–6)

Covers:
- Deploying Grafana Mimir on Kubernetes with Helm
- Adding Mimir as a Grafana datasource (Prometheus-compatible)
- Collecting kubelet + cAdvisor metrics with Grafana Agent Operator
- Grafana Agent Static mode config
- Migrating Agent Static → Alloy
- Migrating Agent Operator → Alloy

→ See [mimir-scenario/README.md](mimir-scenario/README.md)

---

### 🔍 Tempo Scenario – Distributed Tracing (Videos 7–8)

Covers:
- Deploying Grafana Tempo on Kubernetes with Helm
- OpenTelemetry instrumentation for a Python Flask app
- Deploying the OpenTelemetry Operator (Collector + Instrumentation CRDs)
- Visualising traces in Grafana
- Forwarding traces to Tempo via Grafana Alloy

→ See [tempo-scenario/README.md](tempo-scenario/README.md)

---

## Reference

- [Original course repo](https://github.com/devopshobbies/grafana_lgtm)
- [Instructor's personal stack repo](https://github.com/mohammadll/grafana-stack)
- [Grafana Helm Charts](https://github.com/grafana/helm-charts)
- [Grafana Alloy docs](https://grafana.com/docs/alloy/latest/)
