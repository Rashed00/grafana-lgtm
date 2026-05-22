FROM python:3.11-slim

WORKDIR /app

# Install Flask and OpenTelemetry SDK + OTLP exporter
RUN pip install --no-cache-dir \
    flask==3.0.3 \
    opentelemetry-distro==0.46b0 \
    opentelemetry-exporter-otlp==1.25.0 \
    && opentelemetry-bootstrap -a install

COPY app.py .

EXPOSE 8080

# Use opentelemetry-instrument for manual local runs.
# The OTel Operator will override this entrypoint when auto-instrumenting.
CMD ["opentelemetry-instrument", "python", "app.py"]
