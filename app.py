import utils
import utils_spotify
from flask import Flask, request
app = Flask(__name__)

@app.route("/")
def hello():
  return utils.format_response(200, {"message": "Hello!"})

@app.route('/search', methods=['GET'])
def search():
  q = request.args.get('q')
  search_type = request.args.get('type') or 'album,artist'
  client_id = utils.keys('sy_client_id')
  client_secret = utils.keys('sy_client_secret')
  sy_token = utils_spotify.sy_get_token(client_id, client_secret)

  sy_search_results = utils_spotify.sy_search(q, sy_token, search_type)
  response = utils.format_response(200, sy_search_results)
  return response