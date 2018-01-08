from pymongo import MongoClient
import json


with open('configs/connect_db.json') as f:
    conf = json.load(f)

client = MongoClient('{}:{}'.format(conf['host'], conf['port']))
db = getattr(client, conf['db'])

def insert_multi(table, data):
    res = db[table].insert_many(data)
    return res.inserted_ids

def find(table, k, v, required_key=None):
    res = db[table].find({k: v})
    if required_key is None:
        return res
    return (None if required_key not in res else res[required_key])
