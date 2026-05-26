import socketio
import logging
from .models import message_manager
from django.contrib.auth.models import User
from asgiref.sync import sync_to_async

# Setup logging
logger = logging.getLogger(__name__)

# Create an Async Socket.IO server
sio = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins='*')

@sio.event
async def connect(sid, environ):
    logger.info(f"Socket connected: {sid}")
    print(f"DEBUG: Socket CONNECTED: {sid}")

@sio.event
async def disconnect(sid):
    logger.info(f"Socket disconnected: {sid}")
    print(f"DEBUG: Socket DISCONNECTED: {sid}")

@sio.event
async def join_room(sid, data):
    room = f"swap_{data.get('swap_id')}"
    await sio.enter_room(sid, room)
    logger.info(f"SID {sid} joined room {room}")
    print(f"DEBUG: {sid} JOINED ROOM: {room}")

@sio.on('send_message')
async def handle_send_message(sid, data):
    """
    Handles incoming messages from a client.
    Expects data: { 'swap_id': ..., 'text': ..., 'sender_id': ..., 'receiver_id': ... }
    """
    swap_id = data.get('swap_id')
    text = data.get('text')
    sender_id = data.get('sender_id')
    receiver_id = data.get('receiver_id')
    
    if not all([swap_id, text, sender_id, receiver_id]):
        return

    # Persist message to MongoDB (Sync call, wrap in sync_to_async)
    await sync_to_async(message_manager.send_message)(
        conversation_id=swap_id,
        sender_id=sender_id,
        receiver_id=receiver_id,
        text=text
    )

    # Prepare message for broadcast
    message_data = {
        'text': text,
        'sender_id': sender_id,
        'receiver_id': receiver_id,
        'timestamp': 'Just now' # Or format a real timestamp
    }

    # Broadcast to the room
    room = f"swap_{swap_id}"
    await sio.emit('receive_message', message_data, room=room)
    print(f"DEBUG: Message BROADCAST to room {room}: {text[:20]}...")

# Wrap the sio instance for ASGI usage
sio_app = socketio.ASGIApp(sio)
