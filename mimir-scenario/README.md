# Mimir Scenario – Metrics Storage

> Videos 4–6 of the DevOps Hobbies LGTM series

---

## Deploying Grafana Mimir on Kubernetes Using Its Helm Chart

```bash
kubectl create namespace mimir
helm install mimir grafana/mimir-distributed -n mimir -f helm-values/mimir-values.yaml
```

> ⚠️ Update the MinIO credentials in `helm-values/mimir-values.yaml` before
> running.

---

## Adding Grafana Mimir Datasource to Grafana

Install (or upgrade) Grafana with both Mimir and Loki datasources provisioned:

```bash
helm upgrade --install grafana grafana/grafana -n grafana \
  -f helm-values/grafana-values.yaml
```

In Grafana → **Explore** → select **Mimir** (Prometheus-compatible) and run
PromQL queries like:

```promql
# CPU usage across all nodes
rate(container_cpu_usage_seconds_total[5m])

# Memory working set per pod
container_memory_working_set_bytes{namespace="nginx"}
```

---

## Collecting Metrics Using Grafana Agent Operator Mode and Static Mode

### Operator mode

Install the Agent Operator (if not already done):

```bash
helm install collector grafana/grafana-agent-operator
```

Deploy Agent CRDs:

```bash
# Root resource
kubectl apply -f grafana-agent-operator/grafana-agent.yaml

# MetricsInstance – remote_write target
kubectl apply -f grafana-agent-operator/metrics-instance.yaml

# ServiceMonitors for kubelet and cAdvisor
kubectl apply -f grafana-agent-operator/kubelet-svc-monitor.yaml
kubectl apply -f grafana-agent-operator/cadvisor-svc-monitor.yaml
```

### Static mode (alternative)

```bash
kubectl apply -f grafana-agent-static/configmap.yaml
kubectl apply -f grafana-agent-static/deployment.yaml
```

---

## Migrate from Grafana Agent Static to Grafana Alloy

```bash
kubectl create ns alloy-metrics
kubectl apply -f migrate-from-agent-to-alloy/metrics/alloy-configmap.yaml
kubectl apply -f migrate-from-agent-to-alloy/metrics/cadvisor-service-monitor.yaml
kubectl apply -f migrate-from-agent-to-alloy/metrics/kubelet-service-monitor.yaml
helm install alloy-metrics grafana/alloy -n alloy-metrics \
  -f migrate-from-agent-to-alloy/metrics/alloy-helm-values.yaml
```

## Migrate from Grafana Agent Operator to Grafana Alloy

```bash
# Remove old Operator CRDs
kubectl delete -f grafana-agent-operator/cadvisor-svc-monitor.yaml
kubectl delete -f grafana-agent-operator/kubelet-svc-monitor.yaml
kubectl delete -f grafana-agent-operator/metrics-instance.yaml
kubectl delete -f grafana-agent-operator/grafana-agent.yaml

# Deploy Alloy
kubectl create ns alloy-metrics
kubectl apply -f migrate-from-agent-to-alloy/metrics/alloy-configmap.yaml
helm install alloy-metrics grafana/alloy -n alloy-metrics \
  -f migrate-from-agent-to-alloy/metrics/alloy-helm-values.yaml
```
