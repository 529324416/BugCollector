import pymongo
import tqdm
import time


url = "mongodb://admin:rs_locktown_1018@109.244.159.206:28814/"
client = pymongo.MongoClient(url)
db = client["doloctown"]
collection = db["__spec__bug_report_exception"]

collection.find().sort("__timestamp", pymongo.DESCENDING)
