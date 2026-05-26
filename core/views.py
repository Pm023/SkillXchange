from django.shortcuts import render
from .models import HomepageContent, Feature, Testimonial

def home(request):
    """
    Serve the standard Django-managed Homepage.
    """
    homepage = HomepageContent.objects.first()
    features = Feature.objects.all().order_by('order')
    testimonials = Testimonial.objects.all()
    
    context = {
        'homepage': homepage,
        'features': features,
        'testimonials': testimonials,
    }
    return render(request, 'core/home.html', context)

def faq_view(request):
    return render(request, 'core/faq.html')

def community_view(request):
    return render(request, 'core/community.html')

def privacy_view(request):
    return render(request, 'core/privacy.html')

def terms_view(request):
    return render(request, 'core/terms.html')
