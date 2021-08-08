from typing import Dict, Union
from fastapi import WebSocket
from pydantic import BaseModel
from enum import Enum

class Action(str, Enum):
  pause = "pause"
  resume = "resume"
  chat = "chat"
  dissolved = "dissolved"


class Event(BaseModel):
  action: Action
  load: Dict[str, Union[int, str]]


class ConnectionManager():
  def __init__(self, id, token, owner):
    self.id = id
    self.token = token
    self.owner = owner
    self.members = {}

  def __repr__(self):
    return f'id: {self.id}\n owner: {self.owner}'

  async def connect(self, username: str, websocket: WebSocket):
    await websocket.accept()

    if username in self.members:
      await websocket.send_json({ "error": "You've already joined this watch party" })
      await websocket.close(code=1002)
      websocket.state.active = False
      return False
    
    websocket.state.active = True
    message = f'{username} has joined the watch party'
    event = Event(action=Action.chat, load={ "message": message })
    await self.broadcast(event)
    self.members[username] = websocket
    return True

  async def disconnect(self, username: str, websocket: WebSocket):
    if username not in self.members or not websocket.state.active:
      websocket.state.active = False
      return
    
    websocket.state.active = False
    del self.members[username]
    message = f'{username} has left the watch party'
    event = Event(action=Action.chat, load={ "message": message })
    await self.broadcast(event)

  async def dissolve(self):
    del self.members[self.owner]
    processes = []
    
    for username, websocket in self.members.items():
      await websocket.send_json({ "error": "Owner has dissolved the watch party" })
      websocket.state.active = False
      processes.append(websocket.close())
      print("Closed connection with " + username)

    self.members = {}
    for process in processes:
      await process

  async def multicast(self, event: Event, sender: str):
    if sender not in self.members or not self.members[sender].state.active:
      return

    for username, websocket in self.members.items():
      if username != sender and websocket.state.active:
        await websocket.send_json({ "sender": sender, "event": dict(event)})

  async def broadcast(self, event: Event):
    for _, websocket in self.members.items():
      if websocket.state.active:
        await websocket.send_json({ "sender": "bot", "event": dict(event)})
