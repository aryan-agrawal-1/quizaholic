from django.shortcuts import render, redirect
from quiz.forms import UserForm, UserProfileForm
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponse
from django.urls import reverse
from .models import UserProfile
from django.contrib import messages
from django.contrib.auth.decorators import login_required


def index(request):
    return render(request, 'quiz/index.html')

def index(request):
    return render(request, 'quiz/index.html')

def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()

            user.set_password(user.password)
            user.save()

            UserProfile.objects.create(user=user)
            registered = True
        else:
            print(user_form.errors)

    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request, 'quiz/register.html', context= {'user_form' : user_form, 'profile_form' : profile_form, 'registered' : registered})


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return redirect(reverse('quiz:index')) 
            else:
                return HttpResponse("Your account is disabled.")  
        else:
            print(f"Invalid login details: {username}, {password}")
            return HttpResponse("Invalid login details.")
    else: 
        return render(request, 'quiz/login.html')
    
    
@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('quiz:index'))

@login_required
def restricted(request):
    return HttpResponse("Since you're logged in, you can see this text!")

@login_required
def upload_profile_picture(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile picture updated successfully.")
            return redirect('quiz:profile')

    else:
        form = UserProfileForm(instance=user_profile)
    return render(request, 'quiz/profile.html', {'form': form})