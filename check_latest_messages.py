import os
import django
from pymongo import MongoClient
import json
from bson import ObjectId
from datetime import datetime
from dotenv import load_dotenv

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'skillxchange.settings')
django.setup()

# Load .env file
load_dotenv()

def check_latest_messages():
    # Use environment variables if set, else defaults
    uri = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/')
    db_name = os.getenv('MONGODB_NAME', 'skillxchange_db')
    
    client = MongoClient(uri)
    db = client[db_name]
    collection = db['messages']
    
    print("--- MONGODB MESSAGE VERIFICATION ---")
    print(f"Database: {db_name}")
    print(f"Total count: {collection.count_documents({})}")
    print("\nLATEST 10 MESSAGES:")
    print("-" * 50)
    
    # Sort by timestamp descending to get latest
    latest = list(collection.find().sort('timestamp', -1).limit(10))
    
    if not latest:
        print("No messages found in the database.")
    else:
        for m in reversed(latest): # Show in chronological order
            sender = m.get('sender_id')
            receiver = m.get('receiver_id')
            text = m.get('text')
            ts = m.get('timestamp')
            conv = m.get('conversation_id')
            
            # Format timestamp
            if isinstance(ts, datetime):
                ts_str = ts.strftime("%Y-%m-%d %H:%M:%S")
            else:
                ts_str = str(ts)
                
            print(f"[{ts_str}] [Swap {conv}] User {sender} -> User {receiver}: {text}")
    print("-" * 50)

if __name__ == "__main__":
    check_latest_messages()
