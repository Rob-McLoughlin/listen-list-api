import json
import requests
from requests.auth import HTTPBasicAuth
import utils
import base64
import urllib.parse
import time
from datetime import datetime
import boto3
from classes import Album, AlbumSchema


def sy_get_token() -> dict:
    """Gets a Spotify token using stored credentials

    Returns:
        dict: Response with tokens
    """
    client_id = utils.keys('sy_client_id')
    client_secret = utils.keys('sy_client_secret')
    url = "https://accounts.spotify.com/api/token"
    data = {"grant_type": "client_credentials"}
    r = requests.post(url, data, auth=HTTPBasicAuth(client_id, client_secret))
    if r.status_code == 200:
        token = r.json()
        timestamp = round(time.time())
        token["created_at"] = timestamp
        # Save the token
        existing_keys = utils.keys()
        client = boto3.client('secretsmanager')
        data = {"token": token}
        existing_keys['sy_token'] = json.dumps(token)
        client.put_secret_value(
            SecretId='ListenList',
            SecretString=json.dumps(existing_keys)
        )
        return token
    else:
        raise ValueError(f"{r.status_code}, {r.text}")


def sy_check_token() -> bool:
    """Checks if the cached token dict is still in date

    Returns:
        bool: Whether the token is valid or not
    """
    token = json.loads(utils.keys('sy_token'))
    expiry_sec = token["expires_in"]
    created_at = token["created_at"]
    new_timestamp = created_at + expiry_sec
    return new_timestamp > float(time.time())

def sy_access_token() -> dict:
    """Utility function to return the access token cached token if valid or a new one if not.

    Returns:
        dict: A token
    """
    cached_token = utils.keys('sy_token')
    if sy_check_token():
        return json.loads(cached_token).get('access_token')
    else:
        new_token = sy_get_token()
        return new_token.get('access_token')


def sy_search(term: str, key: dict, search_type="album,artist"):
    """Searches spotify for albums and artists

    Args:
        term (str): The search term
        key (dict): A key object,
        search_type (str, optional): comma separated types to search. Defaults to album,artist.
    """
    query = {"q": term, "type": search_type}
    url = "https://api.spotify.com/v1/search?{}".format(urllib.parse.urlencode(query))
    headers = {"Authorization": f"Bearer {key['access_token']}"}
    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        return r.json()
    else:
        raise ValueError(f"{r.status_code}, {r.text}")

def sy_get_album(album_id: str) -> dict:
    """Returns an album

    Args:
        album_id (str): the spotify album id

    Returns:
        dict: The album object
    """
    token = sy_access_token()
    headers = {
        'Authorization': f"Bearer {token}"
    }
    endpoint = f"https://api.spotify.com/v1/albums/{album_id}"
    r = requests.get(endpoint, headers=headers)
    return r.json()

if __name__ == "__main__":
    a = sy_get_album('7eyQXxuf2nGj9d2367Gi5f')
    # print(a)
