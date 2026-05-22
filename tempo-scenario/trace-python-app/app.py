"""
trace-python-app/app.py
Simple Flask app that simulates a dice roll.
The OpenTelemetry Operator injects the Python SDK automatically when the
pod carries the annotation:
  instrumentation.opentelemetry.io/inject-python: "true"

When running locally (without the operator), you can manually instrument:
  pip install opentelemetry-distro opentelemetry-exporter-otlp
  opentelemetry-bootstrap -a install
  opentelemetry-instrument python app.py
"""

import random
import logging
from flask import Flask, jsonify

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)


@app.route("/rolldice")
def roll_dice():
    player = "anonymous"
    result = do_roll()
    logger.info("Player %s rolled a %d", player, result)
    return jsonify({"player": player, "roll": result})


@app.route("/healthz")
def health():
    return jsonify({"status": "ok"})


def do_roll():
    return random.randint(1, 6)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=False)
