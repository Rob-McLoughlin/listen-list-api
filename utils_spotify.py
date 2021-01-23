import json
import requests
from requests.auth import HTTPBasicAuth
import utils
import base64

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
  print(r.status_code, r.text)
  if r.status_code == 200:
    return r.json()
  else:
    raise ValueError(f"{r.status_code}, {r.text}")

if __name__ == '__main__':
  client_id = utils.keys('sy_client_id')
  client_secret = utils.keys('sy_client_secret')
  print(sy_get_token(client_id, client_secret))
