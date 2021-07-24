from fastapi import FastAPI
import users.urls

app = FastAPI()

@app.get("/", tags=["root"])
def index():
  return { "message": "Hello There" }

@app.get("/about", tags=["root"])
def about():
  return { "backend-dev": "me" }

app.include_router(users.urls.router)