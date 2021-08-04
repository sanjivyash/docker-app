from typing import Dict
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
import jwt

from models import user, manager
from config import constants
from middleware import auth

router = APIRouter(
    prefix="/ws",
    tags=["websocket"]
  )

managers: Dict[str, manager.ConnectionManager] = {}

@router.websocket("/ws/create/{id}")
async def create_room(websocket: WebSocket, id: str, person: user.User=Depends(auth.authenticate)):
  token = jwt.encode({ "username": person.username, "id": id }, constants.secret, algorithm="HS256")
  
  if token in managers:
    await websocket.close(code=1002)
    return
  
  room = manager.ConnectionManager(id, token, person.username)
  print(f'Room Created\n {room}')
  managers[token] = room
  await room.connect(person.username, websocket)
  await websocket.send_json({ "token": token })

  try:
    while True:
      if websocket.state.active:
        data = await websocket.receive_text()
        await room.multicast(data, person.username)
  except WebSocketDisconnect:
    await room.dissolve()
    print("Room has been dissolved")
    del managers[token]
  except AssertionError:
    print("ASSERTION ERROR")


@router.websocket("/ws/join/{id}")
async def join_room(websocket: WebSocket, id: str, person: user.User=Depends(auth.authenticate)):
  if id not in managers:
    await websocket.close(code=1002)
    return

  room = managers[id]
  await room.connect(person.username, websocket)

  try:
    while True:
      if websocket.state.active:
        data = await websocket.receive_text()
        await room.multicast(data, person.username)
  except WebSocketDisconnect:
    await room.disconnect(person.username, websocket)
  except AssertionError:
    pass
