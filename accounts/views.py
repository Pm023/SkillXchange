from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from profiles.models import Profile
from django.views.decorators.csrf import csrf_protect

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create the Profile for the NEW user
            Profile.objects.create(user=user, name=user.username)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'accounts/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    """
    Log out the user. If they were staff, redirect to the secure admin login.
    Otherwise, redirect to the homepage.
    """
    is_staff = request.user.is_staff
    if request.method == 'POST':
        logout(request)
        if is_staff:
            return redirect('admin_login')
        return redirect('home')
    return redirect('home')

@csrf_protect
def admin_login_view(request):
    """
    A dedicated, professional login portal for administrators.
    """
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('admin_dashboard')
        
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user.is_staff:
                login(request, user)
                return redirect('admin_dashboard')
            else:
                return render(request, 'accounts/admin_login.html', {
                    'form': form, 
                    'error': "Access Denied: Administrator credentials required."
                })
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/admin_login.html', {'form': form})

from django.contrib.auth.decorators import login_required, user_passes_test

@login_required
@user_passes_test(lambda u: u.is_staff, login_url='admin_login')
def admin_dashboard(request):
    """
    Professional Administrative Server Dashboard.
    Provides advanced access to CMS and system settings.
    """
    return render(request, 'accounts/admin_dashboard.html')
