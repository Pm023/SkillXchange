from django.urls import path
from . import views

urlpatterns = [
    path('<int:swap_id>/', views.chat_view, name='chat'),
    path('unread-count/', views.unread_count_view, name='unread_count'),
]
