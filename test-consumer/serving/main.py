import logging
import sys
import time
from flask import Flask, request
from cloudevents.http import from_http

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

app = Flask(__name__)


@app.route("/next-visit", methods=["POST"])
def next_visit_handler():
    event = from_http(request.headers, request.get_data())

    logging.info(f"Found {event['id']} from {event['source']} with type")
    logging.info(f"{event['type']} and specversion event{['specversion']}")
    logging.info(f"Event data {event.data}")

    time.sleep(30)  # sleep to allow for concurrency testing

    return "", 204


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)
