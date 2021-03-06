from typing import Optional, Dict
from pydantic import BaseModel
from hashlib import blake2b

class User(BaseModel):
  username: str
  password: str
  token: Optional[str]
  access: Optional[float]

  def hash(self):
    self.password = blake2b(self.password.encode()).hexdigest()


class UserDisplay(BaseModel):
  username: str
  portfolio: Optional[str]


class UserAuth(BaseModel):
  username: str
  password: str