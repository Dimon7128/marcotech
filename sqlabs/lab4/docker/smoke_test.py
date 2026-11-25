"""Check the two-container HTTP contract using only Python's standard library."""

import argparse
from html import unescape
import json
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


def request(base_url, path, body=None):
    data = None if body is None else json.dumps(body).encode("utf-8")
    headers = {} if body is None else {"Content-Type": "application/json"}
    outgoing = Request(base_url + path, data=data, headers=headers)
    try:
        with urlopen(outgoing, timeout=15) as response:
            return response.status, response.read().decode("utf-8")
    except HTTPError as error:
        return error.code, error.read().decode("utf-8")


def check(condition, message):
    if not condition:
        raise ValueError(message)
    print("PASS — " + message)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-url", default="http://127.0.0.1:8080")
    parser.add_argument("--app-name", default="SMS Sandbox",
                        help="App name expected in the HTML; set this after rebranding the chat")
    parser.add_argument("--expect-model-down", action="store_true")
    args = parser.parse_args()
    base_url = args.base_url.rstrip("/")

    try:
        status, body = request(base_url, "/")
        check(status == 200 and args.app_name in unescape(body),
              "chat page is served with the expected app name")
        for asset in ("/app.js", "/styles.css"):
            status, body = request(base_url, asset)
            check(status == 200 and bool(body), asset + " is served")
        status, body = request(base_url, "/health")
        check(status == 200 and json.loads(body)["status"] == "ok", "frontend is healthy")

        if args.expect_model_down:
            status, body = request(base_url, "/api/predict", {"message": "Meeting at five"})
            check(status == 503 and isinstance(json.loads(body).get("detail"), str),
                  "backend outage returns a readable JSON error while the chat stays available")
            return

        status, body = request(base_url, "/api/health")
        check(status == 200 and json.loads(body)["status"] == "ok",
              "frontend reaches the model through the Compose network")
        status, body = request(base_url, "/api/predict", {"message": "Meeting at five"})
        check(status == 200 and json.loads(body).get("label") in ("ham", "spam"),
              "prediction follows the label contract")
        for payload in ({"message": ""}, {"message": "   "}, {}):
            status, body = request(base_url, "/api/predict", payload)
            check(status == 422 and isinstance(json.loads(body).get("detail"), list),
                  "invalid input is rejected: " + json.dumps(payload))
    except (URLError, OSError, ValueError, KeyError) as error:
        parser.exit(1, "FAIL — " + str(error) + "\n")


if __name__ == "__main__":
    main()
