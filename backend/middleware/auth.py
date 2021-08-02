from fastapi import status, HTTPException, Header
from pymongo import MongoClient
from bson import objectid, errors
import jwt
import time

from models import user
from config import constants

def authenticate(token: str = Header(..., alias="x-auth-token")):
  try:
    payload = jwt.decode(token, constants.secret, algorithms=["HS256"])
    print(payload)
    id = objectid.ObjectId(payload["_id"])

  except jwt.InvalidTokenError or KeyError or errors.InvalidId:
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail={ "error" : f'Invalid token' }
      )

  with MongoClient(constants.uri) as client:
    usercoll = client[constants.dbname]["users"]
    document = usercoll.find_one({ "_id": id })

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
