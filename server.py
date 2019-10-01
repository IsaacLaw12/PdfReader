from flask import abort, redirect, url_for, Flask

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello World"
