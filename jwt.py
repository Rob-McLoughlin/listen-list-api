import json
import time
import urllib.request
import utils
from jose import jwk, jwt
from jose.utils import base64url_decode
from typing import Union
        
def check_token_validity(token: str) -> Union[dict, bool]:
  """Checks the validity of a token

  Args:
      token (str): The jwt token

  Returns:
      Union[dict, bool]: The claims or False, if the token is invalid
  """
  # instead of re-downloading the public keys every time
  # we download them only on cold start
  # https://aws.amazon.com/blogs/compute/container-reuse-in-lambda/
  # keys_url = 'https://cognito-idp.{}.amazonaws.com/{}/.well-known/jwks.json'.format('eu-west-1', utils.keys('cog_pool_id'))
  # with urllib.request.urlopen(keys_url) as f:
    # response = f.read()
  local_jwk = json.load(open('jwks.json'))
  keys = local_jwk['keys']
  headers = jwt.get_unverified_headers(token)
  kid = headers['kid']
  # search for the kid in the downloaded public keys
  key_index = -1
  for i in range(len(keys)):
      if kid == keys[i]['kid']:
          key_index = i
          break
  if key_index == -1:
      print('Public key not found in jwks.json')
      return False
  # construct the public key
  public_key = jwk.construct(keys[key_index])
  # get the last two sections of the token,
  # message and signature (encoded in base64)
  message, encoded_signature = str(token).rsplit('.', 1)
  # decode the signature
  decoded_signature = base64url_decode(encoded_signature.encode('utf-8'))
  # verify the signature
  if not public_key.verify(message.encode("utf8"), decoded_signature):
      print('Signature verification failed')
      return False
  print('Signature successfully verified')
  # since we passed the verification, we can now safely
  # use the unverified claims
  claims = jwt.get_unverified_claims(token)
  # additionally we can verify the token expiration
  if time.time() > claims['exp']:
      print('Token is expired')
      return False
  # and the Audience  (use claims['client_id'] if verifying an access token)
  if claims['aud'] != keys('cog_app_id'):
      print('Token was not issued for this audience')
      return False
  # now we can use the claims
  print(claims)
  return claims

if __name__ == '__main__':
  token = 'eyJraWQiOiJGZFwvZ0MwMVhWWFVCVWtUeTgzVlNmKzY1U21BNVE2ZXBCbDdNMmtBcEV5Zz0iLCJhbGciOiJSUzI1NiJ9.eyJzdWIiOiI2N2I2NmY3Yy0wNDliLTRmYTktOWUwMi01MDc3YjU4NDNhMGYiLCJhdWQiOiI1bWp2dGhibjBycmtvczBvZDM5bGhqZDRuOSIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJldmVudF9pZCI6ImE2MzI0OGI5LTU2MzctNGI2ZC1hYjI3LTE4NGE1MTEzMmFkMyIsInRva2VuX3VzZSI6ImlkIiwiYXV0aF90aW1lIjoxNjEyNzIwNTM0LCJpc3MiOiJodHRwczpcL1wvY29nbml0by1pZHAuZXUtd2VzdC0xLmFtYXpvbmF3cy5jb21cL2V1LXdlc3QtMV9EQlVERkFRc0IiLCJjb2duaXRvOnVzZXJuYW1lIjoicm9iMiIsImV4cCI6MTYxMjcyNDEzNCwiaWF0IjoxNjEyNzIwNTM0LCJlbWFpbCI6InJvYmJpZW1jbG91Z2hsaW5AZ21haWwuY29tIn0.LcRAXeKv-hHd1Ste2zh6kbCC5Jaa4LjlGEzqF12SepQRjYhI3RB78oG-rFUJ1wrxRLFR1XCkO9ji4tpJulLRgN_MaZLr75gguaFG0VNQmCrmbVjnKGbSwWGaNw3Vr18zFlLQEDvjOB8coPuL0WEzsgG-6hUu4ocFVP3MaEBRCViaFisOodMIhorymJXHIpRk4fIt3wQI9KLYu_9tLV_dDE3VbIUM74V3Sgx4iaRSfbm7ayhcnjFr1t8syN4YQ1VaiiOMwGsi1elf2k8JPGfxmdb2uNsYPi6ui7_NgP3jcDpGZX8F1j2eTR_3JYyGH0lZrT_8hg67f_5DYycQLrn8dA'
  check = check_token_validity(token)
  print(check)