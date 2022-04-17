import argparse
from yaml import load
from definitions import *

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

__all__ = ['read_config', 'run_testcases']

# ############# Test Type Automatic Registration ############# #

# This will contain all the test types accessible in the config.yml
# any function ending with "_active" will be automatically registered.
registered_definitions = {
    func_name.removesuffix("_active"): func
    for func_name, func in globals().copy().items()
    if func_name.endswith("_active")
}


def run_testcases(testcases: dict) -> bool:
    for test_type, test in testcases.items():
        test_passed = run_unit_test(test_type, test)
        if not test_passed:
            return False
    return True


def run_unit_test(test_type, test_parameters):
    test_func = registered_definitions[test_type]
    if type(test_parameters) is str:
        return test_func(test_parameters)

    for parameter in test_parameters:
        test_passed = test_func(parameter)
        if not test_passed:
            return False
    return True


# ################### CLI Arguments Parser ################### #

def parse_cli_args(sys_args):
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config", nargs=1, default=["'/opt/healthcheck/config.yml'"], type=ascii)
    config_path = parser.parse_args(sys_args).config[-1].strip("'")
    return config_path


def read_config(sys_args):
    config_path = parse_cli_args(sys_args)
    with open(config_path) as config:
        config = load(config, Loader=Loader)
        if config:
            return config
        return {}


if __name__ == "__main__":
    import sys

    print(
        "Registered Definitions:",
        *registered_definitions.keys(),
        "\nParsed Config:",
        read_config(sys.argv[1:]),
        sep="\n"
    )
