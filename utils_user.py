import boto3
import utils
import json

def sign_up(username: str, email: str, password: str):
  client = boto3.client('cognito-idp')
  response = client.sign_up(
    ClientId=utils.keys('cog_app_id'),
    Username=username,
    Password=password,
    UserAttributes=[
        {
            'Name': 'email',
            'Value': email
        },
    ],
  )
  print(response)
  return response

def sign_in(username: str, password: str):
  client = boto3.client('cognito-idp')
  params = {
    'USERNAME': username,
    'PASSWORD': password
  }
  response = client.admin_initiate_auth(
    UserPoolId=utils.keys('cog_pool_id'),
    ClientId=utils.keys('cog_app_id'),
    AuthFlow='ADMIN_NO_SRP_AUTH',
    AuthParameters=params
  )
  return response
  
if __name__ == "__main__":
  email = 'robbiemcloughlin@gmail.com'
  username = 'rob2'
  pw = 'Password1@'
  # sign_up(username, email, pw)
  response = sign_in(username, pw)
  with open('key.json', 'w') as outfile:
    json.dump(response, outfile, indent=2)
