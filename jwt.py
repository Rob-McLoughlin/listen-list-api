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
    if value_to_check != utils.keys("cog_app_id"):
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
        ClientId=utils.keys('cog_app_id'),
        AuthFlow='REFRESH_TOKEN_AUTH',
        AuthParameters=params
    )
    return response

if __name__ == "__main__":
    tokens = json.load(open('key.json'))
    # token = "eyJraWQiOiJGZFwvZ0MwMVhWWFVCVWtUeTgzVlNmKzY1U21BNVE2ZXBCbDdNMmtBcEV5Zz0iLCJhbGciOiJSUzI1NiJ9.eyJzdWIiOiI2N2I2NmY3Yy0wNDliLTRmYTktOWUwMi01MDc3YjU4NDNhMGYiLCJhdWQiOiI1bWp2dGhibjBycmtvczBvZDM5bGhqZDRuOSIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJldmVudF9pZCI6ImYyMWFhMjk1LWY3ZWUtNGY2Ny04MTI0LWRmMTM0ZjZjNDE0NCIsInRva2VuX3VzZSI6ImlkIiwiYXV0aF90aW1lIjoxNjEyNzMxMTIwLCJpc3MiOiJodHRwczpcL1wvY29nbml0by1pZHAuZXUtd2VzdC0xLmFtYXpvbmF3cy5jb21cL2V1LXdlc3QtMV9EQlVERkFRc0IiLCJjb2duaXRvOnVzZXJuYW1lIjoicm9iMiIsImV4cCI6MTYxMjczNDcyMCwiaWF0IjoxNjEyNzMxMTIwLCJlbWFpbCI6InJvYmJpZW1jbG91Z2hsaW5AZ21haWwuY29tIn0.cqhjQo5SzSU5cyZALimC7rOm5cnJiGRYJYXJcRM4s__cV5e3ntYJtN66i4INx1pcvtAxxD06TRHixiDgFxupoZsJVumlZVwDcnWOOz0XzrUEzXvXzMg7oRD5a-cLa-kkcDivwD6NZuZdwAR7kWDPhvYixmpKc0LEHbLbVOelEK4cADYU1GWespYJFNMtzS2qfbPl_Ca3NS2CZtbUzhBRwmyjMNvfjRtWUwN7LWqhrsOFt2j5j8e5X4R0QYA-EHTCARw2jRrduWVHkxFhzCBu0_1l5i4m0DiY4WSAvhH5cz-WSxm-4WG9gNo8zrfKRTYVdxZ8_msx8SWhD9pXWxAoaQ"
    # token = tokens['AuthenticationResult']['IdToken']
    r_token = tokens['AuthenticationResult']['RefreshToken']
    # check = check_token_validity(token)
    updated = extend_token(r_token)
    print(updated)
