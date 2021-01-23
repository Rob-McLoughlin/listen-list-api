import json
import boto3

def format_response(status: int, body: dict) -> dict:
  return {
    "statusCode": status,
    "body": json.dumps(body)
  }

def keys(key=None) -> dict:
  """Returns data from the credentials file

  Args:
      key (str, optional): Optional filter to return one value. Defaults to None.

  Returns:
      dict: The data in the credentials file
  """
  with open('credentials.json', 'r') as data_file:
    data = json.load(data_file)
    if key is not None:
      if key in data:
        return data[key]
      else:
        return None
    return data
