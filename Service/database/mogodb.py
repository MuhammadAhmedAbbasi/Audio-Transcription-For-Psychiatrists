from pymongo import MongoClient
from Service.config import *

# Setup MongoDB connection
client = MongoClient(client_uri)
db = client[database_name]
collection = db[collection]
