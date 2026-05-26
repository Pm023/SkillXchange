from django.urls import path
from . import views
from accounts import views as accounts_views

urlpatterns = [
    path('', accounts_views.admin_dashboard, name='admin_dashboard'),
    path('live-editor/', views.live_editor, name='live_editor'),
    path('save-content/', views.save_content, name='save_content'),
]
