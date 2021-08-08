import time
from hashlib import blake2b
from fastapi import APIRouter, status, HTTPException
from typing import Dict
from fastapi.params import Depends
from pymongo import MongoClient
import jwt

from models import user
from config import constants
from middleware import auth

router = APIRouter(
    prefix="/users",
    tags=["user"]
  )


@router.post("/signup", response_model=user.UserDisplay, status_code=201)
def signup(person: user.UserAuth):
  with MongoClient(constants.uri) as client:
    usercoll = client[constants.dbname]["users"]
    
    if usercoll.find_one({ "username": person.username }) is not None:
      raise HTTPException(
          status_code=status.HTTP_400_BAD_REQUEST,
          detail=f'Username {person.username} is already in use'
        )

    person = user.User(**dict(person))
    person.hash()
    usercoll.insert_one(dict(person))
  return person


@router.post("/login", response_model=Dict[str, str])
def login(person: user.UserAuth):
  with MongoClient(constants.uri) as client:
    access = time.time()
    usercoll = client[constants.dbname]["users"]
    document = usercoll.find_one({ "username": person.username })
    
    if document is None or blake2b(person.password.encode()).hexdigest() != document["password"]:
      raise HTTPException(
          status_code=status.HTTP_401_UNAUTHORIZED,
          detail=f'Invalid Credentials'
        )

    if document["token"] is not None: 
      if access - document["access"] > constants.expiry:
        document["token"] = None
        document["access"] = None

    if document["token"] is None:
      token = jwt.encode({ "_id": str(document["_id"]), "time": access }, constants.secret, algorithm="HS256")
      document["token"] = token
    else:
      token = document["token"]
    
    document["access"] = access
    usercoll.replace_one({ "_id": document["_id"] }, document)
  return { "x-auth-token": token }


@router.delete("/delete", response_model=user.UserDisplay)
def remove(person: user.User=Depends(auth.authenticate)):
  with MongoClient(constants.uri) as client:
    usercoll = client[constants.dbname]["users"]
    usercoll.find_one_and_delete({ "username": person.username })
  
  return person