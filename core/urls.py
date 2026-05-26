from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('faq/', views.faq_view, name='faq'),
    path('community/', views.community_view, name='community'),
    path('privacy/', views.privacy_view, name='privacy'),
    path('terms/', views.terms_view, name='terms'),
]
