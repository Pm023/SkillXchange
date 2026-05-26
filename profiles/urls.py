from django.urls import path
from . import views

urlpatterns = [
    path('profile/', views.profile_view, name='profile'),
    path('search/', views.skill_search, name='search'),
    path('edit-skills/', views.edit_skills, name='edit_skills'),
    path('view/<str:username>/', views.view_public_profile, name='view_public_profile'),
]
