import os 

##### DOCKER ENV #########
host = os.getenv("HOST")
port = 8000
reload = True

user = os.getenv("DBUSER")
password = os.getenv("DBPASS")
uri = f'mongodb://{user}:{password}@mongodb'
dbname = os.getenv("DBNAME")

##### SYSTEM ENV #########
# host = "127.0.0.1"
# port = 8000
# reload = True

# user = "root"
# password = "password"
# uri = f'mongodb://{user}:{password}@{host}:27017'
# dbname = "movies"
