from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_safe, require_POST, require_http_methods
from django.contrib.auth import get_user_model
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm

from .forms import CustomUserCreationForm

User = get_user_model()

# Create your views here.
@require_http_methods(['GET', 'POST'])
def signup(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = CustomUserCreationForm(request.POST)
            if form.is_valid():
                user = form.save()
                auth_login(request, user)
                return redirect('community:index')
        else:
            form = CustomUserCreationForm()

        context = {'form': form, }
        return render(request, 'accounts/signup.html', context=context)
    else:
        return redirect('community:index')

@require_http_methods(['GET', 'POST'])
def login(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = AuthenticationForm(request, request.POST)
            if form.is_valid():
                user = form.get_user()
                auth_login(request, user)
                return redirect(request.GET.get('next') or 'community:index')
        else:
            form = AuthenticationForm()
        
        context = {'form': form, }
        return render(request, 'accounts/login.html', context=context)
    else:
        return redirect('community:index')

def logout(request):
    auth_logout(request)
    return redirect('community:index')


@require_safe
def profile(request, username):
    profile = get_object_or_404(User, username=username)

    context = {
        'profile': profile, 

    }
    return render(request, 'accounts/profile.html', context)

def follow(request, username):
    profile = get_object_or_404(get_user_model(), username=username)
    user = request.user
    if profile != user:
        if profile.followers.filter(pk=user.pk).exists():  
            profile.followers.remove(user)
        else:
            profile.followers.add(user)
    return redirect('accounts:profile', profile.username)