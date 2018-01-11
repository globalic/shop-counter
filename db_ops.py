from pymongo import MongoClient
import json


with open('configs/connect_db.json') as f:
    conf = json.load(f)

client = MongoClient('{}:{}'.format(conf['host'], conf['port']))
db = getattr(client, conf['db'])

def insert_update_many(key, data, pk=None):
    if key == 'customer_entry':
        # allowing only one customer entry at a time, for now
        if len(data) == 0:
            return (1, 'No Data Provided!')
        cust = db.customers.find({'name': data[0]['name']}).count()
        if cust > 0:
            return (1, 'Already Exists!')
        else:
            db.customers.insert_many(data)
            return (0, 'Customer Registered!')

    elif key == 'transactions' and pk is not None:
        cust = db.customers.find_one({'name': pk})
        if cust is not None:
            if key in cust:
                db.customers.update({'name': pk}, {
                    '$push': {key: {'$each': data} }
                })
            else:
                db.customers.update({'name': pk}, {
                    '$set': {key: data}
                })
        else:
            # this should not be required, if transactions are being inserted
            # customer entry must be existing
            db.customers.insert_one({'name': pk, key: data})
        return (0, 'Transaction Inserted!')

    else:
        pass

def find(table, k, v, required_key=None):
    if required_key is None:
        res = list(db[table].find({k: v}) )
    else:
        res = list(db[table].find({k: v}, {required_key: 1, '_id': 0}) )[0]
        if required_key in res:
            res = res[required_key]
    return res

def update(table, where_k, where_v, key, value):
    res = db[table].update({where_k: where_v},
                           {'$set': {key: value}})
