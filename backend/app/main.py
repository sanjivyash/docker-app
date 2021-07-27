from fastapi import FastAPI
import routers

app = FastAPI()

@app.get("/", tags=["root"])
def index():
  return { "message": "Hello There" }

@app.get("/about", tags=["root"])
def about():
  return { "backend-dev": "me" }

app.include_router(routers.user.router)
app.include_router(routers.check.router)