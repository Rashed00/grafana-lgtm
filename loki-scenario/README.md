# Loki Scenario – Log Aggregation

> Videos 1–3 of the DevOps Hobbies LGTM series

---

## Deploying Grafana Loki on Kubernetes Using Its Helm Chart

Create a dedicated namespace:

```bash
kubectl create namespace loki
```

Install Loki in **SingleBinary** mode with MinIO as object storage:

```bash
helm install loki grafana/loki -n loki -f helm-values/loki-values.yaml
```

> ⚠️ Before running, open `helm-values/loki-values.yaml` and replace the MinIO
> `accessKeyId` and `secretAccessKey` placeholders with real credentials, and
> update the `bucketNames` if needed.

---

## Adding Grafana Loki Datasource to Grafana

Install Grafana with a pre-provisioned Loki datasource:

```bash
kubectl create namespace grafana
helm install grafana grafana/grafana -n grafana -f helm-values/grafana-values.yaml
```

Retrieve the admin password:

```bash
kubectl get secret -n grafana grafana -o jsonpath="{.data.admin-password}" | base64 -d
```

Port-forward Grafana:

```bash
kubectl port-forward -n grafana svc/grafana 3000:80
```

Open `http://localhost:3000` → **Explore** → select **Loki** datasource.

---

## Collecting Logs Using Grafana Agent Kubernetes Operator

Deploy an Nginx workload to generate logs:

```bash
kubectl apply -f nginx/
```

Install the Grafana Agent Operator:

```bash
helm install collector grafana/grafana-agent-operator
```

Deploy the Agent CRDs in order:

```bash
# 1. Root GrafanaAgent resource
kubectl apply -f grafana-agent-operator/grafana-agent.yaml

# 2. LogsInstance – defines the remote_write target (Loki)
kubectl apply -f grafana-agent-operator/log-instance.yaml

# 3. PodLogs – selects which pods to tail
kubectl apply -f grafana-agent-operator/pod-logs.yaml
```

The pipeline stage inside `pod-logs.yaml` extracts `method` and `status_code`
labels from Nginx access log lines using a regex stage.

### Sample LogQL queries

```logql
# All logs from the nginx namespace
{namespace="nginx"}

# Only 4xx responses
{namespace="nginx", status_code=~"4.*"}

# Rate of log lines per minute
rate({namespace="nginx"}[1m])
```

---

## From Agent to Alloy

Grafana Agent (including the Operator) is **deprecated**. Grafana Alloy is the
successor. The `migrate-from-agent-to-alloy/` folder contains the equivalent
Alloy configuration.

### Migrate logs collection

```bash
# Remove the old Agent CRDs
kubectl delete -f grafana-agent-operator/pod-logs.yaml
kubectl delete -f grafana-agent-operator/log-instance.yaml
kubectl delete -f grafana-agent-operator/grafana-agent.yaml

# Create the Alloy namespace and deploy the ConfigMap
kubectl create ns alloy-logs
kubectl apply -f migrate-from-agent-to-alloy/logs/alloy-configmap.yaml

# Install Alloy via Helm
helm install alloy-logs grafana/alloy -n alloy-logs \
  -f migrate-from-agent-to-alloy/logs/alloy-helm-values.yaml
```

Verify in Grafana **Explore → Loki**: all nginx pods should still stream logs
with the `method` and `status_code` labels attached.
