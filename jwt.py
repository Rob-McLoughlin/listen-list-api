import json
import time
import urllib.request
import utils
from jose import jwk, jwt
from jose.utils import base64url_decode
from typing import Union
import boto3


def check_token_validity(token: str, token_type="id") -> Union[dict, bool]:
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
    local_jwk = json.load(open("jwks.json"))
    keys = local_jwk["keys"]
    headers = jwt.get_unverified_headers(token)
    kid = headers["kid"]
    # search for the kid in the downloaded public keys
    key_index = -1
    for i in range(len(keys)):
        if kid == keys[i]["kid"]:
            key_index = i
            break
    if key_index == -1:
        print("Public key not found in jwks.json")
        return False
    # construct the public key
    public_key = jwk.construct(keys[key_index])
    # get the last two sections of the token,
    # message and signature (encoded in base64)
    message, encoded_signature = str(token).rsplit(".", 1)
    # decode the signature
    decoded_signature = base64url_decode(encoded_signature.encode("utf-8"))
    # verify the signature
    if not public_key.verify(message.encode("utf8"), decoded_signature):
        print("Signature verification failed")
        return False
    print("Signature successfully verified")
    # since we passed the verification, we can now safely
    # use the unverified claims
    claims = jwt.get_unverified_claims(token)
    # additionally we can verify the token expiration
    if time.time() > claims["exp"]:
        print("Token is expired")
        return False
    # and the Audience  (use claims['client_id'] if verifying an access token)
    value_to_check = claims.get("aud") or claims.get("client_id")
    if value_to_check != utils.keys("cog_client_id"):
        print("Token was not issued for this audience")
        return False
    # now we can use the claims
    # print(claims)
    return claims

def extend_token(token: str) -> Union[dict, bool]:
    """Refreshes a valid token

    Args:
        token (str): The RefreshToken

    Returns:
        Union[dict, bool]: New keys or false
    """

    client = boto3.client('cognito-idp')
    params = {
        'REFRESH_TOKEN': token
    }
    response = client.admin_initiate_auth(
        UserPoolId=utils.keys('cog_pool_id'),
        ClientId=utils.keys('cog_client_id'),
        AuthFlow='REFRESH_TOKEN_AUTH',
        AuthParameters=params
    )
    return response

if __name__ == "__main__":
    tokens = json.load(open('key.json'))
    r_token = tokens['AuthenticationResult']['RefreshToken']
    updated = extend_token(r_token)
    print(updated)
