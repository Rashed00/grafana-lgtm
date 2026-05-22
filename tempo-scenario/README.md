# Tempo Scenario – Distributed Tracing

> Videos 7–8 of the DevOps Hobbies LGTM series

---

## Deploying Grafana Tempo on Kubernetes Using Its Helm Chart

```bash
kubectl create namespace tempo
helm install tempo grafana/tempo-distributed -n tempo \
  -f helm-values/tempo-values.yaml
```

---

## Adding Grafana Tempo Datasource to Grafana

```bash
helm upgrade --install grafana grafana/grafana -n grafana \
  -f helm-values/grafana-values.yaml
```

---

## OpenTelemetry Operator Setup

Install `cert-manager` (required by the OTel Operator):

```bash
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/latest/download/cert-manager.yaml
# Wait ~60s for cert-manager to be ready
kubectl wait --for=condition=ready pod -l app=cert-manager -n cert-manager --timeout=120s
```

Install the OpenTelemetry Operator:

```bash
kubectl apply -f https://github.com/open-telemetry/opentelemetry-operator/releases/latest/download/opentelemetry-operator.yaml
```

Deploy the Collector and Instrumentation CRDs:

```bash
# OTel Collector – receives OTLP and forwards traces to Tempo
kubectl apply -f open-telemetry-operator/collector.yaml

# Instrumentation – auto-instruments Python pods
kubectl apply -f open-telemetry-operator/instrumentation.yaml
```

---

## Deploy the Tracing Demo App (Python Flask)

Build and push the image (optional if using the pre-built image):

```bash
cd trace-python-app
docker build -t myapp:latest .
# docker push <your-registry>/myapp:latest  # if using a remote cluster
```

Deploy to Kubernetes:

```bash
kubectl apply -f trace-python-app-manifests/deployment.yaml
kubectl apply -f trace-python-app-manifests/service.yaml
```

Generate traces by hitting the `/rolldice` endpoint:

```bash
kubectl port-forward svc/myapp 8080:8080
# In another terminal:
curl http://localhost:8080/rolldice
# Hit it several times to accumulate traces
```

In Grafana → **Explore** → select **Tempo** → run a **Search** query to see
the `myapp` traces.

---

## Writing Traces to Tempo with Grafana Alloy

Video 8 replaces the OTel Operator with Grafana Alloy acting as the OTLP
collector:

```bash
kubectl create ns alloy-traces
kubectl apply -f grafana-alloy-resources/alloy-configmap.yaml
helm install alloy-traces grafana/alloy -n alloy-traces \
  -f grafana-alloy-resources/alloy-helm-values.yaml
```

Your application only needs to send OTLP traces to
`http://alloy-traces.alloy-traces.svc.cluster.local:4317` (gRPC) or port 4318
(HTTP). Alloy forwards them to Tempo automatically.
