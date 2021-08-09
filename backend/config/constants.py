import os 

##### DOCKER/LOCAL ENV #########
host = os.getenv("HOST") or "127.0.0.1"
port = 8000
debug = True

user = os.getenv("DBUSER") or "root"
password = os.getenv("DBPASS") or "password"
uri = f'mongodb://{user}:{password}@mongodb'
dbname = os.getenv("DBNAME") or "movies"

secret = os.getenv("JWT_SECRET") or "secret"
expiry = float(os.getenv("EXPIRY_TIME") or 600)
