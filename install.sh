#!/usr/bin/env python3
import subprocess
from pathlib import Path
from urllib.request import urlopen
from virtualenv import cli_run

# Variables
installation_dir = "/opt/healthcheck/"
service_file_path = "/etc/systemd/system/healthcheck.service"
repository_base_url = "https://raw.githubusercontent.com/sujaldev/selfhosted-healthcheck/main/"
src_dir_url = repository_base_url + "src/"
scripts = ["app.py", "utils.py", "definitions.py"]

# Create Installation Directory
Path(installation_dir).mkdir(parents=True, exist_ok=True)

# Create Virtualenv
cli_run([installation_dir + "venv"])

# Install Dependencies
with urlopen(repository_base_url + "requirements.txt") as requirements:
    dependencies = requirements.read().decode().strip().split("\n")
subprocess.check_call([installation_dir + "venv/bin/python3", '-m', 'pip', 'install'] + dependencies)

# Fetch Scripts
for script in scripts:
    with urlopen(src_dir_url + script) as response, open(installation_dir + script, 'w') as script_file:
        script_file.write(response.read().decode())

# Initialize Config File
with open(installation_dir + "config.yml", 'w') as config:
    config.write("---\n")

# Setup Systemd
# 1) Ensure systemd directory exists
Path("/etc/systemd/system/").mkdir(parents=True, exist_ok=True)
# 2) Fetch
with urlopen(repository_base_url + "healthcheck.service") as response, open(service_file_path, 'w') as service_file:
    template = response.read().decode()
    service_file.write(template.format(installation_dir=installation_dir))
