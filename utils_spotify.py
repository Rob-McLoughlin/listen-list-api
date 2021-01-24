import json
import requests
from requests.auth import HTTPBasicAuth
import utils
import base64
import urllib.parse
from pprint import pprint

def sy_get_token(client_id: str, client_secret: str) -> dict:
  """Gets a Spotify token

  Args:
      client_id (str): Client ID
      client_secret (str): Client secret

  Returns:
      dict: Response with tokens
  """
  
  url = 'https://accounts.spotify.com/api/token'
  data = {'grant_type': 'client_credentials'}
  r = requests.post(url, data, auth=HTTPBasicAuth(client_id, client_secret))
  if r.status_code == 200:
    return r.json()
  else:
    raise ValueError(f"{r.status_code}, {r.text}")

def sy_search(term: str, key: dict, search_type='album,artist'):
  """Searches spotify for albums and artists

  Args:
      term (str): The search term
      key (dict): A key object,
      search_type (str, optional): comma separated types to search. Defaults to album,artist.
  """
  query = {
    "q": term,
    "type": search_type
  }
  url = 'https://api.spotify.com/v1/search?{}'.format(urllib.parse.urlencode(query))
  headers = {'Authorization': f"Bearer {key['access_token']}"}
  r = requests.get(url, headers=headers)
  if r.status_code == 200:
    return r.json()
  else:
    raise ValueError(f"{r.status_code}, {r.text}")


if __name__ == '__main__':
  client_id = utils.keys('sy_client_id')
  client_secret = utils.keys('sy_client_secret')
  token = sy_get_token(client_id, client_secret)
  results = sy_search('Kid A', token)
  albums = [album for album in results['albums']['items']]
  artists = [artist for artist in results['artists']['items']]
  print(f"There are {len(albums)} albums and {len(artists)} artists found")
  # print('Artists:', [artist['name'] for artist in artist])
  # print(results)
