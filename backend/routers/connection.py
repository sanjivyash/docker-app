from typing import Dict
from pydantic import ValidationError
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Query
from hashlib import shake_256

from models import user, manager
from config import constants
from middleware import auth

router = APIRouter(
    prefix="/ws",
    tags=["websocket"]
  )

managers: Dict[str, manager.ConnectionManager] = {}

@router.websocket("/ws/create/{id}")
async def create_room(websocket: WebSocket, id: str, token:str=Query(..., alias="x-auth-token")):
  person: user.User = auth.authenticate(token)
  expression = person.username + constants.secret + id
  token = shake_256(expression.encode()).hexdigest(5)
  
  if token in managers:
    try:
      await websocket.accept()
      await websocket.send_json({ "error": "Watch Party exists for this video" })
      await websocket.close(code=1002)
    except WebSocketDisconnect:
      pass
    finally:
      return
  
  room = manager.ConnectionManager(id, token, person.username)
  managers[token] = room
  await room.connect(person.username, websocket)
  await websocket.send_json({ "token": token })

  try:
    while True:
      if websocket.state.active:
        try:
          data = await websocket.receive_json()
          event = manager.Event(**data)
          await room.multicast(event, person.username)
        except ValueError or ValidationError:
          await websocket.send_json({ "error": "Invalid payload received" })
  except WebSocketDisconnect:
    await room.dissolve()
    print("Room has been dissolved")
    del managers[token]
  except AssertionError:
    print("ASSERTION ERROR")


@router.websocket("/ws/join/{id}")
async def join_room(websocket: WebSocket, id: str, token:str=Query(..., alias="x-auth-token")):
  person: user.User = auth.authenticate(token)
  
  if id not in managers:
    try:
      await websocket.accept()
      await websocket.send_json({ "error": "No such watch party token" })
      await websocket.close(code=1002)
    except WebSocketDisconnect:
      pass
    finally:
      return

  room = managers[id]
  if not await room.connect(person.username, websocket):
    return

  try:
    while True:
      if websocket.state.active:
        try:
          data = await websocket.receive_json()
          event = manager.Event(**data)
          await room.multicast(event, person.username)
        except ValueError or ValidationError:
          await websocket.send_json({ "error": "Invalid payload received" })
  except WebSocketDisconnect:
    await room.disconnect(person.username, websocket)
  except AssertionError:
    pass
