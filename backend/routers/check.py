from fastapi import APIRouter, Depends

from models import user, manager
from middleware import auth

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
  )

@router.post("/check", response_model=manager.Event)
def check_sensitive(event: manager.Event, person: user.User = Depends(auth.authenticate)):
  event.action = manager.Action.resume
  return event
