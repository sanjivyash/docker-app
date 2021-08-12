import uvicorn
from config import constants

if __name__ == "__main__":
  if constants.debug:
    import test

  uvicorn.run(
    app="app.main:app", 
    host="0.0.0.0", 
    port=constants.port, 
    reload=constants.debug
  )
