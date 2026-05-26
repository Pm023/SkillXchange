from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.requests_dashboard, name='requests_dashboard'),
    path('send/<str:username>/', views.send_request, name='send_request'),
    path('accept/<int:request_id>/', views.accept_request, name='accept_request'),
    path('reject/<int:request_id>/', views.reject_request, name='reject_request'),
    path('withdraw/<int:request_id>/', views.withdraw_request, name='withdraw_request'),
]
