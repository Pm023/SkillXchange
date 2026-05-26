from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('secure-admin/login/', views.admin_login_view, name='admin_login'),
    path('secure-admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
]
