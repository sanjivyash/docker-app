import os 

##### DOCKER/LOCAL ENV #########
containerized = os.getenv("DOCKER_ACTIVE", default="False").lower() in ('true', '1', 't')

host = os.getenv("HOST", default="127.0.0.1")
port = int(os.getenv("PORT", default="8000"))
debug = os.getenv("DEBUG", default="True").lower() in ('true', '1', 't')

user = os.getenv("DBUSER", default="root")
password = os.getenv("DBPASS", default="password")
db = "mongodb" if containerized else f'{host}:27017'

uri = f'mongodb://{user}:{password}@{db}'
dbname = os.getenv("DBNAME", default="movies")

secret = os.getenv("JWT_SECRET", default="secret")
expiry = float(os.getenv("EXPIRY_TIME", default="600"))
