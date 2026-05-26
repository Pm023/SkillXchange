import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'skillxchange.settings')
django.setup()

from swaps.models import SwapRequest
from django.contrib.auth import get_user_model

User = get_user_model()

def check_swaps():
    print("--- Users ---")
    for u in User.objects.all():
        print(f"ID: {u.id}, Username: {u.username}")

    print("\n--- Swap Requests ---")
    requests = SwapRequest.objects.all()
    for r in requests:
        print(f"ID: {r.id}, Requester: {r.requester.username} (ID:{r.requester.id}), Receiver: {r.receiver.username} (ID:{r.receiver.id}), Status: {r.status}")

if __name__ == "__main__":
    check_swaps()
