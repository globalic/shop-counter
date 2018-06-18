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
        v = '.*'
    if not match_exact:
        v = re.compile(v, re.IGNORECASE)

    if required_key is None:
        res = list(db[table].find({k: v}))
    elif required_key == 'transactions':  
        res = get_multiple_sorted(required_key, k, v) 
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
                           
def delete(field, pk, field_id):
    db['customers'].update({'name': pk, 
        '{}.created_at'.format(field): field_id}, 
        {'$set': {'{}.$.deleted'.format(field): True}}
    )
    
def count(key=None, value=None):
    if not key and not value: 
        return db['customers'].find({'deleted': {'$exists': False}}, 
            {'_id': 1}).count()
    
def get_transactions(skip, limit):
    return list(db['customers'].find({'transactions': {'$exists': True}}, 
        {'_id': 0, 'transactions.credit': 1, 'transactions.debit': 1, 
        'transactions.deleted': 1}).skip(skip).limit(limit))

def add_timestamp(data):
    # ideally this ids should be created at database level, since currently this 
    # is a single user app, it doesn't really matter
    for doc in data:
        key = 'created_at'
        if key in doc:
            key = 'updated_at'
        doc[key] = str(time.time())
    return data
    
def get_multiple_sorted(key, k, v, order_by='dated'):
	dollar_key = '${}'.format(key)
	res = list(db['customers'].aggregate([
		{'$match': {k: v}},
		{'$unwind': dollar_key},
		{'$project': {key: dollar_key, '_id': 0}},
		{'$sort': {'{}.{}'.format(key, order_by): -1}}	
	]))
	for i in range(len(res)):
		res[i] = res[i][key]	
	return res
