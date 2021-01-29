
import pytest
import utils

def test_format_response():
  statusCode = 200
  message = 'Test response'
  response = utils.format_response(statusCode, {"body": message})
  assert type(response) == dict
  assert response['statusCode'] == 200

def test_keys():
  assert type(utils.keys()) == dict
  assert type(utils.keys('cog_app_id')) == str
  assert utils.keys('abc') == None


## DYNAMO TESTS
def test_create_listen_list():
  albums = [
    {
      "album_id": 123,
      "artist_id": 123,
      "artist_title": "Radiohead",
      "album_title": "Kid A",
      "spotify_link": "https://open.spotify.com/album/6GjwtEZcfenmOf6l18N7T7?si=im-0p4eEQz2Nz6zM6JprLA",
      "spotify_album_id": 123,
      "spotify_artist_id": 123,
      "rating": 9,
      "listened_to": False
    }
  ]
  owner_id = 0
  title = 'Listen List 1'
  new_list = utils.create_ll(owner_id, title, albums)
  assert new_list != False
  new_id = new_list['list_id']
  # Make sure the new list is in the db
  db_list = utils.get_ll(new_id)
  assert type(db_list) == dict