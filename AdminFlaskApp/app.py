from flask import Flask, jsonify, Blueprint
from .jobs import init as init_jobs

app = Flask(__name__)
# app.config.from_envvar("APP_CONFIG_FILE")


init_jobs(app)


bp = Blueprint("default", __name__, url_prefix="/foo")


@bp.route("/")
def index():
    return jsonify({"message": "Welcome to the Flask App"})


@bp.route("/hello")
def hello():
    return jsonify({"message": "Hello from Flask!"})


app.register_blueprint(bp)
