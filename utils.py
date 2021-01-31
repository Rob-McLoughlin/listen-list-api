import json
import boto3
from boto3.dynamodb.types import TypeDeserializer
from botocore.exceptions import ClientError
from datetime import datetime
import uuid
import decimal
import base64


def format_response(status: int, body: dict) -> dict:
    return {"statusCode": status, "body": json.dumps(body)}


def keys(key=None) -> dict:
    """Returns data from ssm

    Args:
        key (str, optional): Optional filter to return one value. Defaults to None.

    Returns:
        dict: The data in the credentials file
    """

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(service_name="secretsmanager", region_name="eu-west-1")

    # In this sample we only handle the specific exceptions for the 'GetSecretValue' API.
    # See https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
    # We rethrow the exception by default.

    try:
        get_secret_value_response = client.get_secret_value(SecretId="ListenList")
    except ClientError as e:
        if e.response["Error"]["Code"] == "DecryptionFailureException":
            # Secrets Manager can't decrypt the protected secret text using the provided KMS key.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response["Error"]["Code"] == "InternalServiceErrorException":
            # An error occurred on the server side.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response["Error"]["Code"] == "InvalidParameterException":
            # You provided an invalid value for a parameter.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response["Error"]["Code"] == "InvalidRequestException":
            # You provided a parameter value that is not valid for the current state of the resource.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response["Error"]["Code"] == "ResourceNotFoundException":
            # We can't find the resource that you asked for.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
    else:
        # Decrypts secret using the associated KMS CMK.
        # Depending on whether the secret is a string or binary, one of these fields will be populated.
        if "SecretString" in get_secret_value_response:
            secret = json.loads(get_secret_value_response["SecretString"])
            if key:
                return secret.get(key)
            return secret
        else:
            decoded_binary_secret = json.loads(
                base64.b64decode(get_secret_value_response["SecretBinary"])
            )
            if key:
                return decoded_binary_secret.get(key)
            return decoded_binary_secret


def replace_decimals(obj):
    """
    Convert all whole number decimals in `obj` to integers
    """
    if isinstance(obj, list):
        return [replace_decimals(i) for i in obj]
    elif isinstance(obj, dict):
        return {k: replace_decimals(v) for k, v in obj.items()}
    elif isinstance(obj, decimal.Decimal):
        return int(obj) if obj % 1 == 0 else obj
    return obj


def create_ll(owner_id: int, title: str, albums: list) -> dict:
    """Creates a new listen list in the database

    Args:
        owner_id (int): The owner of the list
        title (str): The title of the list
        albums (list): List of album objects

    Returns:
        dict: The list item that was created
    """
    item = {
        "list_id": str(uuid.uuid4()),
        "owner_id": owner_id,
        "created_at": datetime.now().strftime("%Y/%m/%dT%H:%M:%S"),
        "updated_at": datetime.now().strftime("%Y/%m/%dT%H:%M:%S"),
        "list_title": title,
        "albums": albums,
    }
    db = boto3.resource("dynamodb")
    table = db.Table("ListenList")
    response = table.put_item(Item=item)
    print(response)
    if response["ResponseMetadata"]["HTTPStatusCode"] == 200:
        return item
    return False


def dynamo_to_dict(dynamo_response: dict) -> dict:
    """Takes a dynamo response and turns it into a dict

    Args:
        dynamo_response (dict): A dynamo schema object

    Returns:
        dict: Dict without the data types
    """
    obj = {}
    keys = dynamo_response.keys()
    for key in keys:
        attribute = dynamo_response[key]
        obj[key] = attribute
    return obj


def get_ll(list_id: str) -> dict:
    """Returns a listen list from the database

    Args:
        list_id (str): The id of the list to return

    Returns:
        dict: The listen list
    """
    db = boto3.resource("dynamodb")
    table = db.Table("ListenList")
    key = {
        "list_id": list_id,
    }
    try:
        response = table.get_item(Key=key)
        item = response["Item"]
        # print(item)
        data = dynamo_to_dict(item)
        return data
        # print(item.keys())
        # To go from low-level format to python
        # return deserialised
        # deserialised = {k: deserialiser.deserialize(v) for k, v in response.get("Item").items()}
        # print(deserialised)
        # TODO: Add not found/error responses
    except ClientError as err:
        raise err


if __name__ == "__main__":
    # albums = [
    #   {
    #     "album_id": 123,
    #     "artist_id": 123,
    #     "artist_title": "Radiohead",
    #     "album_title": "Kid A",
    #     "spotify_link": "https://open.spotify.com/album/6GjwtEZcfenmOf6l18N7T7?si=im-0p4eEQz2Nz6zM6JprLA",
    #     "spotify_album_id": 123,
    #     "spotify_artist_id": 123,
    #     "rating": 9,
    #     "listened_to": False
    #   }
    # ]
    # owner_id = 0
    # title = 'Listen List 1'
    # create_ll(owner_id, title, albums)
    # ll = get_ll("248c917e-a9ce-47a2-8c28-73fa594452e2")
    # ll = replace_decimals(ll)
    # print(ll["albums"])
    # print(json.dumps(ll))
    secret = keys()
    print(secret)