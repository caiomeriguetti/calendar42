import os

from pymongo import MongoClient


def client():
    return MongoClient(os.getenv('MONGODB_URI'))