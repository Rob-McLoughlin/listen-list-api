import pytest
import utils_spotify
import utils
import time

def test_sy_get_token():
  client_id = utils.keys('sy_client_id')
  client_secret = utils.keys('sy_client_secret')
  token = utils_spotify.sy_get_token(client_id, client_secret)
  assert type(token) == dict
  assert 'access_token' in token
  assert 'created_at' in token
  with pytest.raises(ValueError):
    utils_spotify.sy_get_token('', client_secret)

def test_sy_check_token():
  token = {
    "created_at": 1611483375,
    "expires_in": 3600
  }
  assert utils_spotify.sy_check_token(token) == False
  token['created_at'] = round(time.time())
  assert utils_spotify.sy_check_token(token) == True

def test_sy_search():
  client_id = utils.keys('sy_client_id')
  client_secret = utils.keys('sy_client_secret')
  token = utils_spotify.sy_get_token(client_id, client_secret)
  search = utils_spotify.sy_search('Kid A', token)
  assert type(search) == dict
  album_results = search['albums']['items']
  album_names = [album['name'] for album in album_results]
  assert 'Kid A' in album_names