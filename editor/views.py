from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from core.models import HomepageContent, Feature, Testimonial
from django.contrib.auth.decorators import login_required, user_passes_test
import json

@login_required
@user_passes_test(lambda u: u.is_staff)
def live_editor(request):
    """
    Sweet and professional dual-pane live editor UI.
    Allows real-time preview of landing page content changes.
    """
    homepage = HomepageContent.objects.first()
    
    # Auto-initialize if empty
    if not homepage:
        homepage = HomepageContent.objects.create(
            title="Unlock New Skills Without Spending a Penny",
            subtitle="The world's most innovative skill-swap platform.",
            cta_text="Join the Exchange"
        )
    
    if Feature.objects.count() == 0:
        Feature.objects.create(title="Build Portfolio", description="Showcase your skills.", icon_class="bi-person-badge", order=0)
        Feature.objects.create(title="Swap Skills", description="Connect with peers.", icon_class="bi-lightning-charge", order=1)
    
    features = Feature.objects.all().order_by('order')
    testimonials = Testimonial.objects.all()

    context = {
        'homepage': homepage,
        'features': features,
        'testimonials': testimonials,
    }
    return render(request, 'editor/live_editor.html', context)

@login_required
@user_passes_test(lambda u: u.is_staff)
def save_content(request):
    """
    Secure API endpoint to save site content changes from the live editor.
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            # Update Homepage
            homepage = HomepageContent.objects.first()
            if homepage:
                homepage.title = data.get('title', homepage.title)
                homepage.subtitle = data.get('subtitle', homepage.subtitle)
                homepage.cta_text = data.get('cta_text', homepage.cta_text)
                homepage.save()
            
            # Update Features
            incoming_feat_ids = []
            for feat_data in data.get('features', []):
                fid = feat_data.get('id')
                if fid and not str(fid).startswith('temp-'):
                    Feature.objects.filter(id=fid).update(
                        title=feat_data.get('title'),
                        description=feat_data.get('description'),
                        icon_class=feat_data.get('icon_class', 'bi-star')
                    )
                    incoming_feat_ids.append(int(fid))
                else:
                    new_feat = Feature.objects.create(
                        title=feat_data.get('title'),
                        description=feat_data.get('description'),
                        icon_class=feat_data.get('icon_class', 'bi-star'),
                        order=0
                    )
                    incoming_feat_ids.append(new_feat.id)
            
            # Delete features not in incoming data
            Feature.objects.exclude(id__in=incoming_feat_ids).delete()
            
            # Update Testimonials
            incoming_test_ids = []
            for t_data in data.get('testimonials', []):
                tid = t_data.get('id')
                if tid and not str(tid).startswith('temp-'):
                    Testimonial.objects.filter(id=tid).update(
                        name=t_data.get('name'),
                        feedback=t_data.get('feedback')
                    )
                    incoming_test_ids.append(int(tid))
                else:
                    new_t = Testimonial.objects.create(
                        name=t_data.get('name'),
                        feedback=t_data.get('feedback'),
                        rating=5
                    )
                    incoming_test_ids.append(new_t.id)
            
            # Delete testimonials not in incoming data
            Testimonial.objects.exclude(id__in=incoming_test_ids).delete()

            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid Method'}, status=405)
