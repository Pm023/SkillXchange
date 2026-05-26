from django.db import models

class HomepageContent(models.Model):
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=300, blank=True)
    cta_text = models.CharField(max_length=100, blank=True)
    cta_url = models.URLField(blank=True)
    hero_image = models.ImageField(upload_to='hero/', blank=True, null=True)

    def __str__(self):
        return self.title

class Feature(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField()
    icon_class = models.CharField(max_length=100, help_text='Bootstrap icon class, e.g., bi-gear')
    order = models.IntegerField(default=0)

    def __str__(self):
        return self.title

class Testimonial(models.Model):
    name = models.CharField(max_length=150)
    feedback = models.TextField()
    rating = models.PositiveSmallIntegerField()
    avatar = models.ImageField(upload_to='testimonials/', blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.rating})"
