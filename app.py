import utils
import uuid
from datetime import datetime
from classes import ListenList, ListenListSchema
import utils_spotify
import utils_user
import jwt
from flask import Flask, request

app = Flask(__name__)


@app.route("/")
def hello():
    return utils.format_response(200, {"message": "Hello!"})


@app.route("/search", methods=["GET"])
def search():
    q = request.args.get("q")
    search_type = request.args.get("type") or "album,artist"
    client_id = utils.keys("sy_client_id")
    client_secret = utils.keys("sy_client_secret")
    sy_token = utils_spotify.sy_get_token(client_id, client_secret)

    sy_search_results = utils_spotify.sy_search(q, sy_token, search_type)
    response = utils.format_response(200, sy_search_results)
    return response


@app.route("/lists/create", methods=["POST"])
def create_list() -> dict:
    """Creates an empty list

    Returns:
        [dict]: [description]
    """
    list_title = request.json.get("list_title") or "Listen List"
    new_id = str(uuid.uuid4())
    listen_list = ListenList(
        list_id=new_id,
        owner_id=request.json.get("owner_id"),
        created_at=datetime.now(),
        updated_at=datetime.now(),
        list_title=list_title,
        albums=[],
    )
    # Save the new list
    listen_list.store()
    # Return the list JSON
    formatted = ListenListSchema().dump(listen_list)
    response = utils.format_response(200, formatted)
    return response

@app.route("/lists/delete/<list_id>", methods=["DELETE"])
def delete_list(list_id):
    ll = utils.get_ll(list_id)
    ll.delete()
    response = utils.format_response(200, 'Deleted List')
    return response

@app.route("/users/create", methods=["POST"])
def create_new_user():
    username = request.json.get('username')
    email = request.json.get('email')
    password = request.json.get('password')
    sign_up_request = utils_user.sign_up(username, email, password)
    return utils.format_response(200, sign_up_request)
    

@app.route("/users/login", methods=["POST"])
def sign_in():
    username = request.json.get('username')
    password = request.json.get('password')
    sign_in_request = utils_user.sign_in(username, password)
    return utils.format_response(200, sign_in_request)
    
    
@app.route("/users/extend", methods=["POST"])
def extend_token():
    refresh_token = request.json.get('refresh_token')
    refresh_request = jwt.extend_token(refresh_token)
    return utils.format_response(200, refresh_request)
    