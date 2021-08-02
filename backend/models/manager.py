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
  load: str


class ConnectionManager():
  token: str
  id: str
  owner: str
  members: Dict[str, WebSocket] = {}

  def __init__(self, id, token, owner):
    self.id = id
    self.token = token
    self.owner = owner

  def __repr__(self):
    return f'id: {self.id}\n token: {self.token}\n owner: {self.owner}'

  async def connect(self, username: str, websocket: WebSocket):
    if username in self.members:
      await websocket.close()
      websocket.state.active = False
      return
    
    await websocket.accept()
    websocket.state.active = True
    self.members[username] = websocket

  async def disconnect(self, username: str, websocket: WebSocket):
    if username not in self.members or not websocket.state.active:
      websocket.state.active = False
      return
    
    websocket.state.active = False
    del self.members[username]
    await self.broadcast(f'{username} has left the watch party')

  async def dissolve(self):
    del self.members[self.owner]
    await self.broadcast("This watch party has been dissolved by the owner")
    processes = []
    
    for username, websocket in self.members.items():
      websocket.state.active = False
      processes.append(websocket.close())
      print("Closed connection with " + username)

    self.members = {}
    for process in processes:
      await process

  async def multicast(self, message: Union[Event, str], sender: str):
    if sender not in self.members or not self.members[sender].state.active:
      return

    for username, websocket in self.members.items():
      if username != sender and websocket.state.active:
        await websocket.send_text(f'{sender}: {message}')

  async def broadcast(self, message: Union[Event, str]):
    for _, websocket in self.members.items():
      if websocket.state.active:
        await websocket.send_text(message)
