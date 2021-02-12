import pytest
import utils_user
import json

test_email_address = 'hi@robmcloughlin.io'
test_password = "c9US]TkQs^H7,%ZZ"

def test_sign_up():
  email = test_email_address

  # Delete the account if it exists
  utils_user.delete_account(email)

  # Purposefully bad password
  password = 'abc123'
  # Try to create a user with the above credentials
  attempt = utils_user.sign_up(email, password)
  assert type(attempt) == dict
  assert attempt['success'] != True
  assert 'Password did not conform with policy' in attempt['details']

  # Empty password
  password = ''
  attempt = utils_user.sign_up(email, password)
  assert attempt['success'] != True
  assert 'Parameter validation failed' in attempt['details']
  assert 'Password' in attempt['details']

  # Empty Email
  email = ''
  password = '1234abC!!!!'
  attempt = utils_user.sign_up(email, password)
  assert attempt['success'] != True
  assert 'Parameter validation failed' in attempt['details']
  assert 'Username' in attempt['details']

  # Good Param Data
  email = test_email_address
  password = '1234abC!!!!'
  attempt = utils_user.sign_up(email, password)
  assert attempt['success'] == True
  assert 'Parameter validation failed' not in attempt['details']
  assert 'UserSub' in attempt['details']

  # Check that you can't sign up again with the same email
  attempt = utils_user.sign_up(email, password)
  assert attempt['success'] == False
  assert 'email already exist' in attempt['details']

  # Delete the test user
  utils_user.delete_account(test_email_address)

def test_sign_in():
  # Create the user first
  email = test_email_address
  password = "c9US]TkQs^H7,%ZZ"
  utils_user.sign_up(email, password)

  # Try to log in with the wrong password
  attempt = utils_user.sign_in(email, '123')
  assert attempt['success'] == False
  assert 'Incorrect username or password' in attempt['details']

  # Use the correct password this time
  # This should fail because the user hasn't confirmed their account
  attempt = utils_user.sign_in(email, password)
  assert attempt['success'] == False
  assert 'User is not confirmed' in attempt['details']

  # Confirm the user
  attempt = utils_user.confirm_user_admin(email)
  assert attempt['success'] == True

  # Use the correct password this time
  # This should pass now because the user is confirmed
  attempt = utils_user.sign_in(email, password)
  assert attempt['success'] == True

  # Delete the test user
  utils_user.delete_account(test_email_address)