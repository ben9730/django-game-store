from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from .forms import ProfileForm
from django.contrib.auth import update_session_auth_hash
from .models import UserGame

User = get_user_model()

def logout_view(request):
    logout(request)
    return redirect('games:game_list')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('games:game_list')
        else:
            messages.error(request, 'Invalid username or password')
            
    return render(request, 'users/login.html')

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        
        if password1 != password2:
            messages.error(request, 'Passwords do not match')
            return redirect('users:register')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return redirect('users:register')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists')
            return redirect('users:register')
        
        user = User.objects.create_user(username=username, email=email, password=password1)
        login(request, user)
        return redirect('games:game_list')
    
    return render(request, 'users/register.html')

@login_required
def profile(request):
    if request.method == 'POST':
        # Handle email change
        email_form = ProfileForm(request.POST, instance=request.user)
        if email_form.is_valid():
            email_form.save()
            messages.success(request, 'Your email was successfully updated!')
            return redirect('users:profile')
        
        # Handle password change
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('users:profile')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
        email_form = ProfileForm(instance=request.user)
    
    context = {
        'form': form,
        'email_form': email_form,
        'user': request.user
    }
    return render(request, 'users/profile.html', context)

@login_required
def subscription(request):
    return render(request, 'users/subscription.html')

@login_required
def library(request):
    user_games = UserGame.objects.filter(user__username=request.user.username)
    context = {
        'user_games': user_games,
        'user': request.user
    }
    return render(request, 'users/library.html', context)
