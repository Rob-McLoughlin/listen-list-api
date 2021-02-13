import json
import boto3
from boto3.dynamodb.types import TypeDeserializer
from botocore.exceptions import ClientError
from datetime import datetime
import uuid
import decimal
import base64
from classes import ListenList, ListenListSchema, Album, AlbumSchema, AlbumCoverSchema
import utils_spotify


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


# TODO: Replace with serialisation
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


def get_ll(list_id: str) -> ListenList:
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
        data = dynamo_to_dict(item)
        # print(data)
        try:
            listen_list = ListenListSchema().load(data)
            return listen_list
        except ClientError as err:
            raise err
        # print(item.keys())
        # To go from low-level format to python
        # return deserialised
        # deserialised = {k: deserialiser.deserialize(v) for k, v in response.get("Item").items()}
        # print(deserialised)
        # TODO: Add not found/error responses
    except ClientError as err:
        raise err

def ll_create(data) -> ListenList:
    return ListenListSchema().load(data)

def album_from_sy_data(sy_data: dict) -> Album:
    """Takes an album response from the Spotify API and turns it into an Album

    Args:
        sy_data (dict): Data from the Spotify API

    Returns:
        Album: The Album object
    """
    images = [
        {
            "height": 640,
            "url": "https://i.scdn.co/image/ab67616d0000b273674c2b8b77e1e9259a2fcb87",
            "width": 640,
        },
        {
            "height": 300,
            "url": "https://i.scdn.co/image/ab67616d00001e02674c2b8b77e1e9259a2fcb87",
            "width": 300,
        },
        {
            "height": 64,
            "url": "https://i.scdn.co/image/ab67616d00004851674c2b8b77e1e9259a2fcb87",
            "width": 64,
        },
    ]

    artists = [
        {
            "name": "Radiohead",
            "spotify_url": "https://open.spotify.com/artist/4Z8W4fKeB5YxbusRsdQVPb",
        }
    ]
    album_data = {
        "spotify_id": sy_data['id'],
        "spotify_url": sy_data['external_urls']['spotify'],
        "title": sy_data["name"],
        "images": sy_data['images'],
        "artists": artists,
        "rating": 0,
        "listened_to": False,
    }
    a = AlbumSchema().load(album_data)
    return a

if __name__ == "__main__":
    in_rainbows = utils_spotify.sy_get_album('7eyQXxuf2nGj9d2367Gi5f')
    new_album = album_from_sy_data(in_rainbows)
    ll = get_ll('abc-123')
    for album in ll.albums:
        print(album.title)
    ll.add_album(new_album)
    for album in ll.albums:
        print(album.title)
    ll.store()