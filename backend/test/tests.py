import sys
from typing import Dict
from fastapi.testclient import TestClient

from .format import *

class Test:
  client: TestClient
  username: str = "testuser"
  password: str = "secret"
  header: Dict[str, str]

  def __init__(self, client: TestClient):
    self.client = client

  def __call__(self):
    self.root()
    self.register()
    self.login()
    self.check()
    self.delete()

  def root(self):
    title = formatter("Test 1", "header", "bold")
    status_err = formatter("incorrect response code", "error")
    response_err = formatter("incorrect response body", "error")

    print(f'{title} Testing the root')
    response = self.client.get("/")

    try:
      assert response.status_code == 200, status_err
      assert response.json() == { "message": "Hello There" }, response_err
      print(formatter("Test 1 passed\n", "success"))
    except AssertionError as e:
      print(formatter("AssertionError: ", "bold", "error") + str(e) + "\n")
      sys.exit() 

  def register(self):
    title = formatter("Test 2", "header", "bold")
    status_err = formatter("incorrect response code", "error")
    response_err = formatter("incorrect response body", "error")
    
    print(f'{title} Registering a user')
    input = { "username": self.username, "password": self.password }
    output = { "username": self.username, "portfolio": None }
    response = self.client.post(url="/users/signup", json=input)

    try:
      assert response.status_code == 201, status_err
      assert response.json() == output, response_err
      print(formatter("Test 2 passed\n", "success"))
    except AssertionError as e:
      print(formatter("AssertionError: ", "bold", "error") + str(e) + "\n") 
      sys.exit()

  def login(self):
    title = formatter("Test 3", "header", "bold")
    status_err = formatter("incorrect response code", "error")
    response_err = formatter("incorrect response body", "error")
    
    print(f'{title} Logging a user')
    input = { "username": self.username, "password": self.password }
    response = self.client.post(url="/users/login", json=input)
    
    try:
      assert response.status_code == 200, status_err
      assert list(response.json().keys()) == ["x-auth-token"], response_err
      self.header = response.json()
      print(formatter("Test 3 passed\n", "success"))
    except AssertionError as e:
      print(formatter("AssertionError: ", "bold", "error") + str(e) + "\n")
      sys.exit()

  def check(self):
    title = formatter("Test 4", "header", "bold")
    status_err = formatter("incorrect response code", "error")
    response_err = formatter("incorrect response body", "error")
    
    print(f'{title} Accessing a protected route')
    input = { "action": "pause", "load": { "time": 23, "relay": "all" } }
    output = { "origin": self.username, "event": { "action": "resume", "load": { "time": 23, "relay": "all" } }}
    response = self.client.post(url="/auth/check", json=input, headers=self.header)

    try:
      assert response.status_code == 200, status_err
      assert response.json() == output, response_err
      print(formatter("Test 4 passed\n", "success"))
    except AssertionError as e:
      print(formatter("AssertionError: ", "bold", "error") + str(e) + "\n")
      sys.exit()

  def delete(self):
    title = formatter("Test 5", "header", "bold")
    status_err = formatter("incorrect response code", "error")
    delete_err = formatter("user not deleted", "error")
    response_err = formatter("incorrect response body", "error")
    
    print(f'{title} Deleting a user')
    response = self.client.delete(url="/users/delete", headers=self.header)
    input = { "username": self.username, "password": self.password }
    output = { "username": self.username, "portfolio": None }

    try:
      assert response.status_code == 200, status_err
      assert response.json() == output, response_err
      response = self.client.post(url="/users/login", json=input)
      assert response.status_code == 401, delete_err
      print(formatter("Test 5 passed\n", "success"))
    except AssertionError as e:
      print(formatter("AssertionError: ", "bold", "error") + str(e) + "\n")
      sys.exit()
