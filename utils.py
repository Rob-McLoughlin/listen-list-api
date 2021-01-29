import json
import boto3
from boto3.dynamodb.types import TypeDeserializer
from botocore.exceptions import ClientError
from datetime import datetime
import uuid


def format_response(status: int, body: dict) -> dict:
    return {"statusCode": status, "body": json.dumps(body)}


def keys(key=None) -> dict:
    """Returns data from the credentials file

    Args:
        key (str, optional): Optional filter to return one value. Defaults to None.

    Returns:
        dict: The data in the credentials file
    """
    with open("credentials.json", "r") as data_file:
        data = json.load(data_file)
        if key is not None:
            if key in data:
                return data[key]
            else:
                return None
        return data


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
    ll = get_ll("248c917e-a9ce-47a2-8c28-73fa594452e2")
    print(ll["albums"])
