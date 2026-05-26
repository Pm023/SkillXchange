from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Profile, Skill, Rating
from django.db.models import Q

@login_required
def profile_view(request):
    profile = get_object_or_404(Profile, user=request.user)
    context = {'profile': profile}
    return render(request, 'profiles/profile.html', context)

def skill_search(request):
    query = request.GET.get('q', '')
    filter_type = request.GET.get('type', 'all') # 'all', 'offering', 'seeking'
    
    profiles = Profile.objects.all().select_related('user').prefetch_related('skills_offered', 'skills_wanted')

    if query:
        q_filter = Q(name__icontains=query) | Q(bio__icontains=query)
        
        if filter_type == 'offering':
            q_filter |= Q(skills_offered__name__icontains=query)
        elif filter_type == 'seeking':
            q_filter |= Q(skills_wanted__name__icontains=query)
        else:
            # Search both
            q_filter |= Q(skills_offered__name__icontains=query) | Q(skills_wanted__name__icontains=query)
            
        profiles = profiles.filter(q_filter).distinct()
    
    context = {
        'profiles': profiles,
        'query': query,
        'filter_type': filter_type
    }
    return render(request, 'profiles/search.html', context)

@login_required
def view_public_profile(request, username):
    profile = get_object_or_404(Profile, user__username=username)
    context = {'profile': profile}
    return render(request, 'profiles/profile.html', context)

@login_required
def edit_skills(request):
    profile = get_object_or_404(Profile, user=request.user)
    if request.method == 'POST':
        offered_names = [s.strip() for s in request.POST.get('offered', '').split(',') if s.strip()]
        wanted_names = [s.strip() for s in request.POST.get('wanted', '').split(',') if s.strip()]
        
        # Helper to get or create skills
        def get_skills_list(names):
            skill_objs = []
            for name in names:
                skill, _ = Skill.objects.get_or_create(name=name)
                skill_objs.append(skill)
            return skill_objs

        profile.skills_offered.set(get_skills_list(offered_names))
        profile.skills_wanted.set(get_skills_list(wanted_names))
        profile.save()
        return redirect('profile')
    
    offered_str = ", ".join([s.name for s in profile.skills_offered.all()])
    wanted_str = ", ".join([s.name for s in profile.skills_wanted.all()])
    return render(request, 'profiles/edit_skills.html', {
        'offered': offered_str,
        'wanted': wanted_str
    })
