from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import routers
from config import constants

app = FastAPI()

origins = [
    f'{constants.host}',
    f'{constants.host}:80',
    f'{constants.host}:8080',
    f'{constants.host}:3000',
  ]

app.add_middleware(
  CORSMiddleware,
  allow_origins=origins,
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)

@app.get("/", tags=["root"])
async def get():
  return { "message": "Hello There" }

@app.get("/about", tags=["root"])
def about():
  return { "backend-dev": "me" }

app.include_router(routers.user.router)
app.include_router(routers.connection.router)
app.include_router(routers.check.router)
