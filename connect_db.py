from pymongo import MongoClient
import json


with open('configs/connect_db.json') as f:
    conf = json.load(f)

client = MongoClient('{}:{}'.format(conf['host'], conf['port']))
db = getattr(client, conf['db'])

def insert_multi(table, data):
    res = db[table].insert_many(data)
    return res.inserted_ids

def find(k, v, c):
    res = db.customers.find({k: v})
    return res
