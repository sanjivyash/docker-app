import time
from hashlib import blake2b
from fastapi import APIRouter, status, HTTPException
from typing import Dict
from pymongo import MongoClient
import jwt

from models import user
from config import constants

router = APIRouter(
    prefix="/users",
    tags=["user"]
  )


@router.post("/signup", response_model=user.UserDisplay, status_code=201)
def signup(person: user.User):
  with MongoClient(constants.uri) as client:
    usercoll = client[constants.dbname]["users"]
    
    if usercoll.find_one({ "username": person.username }) is not None:
      raise HTTPException(
          status_code=status.HTTP_400_BAD_REQUEST,
          detail={ "error" : f'Username {person.username} is already in use' }
        )

    person.hash()
    usercoll.insert_one(dict(person))
  return person


@router.post("/login", response_model=Dict[str, str])
def login(person: user.UserAuth):
  with MongoClient(constants.uri) as client:
    usercoll = client[constants.dbname]["users"]
    document = usercoll.find_one({ "username": person.username })
    
    if document is None or blake2b(person.password.encode()).hexdigest() != document["password"]:
      raise HTTPException(
          status_code=status.HTTP_401_UNAUTHORIZED,
          detail={ "error" : f'Invalid Credentials' }
        )

    token = jwt.encode({ "_id": str(document["_id"]), "time": time.time() }, constants.secret, algorithm="HS256")
    document["tokens"][token] = time.time()

    for token in list(document["tokens"].keys()):
      created_at = document["tokens"][token]
      if time.time() - created_at > constants.expiry:
        del document["tokens"][token] 

    usercoll.replace_one({ "_id": document["_id"]}, document)
  return { "x-auth-token": token }
