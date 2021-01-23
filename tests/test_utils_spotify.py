import pytest
import utils_spotify
import utils

def test_sy_get_token():
  client_id = utils.keys('sy_client_id')
  client_secret = utils.keys('sy_client_secret')
  token = utils_spotify.sy_get_token(client_id, client_secret)
  assert type(token) == dict
  assert 'access_token' in token
  with pytest.raises(ValueError):
    utils_spotify.sy_get_token('', client_secret)