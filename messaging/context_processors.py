from messaging.models import message_manager

def unread_messages(request):
    coll = message_manager._get_collection()
    connected = coll is not None
    if request.user.is_authenticated and connected:
        count = message_manager.get_unread_count(request.user.id)
        return {'unread_count': count, 'mongo_connected': True}
    return {'unread_count': 0, 'mongo_connected': connected}
