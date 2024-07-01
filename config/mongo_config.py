import pymongo

# Create the client
client = pymongo.MongoClient('localhost', 27017)
db = client['tehnika_bot_db']
users = db['users']
vehicles = db['vehicles']
