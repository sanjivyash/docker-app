import os 

##### DOCKER/LOCAL ENV #########
host = os.getenv("HOST", default="127.0.0.1")
port = 8000
debug = True

user = os.getenv("DBUSER", default="root")
password = os.getenv("DBPASS", default="password")
uri = f'mongodb://{user}:{password}@mongodb'
dbname = os.getenv("DBNAME", default="movies")

secret = os.getenv("JWT_SECRET", default="secret")
expiry = float(os.getenv("EXPIRY_TIME", default=600))
