
#Que : 1. Create a Flask app that displays "Hello, World!" on the homepage.

from flask import Flask, request, render_template
app = Flask(__name__)


@app.route("/")
def index():
    return f"<center><h1>Hello World!</h1></center>"


if __name__ == "__main__":
    app.run(host="localhost",port=5000)