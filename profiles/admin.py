from django.contrib import admin
from .models import Profile, Skill, Rating

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'name')
    search_fields = ('name', 'user__username')
    list_filter = ('skills_offered', 'skills_wanted')

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')
    search_fields = ('name', 'category')

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('rated_user', 'rater', 'score', 'created_at')
    search_fields = ('rated_user__name', 'rater__username')
    list_filter = ('score', 'created_at')
