import os 

##### DOCKER ENV #########
# host = os.getenv("HOST")
# port = 8000
# debug = True

# user = os.getenv("DBUSER")
# password = os.getenv("DBPASS")
# uri = f'mongodb://{user}:{password}@mongodb'
# dbname = os.getenv("DBNAME")

# secret = os.getenv("JWT_SECRET")
# expiry = float(os.getenv("EXPIRY_TIME"))

##### LOCAL ENV #########
host = "127.0.0.1"
port = 8000
debug = True

user = "root"
password = "password"
uri = f'mongodb://{user}:{password}@{host}:27017'
dbname = "movies"

secret = "secret"
expiry = 6000
