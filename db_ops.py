from pymongo import MongoClient
import json
import re
import time

with open('configs/connect_db.json') as f:
    conf = json.load(f)

client = MongoClient('mongodb://{}:{}'.format(conf['host'], conf['port']))
db = getattr(client, conf['db'])

def insert_many(key, data=[], pk=None):
    if len(data) == 0:
        return (1, 'No Data Provided!')
        
    elif key == 'customer_entry':
        # allowing only one customer entry at a time, for now
        cust = db.customers.find({'name': data[0]['name']}, {'name': 1}).count()
        if cust > 0:
            return (1, 'Already Exists!')
        else:
            data = add_timestamp(data)
            db.customers.insert_many(data)
            return (0, 'Customer Registered!')

    elif key == 'transactions' and pk is not None:
        data = add_timestamp(data)
        if 'updated_at' not in data[0]:
            db.customers.update({'name': pk}, {
                '$push': {key: {'$each': data} }
            })
            return (0, 'Transaction Inserted!')
        else:
            update_nested(data[0], pk, key)
            return (0, 'Transaction Updated!')
        
    else:
        return (1, 'Invalid Operation!')

def find(table, k, v, required_key=None, match_exact=True):
    res = []
    if v == '' or v is None:
        return []
    if not match_exact:
        v = re.compile(v, re.IGNORECASE)

    if required_key is None:
        res = list(db[table].find({k: v}) )
    else:
        res = list(db[table].find({k: v}, {required_key: 1, '_id': 0}))[0]
        if required_key in res:
            res = res[required_key]
    return res

def update_nested(new_doc, pk, nesting_key, nested_doc_id='created_at'):
    search_key = '{}.{}'.format(nesting_key, nested_doc_id)
    processed_doc = {}
    for k, v in new_doc.items():
        processed_doc['{}.$.{}'.format(nesting_key, k)] = v
    res = db['customers'].update({'name': pk, search_key: new_doc['created_at']},
                           {'$set': processed_doc})
                           
def add_timestamp(data):
    # ideally this ids should be created at database level, since currently this 
    # is a single user app, it doesn't really matter
    for doc in data:
        key = 'created_at'
        if key in doc:
            key = 'updated_at'
        doc[key] = str(time.time())
    return data
    
