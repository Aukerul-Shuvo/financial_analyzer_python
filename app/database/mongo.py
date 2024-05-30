from pymongo import MongoClient
from app.config import Config

client = MongoClient(Config.MONGO_URI)
db = client[Config.get_database_name()]
