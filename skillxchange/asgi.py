"""
ASGI config for skillxchange project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'skillxchange.settings')
django_asgi_app = get_asgi_application()

# Import SIO after django is initialized to avoid app registry issues
from messaging.socket_server import sio

# The final ASGI application
# Routes starting with /socket.io/ go to Socket.IO, others to Django
import socketio
application = socketio.ASGIApp(sio, django_asgi_app)
