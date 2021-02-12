import os, sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
import pytest
import utils


def test_format_response():
    statusCode = 200
    message = "Test response"
    response = utils.format_response(statusCode, {"body": message})
    assert type(response) == dict
    assert response["statusCode"] == 200


def test_keys():
    assert type(utils.keys()) == dict
    assert type(utils.keys("cog_client_id")) == str
    assert utils.keys("abc") == None
