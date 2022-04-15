import subprocess
import requests


def service_active(service) -> bool:
    # Check whether service is active with systemctl
    if type(service) is list:
        for s in service:
            if not service_active(s):
                return False
        return True

    command = subprocess.run(["systemctl", "is-active", service], capture_output=True, text=True)
    return command.stdout.strip() == "active"


def web_active(url) -> bool:
    # Check if website is reachable

    if type(url) is list:
        for u in url:
            if not web_active(u):
                return False
        return True
    try:
        response = requests.head(url, allow_redirects=True)
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
