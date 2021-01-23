import utils
from flask import Flask
app = Flask(__name__)


@app.route("/")
def hello():
  return utils.format_response(200, {"message": "Hello!"})

