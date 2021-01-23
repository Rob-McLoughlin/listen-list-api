import pytest
import utils

def test_format_response():
  statusCode = 200
  message = 'Test response'
  response = utils.format_response(statusCode, {"body": message})
  assert type(response) == dict
  assert response['statusCode'] == 200
