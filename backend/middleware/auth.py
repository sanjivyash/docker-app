from fastapi import status, HTTPException, Header
from pymongo import MongoClient
from bson.objectid import ObjectId
import jwt
import time

from models import user
from config import constants

def authenticate(x_auth_token: str = Header(None)):
  try:
    token = x_auth_token
    id = jwt.decode(token, constants.secret, algorithms=["HS256"])["_id"]
  except:
    raise HTTPException(
          status_code=status.HTTP_401_UNAUTHORIZED,
          detail={ "error" : f'Invalid token' }
      )

  with MongoClient(constants.uri) as client:
    usercoll = client[constants.dbname]["users"]
    document = usercoll.find_one({ "_id": ObjectId(id) })

    if document is None or token not in document["tokens"]:
      raise HTTPException(
          status_code=status.HTTP_401_UNAUTHORIZED,
          detail={ "error" : f'Invalid token' }
      )
    
    created_at = document["tokens"][token]
    if time.time() - created_at > constants.expiry:
      raise HTTPException(
          status_code=status.HTTP_401_UNAUTHORIZED,
          detail={ "error" : f'Token expired, please login again' }
      )

  return user.User(**document)