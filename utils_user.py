import boto3
from botocore.exceptions import ClientError, ParamValidationError
import utils
import json


def sign_up(email: str, password: str):
    client = boto3.client("cognito-idp")
    response = {"success": False, "details": ""}
    try:
        attempt = client.sign_up(
            ClientId=utils.keys("cog_client_id"),
            Username=email,
            Password=password,
        )
        response['success'] = True
        response['details'] = attempt
    except ClientError as e:
        response['details'] = e.response['Error']['Message']
    except ParamValidationError as e:
        response['details'] = str(e)
    finally:
      return response


def sign_in(username: str, password: str):
    client = boto3.client("cognito-idp")
    params = {"USERNAME": username, "PASSWORD": password}
    response = client.admin_initiate_auth(
        UserPoolId=utils.keys("cog_pool_id"),
        ClientId=utils.keys("cog_client_id"),
        AuthFlow="ADMIN_NO_SRP_AUTH",
        AuthParameters=params,
    )
    return response

def delete_account(email: str) -> dict:
    """Deletes a user

    Args:
        email (str): The email to delete

    Returns:
        dict: success and details
    """
    client = boto3.client("cognito-idp")
    response = {"success": False, "details": ""}
    try:
        attempt = client.admin_delete_user(
            UserPoolId=utils.keys('cog_pool_id'),
            Username=email
        )
        response['success'] = True
        response['details'] = attempt
    except ClientError as e:
        response['details'] = e.response['Error']['Message']
    except ParamValidationError as e:
        response['details'] = str(e)
    finally:
      return response

if __name__ == "__main__":
    pass
