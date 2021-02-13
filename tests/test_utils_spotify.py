import os, sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
import pytest
import utils_spotify
import utils
import time


def test_sy_get_token():
    token = utils_spotify.sy_get_token()
    assert type(token) == dict
    assert "access_token" in token
    assert "created_at" in token


def test_sy_check_token():
    token = {"created_at": 1611483375, "expires_in": 3600}
    assert utils_spotify.sy_check_token(token) == False
    token["created_at"] = round(time.time())
    assert utils_spotify.sy_check_token(token) == True


def test_sy_search():
    token = utils_spotify.sy_get_token()
    search = utils_spotify.sy_search("Kid A", token)
    assert type(search) == dict
    album_results = search["albums"]["items"]
    album_names = [album["name"] for album in album_results]
    assert "Kid A" in album_names

def test_sy_get_album():
    in_rainbows = utils_spotify.sy_get_album('7eyQXxuf2nGj9d2367Gi5f')
    assert type(in_rainbows) == dict
    assert in_rainbows['name'] == 'In Rainbows'