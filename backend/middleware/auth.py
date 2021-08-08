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
    id = objectid.ObjectId(payload["_id"])

  except jwt.InvalidTokenError or KeyError or errors.InvalidId:
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid token"
      )

  with MongoClient(constants.uri) as client:
    usercoll = client[constants.dbname]["users"]
    document = usercoll.find_one({ "_id": id })

    if document is None or token != document["token"]:
      raise HTTPException(
          status_code=status.HTTP_401_UNAUTHORIZED,
          detail="Invalid token"
        )
    
    access = time.time()

    if access - document["access"] > constants.expiry:
      raise HTTPException(
          status_code=status.HTTP_401_UNAUTHORIZED,
          detail="Token expired, please login again"
        )

    document["access"] = access
  return user.User(**document)
