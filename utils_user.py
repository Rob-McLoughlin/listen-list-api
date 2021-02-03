import boto3
import utils

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

if __name__ == "__main__":
  email = 'robbiemcloughlin@gmail.com'
  username = 'rob2'
  pw = 'Password1@'
  sign_up(username, email, pw)
