import argparse
from yaml import load

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper


def parse_cli_args(sys_args):
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config", nargs=1, default=["'/opt/healthcheck/config.yml'"], type=ascii)
    config_path = parser.parse_args(sys_args).config[-1].strip("'")
    return config_path


def read_config(sys_args):
    config_path = parse_cli_args(sys_args)
    with open(config_path) as config:
        return load(config, Loader=Loader)[0]


if __name__ == "__main__":
    import sys

    print(read_config(sys.argv[1:]))
