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


# @app.route("/search", methods=["GET"])
# def search():
#     q = request.args.get("q")
#     search_type = request.args.get("type") or "album,artist"
#     sy_token = utils_spotify.sy_get_token()

#     sy_search_results = utils_spotify.sy_search(q, sy_token, search_type)
#     response = utils.format_response(200, sy_search_results)
#     return response




@app.route("/lists/create", methods=["POST"])
def create_list() -> dict:
    """Creates an empty list

    Returns:
        [dict]: [description]
    """
    if request.headers.get('Authorization') == None:
        return utils.format_response(403, 'Not Authorised')
    token = request.headers.get('Authorization').split('Bearer ')[1]
    validity = jwt.check_token_validity(token)
    if validity:
        user_id = validity['username']
        list_title = "Listen List"
        new_id = str(uuid.uuid4())
        listen_list = ListenList(
            list_id=new_id,
            owner_id=user_id,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            list_title=list_title,
            albums=[],
        )
        print(listen_list)
        # Save the new list
        listen_list.store()
        # Return the list JSON
        formatted = ListenListSchema().dump(listen_list)
        response = utils.format_response(200, formatted)
        return response
    else:
        response = utils.format_response(403, 'Not Authorised')
        return response

@app.route("/lists/delete/<list_id>", methods=["DELETE"])
def delete_list(list_id):
    if request.headers.get('Authorization') == None:
        return utils.format_response(403, 'Not Authorised')
    token = request.headers.get('Authorization').split('Bearer ')[1]
    validity = jwt.check_token_validity(token)
    if validity:
        ll = utils.get_ll(list_id)
        print(ll.owner_id)
        # ll.delete()
        response = utils.format_response(200, 'Deleted List')
        return response

@app.route("/users/create", methods=["POST"])
def create_new_user():
    email = request.json.get('email')
    password = request.json.get('password')
    sign_up_request = utils_user.sign_up(email, password)
    return utils.format_response(200, sign_up_request)

@app.route("/users/confirm", methods=["POST"])
def confirm_new_user():
    email = request.json.get('email')
    code = request.json.get('code')
    confirm_user_request = utils_user.confirm_user(email, code)
    return utils.format_response(200, confirm_user_request)
    

@app.route("/users/login", methods=["POST"])
def sign_in():
    email = request.json.get('email')
    password = request.json.get('password')
    sign_in_request = utils_user.sign_in(email, password)
    return utils.format_response(200, sign_in_request)
    
    
@app.route("/users/extend", methods=["POST"])
def extend_token():
    refresh_token = request.json.get('refresh_token')
    refresh_request = jwt.extend_token(refresh_token)
    return utils.format_response(200, refresh_request)
    