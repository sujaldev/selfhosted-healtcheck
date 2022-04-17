sudo python3 -c '
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
print(f"Installing at {installation_dir}...")
Path(installation_dir).mkdir(parents=True, exist_ok=True)
print("Done\n")

# Create Virtualenv
print("Initializing virtual environment...")
cli_run([installation_dir + "venv"])
print("Done\n")

# Install Dependencies
print("Installing Dependencies...")
with urlopen(repository_base_url + "requirements.txt") as requirements:
    dependencies = requirements.read().decode().strip().split("\n")
subprocess.check_call([installation_dir + "venv/bin/python3", "-m", "pip", "install"] + dependencies)
print("Done\n")

# Fetch Scripts
print("Fetching Scripts...")
for script in scripts:
    with urlopen(src_dir_url + script) as response, open(installation_dir + script, "w") as script_file:
        script_file.write(response.read().decode())
    print(f"Fetched {script}")
print("Done\n")

# Initialize Config File
print("Initializing Config File...")
with open(installation_dir + "config.yml", "w") as config:
    config.write("---\n")
print("Done\n")

# Setup Systemd
print("Installing service file...")
# 1) Ensure systemd directory exists
Path("/etc/systemd/system/").mkdir(parents=True, exist_ok=True)
# 2) Fetch
with urlopen(repository_base_url + "healthcheck.service") as response, open(service_file_path, "w") as service_file:
    template = response.read().decode()
    service_file.write(template.format(installation_dir=installation_dir))
print("Done\n")

print(
    "########################################################################",
    "Installation Complete!\n",
    "1) Start service by running:",
    "   systemctl start healthcheck.service\n",
    "2) To automatically start on boot run:",
    "   systemctl enable healthcheck.service",
    sep="\n"
)
'
