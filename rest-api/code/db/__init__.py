import os

from pymongo import MongoClient


def client():
    return MongoClient(os.getenv('MONGO_DB_URI'))


def default_db():
    return client().street_data
