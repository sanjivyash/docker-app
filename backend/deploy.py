import uvicorn
from config.constants import *

if __name__ == "__main__":
  if debug:
    import test

  uvicorn.run(
    app="app.main:app", 
    host=host, 
    port=port, 
    reload=debug
  )
