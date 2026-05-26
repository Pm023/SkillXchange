from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    name = models.CharField(max_length=150)
    bio = models.TextField(blank=True)
    image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    skills_offered = models.ManyToManyField('Skill', related_name='offered_by', blank=True)
    skills_wanted = models.ManyToManyField('Skill', related_name='wanted_by', blank=True)

    def __str__(self):
        return self.name

class Skill(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name

class Rating(models.Model):
    rated_user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='ratings_received')
    rater = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratings_given')
    score = models.PositiveSmallIntegerField()
    review = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.rater} -> {self.rated_user}: {self.score}"
