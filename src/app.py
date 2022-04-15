import sys
from flask import Flask
from tester import perform_checks
from config_reader import read_config

app = Flask(__name__)
config = read_config(sys.argv[1:])


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def check(path):
    if path.lower() in config.keys():
        print(path)
        is_active = perform_checks(config[path])
        if is_active:
            return "active"
        else:
            return "inactive", 503
    return "not found", 404


if __name__ == "__main__":
    app.run(port=55004)
