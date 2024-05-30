from app.database.mongo import db
import pandas as pd
from bson import ObjectId

def save_transaction(transactions, unique_id):
    records = transactions.to_dict("records")
    for record in records:
        record['uuid'] = unique_id
    db.transactions.insert_many(records)

def save_analysis_results(analysis_results, unique_id):
    analysis_results['uuid'] = unique_id
    db.analysis_results.insert_one(analysis_results)

def get_transactions(uuid):
    return pd.DataFrame(list(db.transactions.find({"uuid": uuid})))

def get_total_transaction_count():
    return db.transactions.count_documents({})

def get_all_transactions():
    return pd.DataFrame(list(db.transactions.find()))

def save_analysis(analysis):
    result = db.analysis.insert_one(analysis)
    analysis['_id'] = str(result.inserted_id)  # Convert id to string
    return analysis

def get_last_n_analyses(n):
    # Retrieve last n analyses sorted by id in descending order
    analyses = list(db.analysis.find().sort('_id', -1).limit(n))
    # Convert id to string and return results
    for analysis in analyses:
        analysis['_id'] = str(analysis['_id'])
    return analyses