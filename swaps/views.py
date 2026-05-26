from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import SwapRequest
from django.contrib import messages

@login_required
def requests_dashboard(request):
    """View all incoming and outgoing swap requests with professional labels."""
    sent_requests = SwapRequest.objects.filter(requester=request.user).order_by('-created_at')
    received_requests = SwapRequest.objects.filter(receiver=request.user).order_by('-created_at')

    context = {
        'sent_requests': sent_requests,
        'received_requests': received_requests
    }
    return render(request, 'swaps/requests.html', context)

@login_required
def send_request(request, username):
    """Send a new swap request to another user."""
    receiver = get_object_or_404(User, username=username)
    
    if receiver == request.user:
        messages.error(request, "You cannot swap with yourself.")
        return redirect('view_public_profile', username=username)
    
    # Check for existing pending request
    existing = SwapRequest.objects.filter(requester=request.user, receiver=receiver, status='P').exists()
    if existing:
        messages.warning(request, "Request already sent!")
        return redirect('view_public_profile', username=username)
    
    SwapRequest.objects.create(requester=request.user, receiver=receiver, status='P')
    messages.success(request, f"Swap request sent to {username}!")
    return redirect('requests_dashboard')

@login_required
def accept_request(request, request_id):
    """Accept an incoming swap request (Status 'A')."""
    swap_req = get_object_or_404(SwapRequest, id=request_id, receiver=request.user)
    swap_req.status = 'A'
    swap_req.save()
    messages.success(request, f"You matched with {swap_req.requester.username}! You can now start collaborating.")
    # In a full system, we could send a notification here too.
    return redirect('chat', swap_id=swap_req.id)

@login_required
def reject_request(request, request_id):
    """Reject an incoming swap request (Status 'R')."""
    swap_req = get_object_or_404(SwapRequest, id=request_id, receiver=request.user)
    swap_req.status = 'R'
    swap_req.save()
    messages.info(request, "Swap request declined.")
    return redirect('requests_dashboard')

@login_required
def withdraw_request(request, request_id):
    """Withdraw a sent swap request (Status 'W')."""
    swap_req = get_object_or_404(SwapRequest, id=request_id, requester=request.user)
    swap_req.status = 'W'
    swap_req.save()
    messages.info(request, "You have withdrawn your swap request.")
    return redirect('requests_dashboard')
