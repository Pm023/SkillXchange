from django.conf import settings
from datetime import datetime

class MessageManager:
    """
    A simple Pymongo-based manager for storing and retrieving messages.
    """
    def __init__(self):
        self.db = None
        self.collection = None

    def _get_collection(self):
        if self.collection is None:
            try:
                self.db = settings.MONGO_DB
                self.collection = self.db['messages']
            except Exception as e:
                print(f"[MESSAGING] ERROR: Could not access MongoDB - {str(e)}")
                return None
        return self.collection

    def send_message(self, conversation_id, sender_id, receiver_id, text):
        coll = self._get_collection()
        if coll is None: return None
        
        message = {
            'conversation_id': str(conversation_id),
            'sender_id': int(sender_id),
            'receiver_id': int(receiver_id),
            'text': str(text),
            'timestamp': datetime.now(),
            'is_read': False
        }
        try:
            res = coll.insert_one(message)
            print(f"[MESSAGING] Message SENT: from={sender_id}, to={receiver_id}, conv={conversation_id}, id={res.inserted_id}")
            return res
        except Exception as e:
            print(f"[MESSAGING] ERROR during send_message: {str(e)}")
            return None

    def get_messages(self, conversation_id):
        coll = self._get_collection()
        if coll is None: return []
        
        try:
            cid = str(conversation_id)
            msgs = list(coll.find({'conversation_id': cid}).sort('timestamp', 1))
            # Convert ObjectId to string for JSON serialization
            for m in msgs:
                if '_id' in m:
                    m['_id'] = str(m['_id'])
            
            # Extreme Diagnostic: Log the content summary
            snippet = msgs[-1]['text'][:20] + "..." if msgs else "EMPTY"
            print(f"[MESSAGING] DB FETCH: conv={cid}, count={len(msgs)}, latest='{snippet}'")
            return msgs
        except Exception as e:
            print(f"[MESSAGING] ERROR during get_messages: {str(e)}")
            return []

    def get_unread_count(self, user_id):
        coll = self._get_collection()
        if coll is None: return 0
        
        try:
            return coll.count_documents({'receiver_id': int(user_id), 'is_read': False})
        except Exception:
            return 0

    def mark_as_read(self, conversation_id, user_id):
        """Marks all messages in a conversation sent TO user_id as read."""
        coll = self._get_collection()
        if coll is None: return False
        
        try:
            coll.update_many(
                {'conversation_id': str(conversation_id), 'receiver_id': int(user_id), 'is_read': False},
                {'$set': {'is_read': True}}
            )
            return True
        except Exception:
            return False

# Global instance
message_manager = MessageManager()
