from fastapi import APIRouter, status, HTTPException
from pymongo import MongoClient
from .models import User
from config.constants import uri, dbname

router = APIRouter(
  prefix="/users",
  tags=["user"]
)

@router.post("/signup")
def signup(user: User):
  with MongoClient(uri) as client:
    usercoll = client[dbname]["users"]
    
    if usercoll.find_one({ "username": user.username }) is not None:
      raise HTTPException(
          status_code=status.HTTP_400_BAD_REQUEST,
          detail={ "error" : f'Username {user.username} is already in use' }
        )

    usercoll.insert_one(dict(user))
