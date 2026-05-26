import os
import django
from pymongo import MongoClient
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'skillxchange.settings')
django.setup()

from django.conf import settings

def check_mongo():
    client = MongoClient(os.getenv('MONGODB_URI', 'mongodb://localhost:27017/'))
    db = client[os.getenv('MONGODB_NAME', 'skillxchange_db')]
    collection = db['messages']
    
    print(f"Total messages in SQL: {collection.count_documents({})}")
    
    # Check messages for swap_id 1
    swap_id = "1"
    msgs = list(collection.find({'conversation_id': swap_id}))
    print(f"\n--- Messages for Conversation ID {swap_id} ---")
    print(f"Count: {len(msgs)}")
    for m in msgs:
        print(f"Sender: {m.get('sender_id')}, Receiver: {m.get('receiver_id')}, Text: {m.get('text')}, Read: {m.get('is_read')}")

    # Check for any other conversation_ids
    all_ids = collection.distinct('conversation_id')
    print(f"\nDistinct Conversation IDs: {all_ids}")

if __name__ == "__main__":
    check_mongo()
