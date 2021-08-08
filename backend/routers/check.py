from fastapi import APIRouter, Depends

from models import user, manager
from middleware import auth

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
  )

@router.get("/check")
def check_sensitive(person: user.User = Depends(auth.authenticate)):
  return
