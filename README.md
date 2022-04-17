# Selfhosted Health Check

Configurable small utility that checks if a service is running.

# Why

I use this with [homer](https://github.com/bastienwirtz/homer) on my selfhosted services.
Instead of fixing CORS on every service I just created this, and now I can set cors policy
on just this API (with nginx reverse proxy) and use the endpoint parameter in homer's config.


# Installation

### Prerequisites
- python3
- virtualenv

```bash
curl https://raw.githubusercontent.com/sujaldev/selfhosted-healthcheck/main/install.sh | bash
```

# Configuration

Edit `/opt/healthcheck/config.yml` to add services

```yaml
service_name:
  test_type: test_parameters
  test_type:
    - multiple_parameters
    - multiple_parameters
another_service:
  test_type: test_parameters
```

Where

- `service_name` will be used in the url so that `https://health.example.com/service_name` will return the status of the
  service.
- `test_type` can be any of the following:

| Test Type | Parameter(s)      | Description                                                                |
|:----------|:------------------|----------------------------------------------------------------------------|
| service   | service name(s)   | checks systemctl for an active service with the given name                 |
| container | container name(s) | checks docker for a running container with the given name                  |
| web       | url(s)            | checks whether website is active by making a head request to the given url |

# Responses:

| HTTP Status Code | Description       |
|:-----------------|:------------------|
| 200              | active            |
| 503              | inactive          |
| 404              | undefined service |

# Uninstallation

```bash
sudo rm -r /opt/healthcheck
sudo rm /etc/systemd/system/healthcheck.service
```
