import subprocess
import requests
import docker
import docker.errors


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


def container_active(container_name) -> bool:
    if type(container_name) is list:
        for n in container_name:
            if not container_active(n):
                return False
        return True
    try:
        docker_client = docker.from_env()
        container = docker_client.containers.get(container_name)
        return container.attrs["State"]["Status"] == "running"
    except docker.errors.NotFound:
        return False


def perform_checks(testcases: dict):
    for test_type, test_value in testcases.items():
        if test_type == "service" and not service_active(test_value):
            return False
        if test_type == "container" and not container_active(test_value):
            return False
        if test_type == "web" and not web_active(test_value):
            return False
        return True
