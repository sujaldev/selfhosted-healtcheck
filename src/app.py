import sys
from flask import Flask
from utils import *

app = Flask(__name__)
config = read_config(sys.argv[1:])


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def check(path):
    if path.lower() in config.keys():
        testcases = config[path]
        is_active = run_testcases(testcases)
        if is_active:
            return "active"
        else:
            return "inactive", 503
    return "not found", 404


if __name__ == "__main__":
    app.run(port=55004)
