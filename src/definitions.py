"""
All Test Types will be defined here, every definition should end with "_active"and shall return boolean type.
"""
import docker
import docker.errors
import subprocess
import requests


def service_active(service) -> bool:
    command = subprocess.run(["systemctl", "is-active", service], capture_output=True, text=True)
    return command.stdout.strip() == "active"


def container_active(container_name) -> bool:
    try:
        docker_client = docker.from_env()
        container = docker_client.containers.get(container_name)
        return container.attrs["State"]["Status"] == "running"
    except docker.errors.NotFound:
        return False


def web_active(url) -> bool:
    try:
        response = requests.head(url, allow_redirects=True)
        return 200 <= response.status_code < 300
    except requests.RequestException:
        return False
