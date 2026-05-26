import os
import django
from django.conf import settings
from pymongo import MongoClient

# Setup Django before importing models
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'skillxchange.settings')
django.setup()

def check_messages():
    client = MongoClient(os.getenv('MONGODB_URI', 'mongodb://localhost:27017/'))
    db = client[os.getenv('MONGODB_NAME', 'skillxchange_db')]
    collection = db['messages']
    
    print(f"Total messages in 'messages' collection: {collection.count_documents({})}")
    
    # Check messages for swap_id 1
    swap_id = "1"
    msgs = list(collection.find({'conversation_id': swap_id}))
    print(f"Messages for Swap ID {swap_id}: {len(msgs)}")
    for m in msgs:
        print(f"ID: {m['_id']}, Sender: {m.get('sender_id')}, Receiver: {m.get('receiver_id')}, Text: {m.get('text')}, Read: {m.get('is_read')}")

if __name__ == "__main__":
    check_messages()
