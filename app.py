from flask import Flask
from yaml import load
import subprocess
import requests

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

app = Flask(__name__)

with open("config.yml") as config:
    config = load(config, Loader=Loader)[0]


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def hello_world(path):
    if path.lower() in config.keys():
        print(path)
        is_active = perform_checks(config[path])
        if is_active:
            return "active"
    return "inactive", 503


def service_active(service: str | list) -> bool:
    # Check whether service is active with systemctl
    if type(service) is list:
        for s in service:
            if not service_active(s):
                return False
        return True

    command = subprocess.run(["systemctl", "is-active", service], capture_output=True, text=True)
    return command.stdout.strip() == "active"


def web_active(url: str | list) -> bool:
    # Check if website is reachable

    if type(url) is list:
        for u in url:
            if not web_active(u):
                return False
        return True
    try:
        response = requests.get(url)
        return 200 <= response.status_code < 300
    except requests.RequestException:
        return False


def perform_checks(testcases: dict):
    for test_type, test_value in testcases.items():
        if test_type == "service" and not service_active(test_value):
            return False
        if test_type == "web" and not web_active(test_value):
            return False
        return True


if __name__ == "__main__":
    app.run(port=55004)
