from django.db import models
from django.conf import settings
from django.utils import timezone

class SwapRequest(models.Model):
    STATUS_CHOICES = [
        ('P', 'Pending'),
        ('A', 'Accepted'),
        ('R', 'Rejected'),
        ('W', 'Withdrawn'),
    ]
    requester = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='swap_requests_sent')
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='swap_requests_received')
    skill_offered = models.ForeignKey('profiles.Skill', on_delete=models.SET_NULL, null=True, related_name='offered_swaps')
    skill_requested = models.ForeignKey('profiles.Skill', on_delete=models.SET_NULL, null=True, related_name='requested_swaps')
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='P')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.requester} -> {self.receiver} ({self.get_status_display()})"
