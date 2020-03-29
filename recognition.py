from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def index():
    return 'blank'


@app.route("/link")
def link():
    return "linked"


@app.route("/hello")
def hello():
    return "hello world"


@app.route("/load")
def load():
    return "loaded"


@app.route("/unlink")
def unlink():
    return "unlinked"


if __name__ == "__main__":
    app.run(debug=True)
