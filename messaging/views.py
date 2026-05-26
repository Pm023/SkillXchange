from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import message_manager
from swaps.models import SwapRequest

@login_required
def chat_view(request, swap_id):
    """
    A simple chat interface for an accepted swap request.
    Uses MongoDB for message storage.
    """
    swap = get_object_or_404(SwapRequest, id=swap_id)
    
    # Check if the user is part of this swap
    # Diagnostic: Who is trying to chat?
    print(f"[MESSAGING] VIEW ACCESS: user={request.user.username}(id={request.user.id}), swap_id={swap_id}")
    
    if request.user != swap.requester and request.user != swap.receiver:
        return redirect('home')
        
    # Identify the recipient
    receiver = swap.receiver if request.user == swap.requester else swap.requester
        
    if request.method == 'POST':
        text = request.POST.get('message')
        if text:
            msg = message_manager.send_message(
                conversation_id=swap_id,
                sender_id=request.user.id,
                receiver_id=receiver.id,
                text=text
            )
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                # Convert inserted_id if necessary, though get_messages handles it better
                return JsonResponse({'status': 'success'})
        
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'status': 'error', 'message': 'Empty message'}, status=400)
        return redirect('chat', swap_id=swap_id)
        
    # Mark messages as read for current user in this chat (Do this for both regular and AJAX)
    message_manager.mark_as_read(swap_id, request.user.id)
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        messages = message_manager.get_messages(swap_id)
        # Stringify timestamps for JSON
        for m in messages:
            if 'timestamp' in m and not isinstance(m.get('timestamp'), str):
                m['timestamp'] = m['timestamp'].isoformat()
        
        unread_count = message_manager.get_unread_count(request.user.id)
        print(f"[MESSAGING] AJAX POLLING: user={request.user.username}, messages={len(messages)}, unread={unread_count}")
        return JsonResponse({
            'messages': messages,
            'unread_count': unread_count
        })
        
    messages = message_manager.get_messages(swap_id)
    
    context = {
        'swap': swap,
        'messages': messages,
    }
    return render(request, 'messaging/chat.html', context)

@login_required
def unread_count_view(request):
    """Returns the unread message count for the current user."""
    count = message_manager.get_unread_count(request.user.id)
    return JsonResponse({'unread_count': count})
