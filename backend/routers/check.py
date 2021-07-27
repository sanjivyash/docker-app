from fastapi import APIRouter, status, HTTPException, Header, Depends
from pymongo import MongoClient

from models import user
from config import constants
from middleware import auth

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
  )

@router.post("/check", response_model=user.UserDisplay)
def check_sensitive(inpuser: user.UserAuth, person: user.User = Depends(auth.authenticate)):
  assert(inpuser.username == person.username)
  return person
