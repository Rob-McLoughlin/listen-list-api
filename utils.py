import json

def format_response(status: int, body: dict) -> dict:
  return {
    "statusCode": status,
    "body": json.dumps(body)
  }

