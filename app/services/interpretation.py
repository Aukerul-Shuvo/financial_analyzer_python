from app.database.mongo import db

def save_interpretation(transaction_id: str, narratives: dict):
    document = {
        "transaction_id": transaction_id,
        "narratives": narratives
    }
    db.analysis_interpretations_collection.insert_one(document)