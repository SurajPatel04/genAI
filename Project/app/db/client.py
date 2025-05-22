from pymongo import AsyncMongoClient

mongo_client: AsyncMongoClient = AsyncMongoClient("mongodb://admin:admin@localhost:27018")
