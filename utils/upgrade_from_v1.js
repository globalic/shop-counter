db = connect('localhost:27017/srjm');
date = new Date();

print('Documents with following name are updated to support new versions:');

updated_n = 0;
while (true) {
		all_docs = db.customers.find({
				'transactions.created_at': {'$exists': false}, 
				'transactions.ref': {'$exists': true}
			}, {'transactions':1, 'name': 1}).limit(10).toArray();

		all_docs.forEach(function (doc, doc_no) {			
			if ('transactions' in doc && doc['transactions'] != undefined) {
				// modify all the docs
				doc['transactions'].forEach(function (trans, i) {
					trans['created_at'] = date.getTime() + "_" + i;
				});

				// update db with new values
				db.customers.update(
					{'_id': doc['_id']}, 
					{$set: {'transactions': doc['transactions']}}
				);
			}
			
			// log
			print(doc['name']);
		});
		
		updated_n += all_docs.length;
		if (all_docs.length < 10) {
			break;
		}
}

var total_n = db.customers.find().count();
print('Total documents: ' + total_n);
print('Updated documetns: ' + updated_n);
