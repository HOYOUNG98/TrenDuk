import time
from flask import Flask

app = Flask(__name__)


@app.cli.command()
def scheduled():
    """Run scheduled job."""
    print('Simulating Job...')
    time.sleep(5)
    print('Done!')


@app.route('/')
def hello_world():
    return 'Hello, World!'
