from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/")
def index():
    return jsonify({"message": "Welcome to the Flask App"})


@app.route("/hello")
def hello():
    return jsonify({"message": "Hello from Flask!"})
