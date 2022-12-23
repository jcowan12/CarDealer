import pymongo

with open("credentials.txt", "r") as f:
    user, password, ipAddress = f.read().splitlines()

client = pymongo.MongoClient('mongodb://'+user+':'+password+'@'+ipAddress+'/')