from django.shortcuts import render, redirect
from quiz.forms import UserForm, UserProfileForm, CustomUserCreationForm
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponse
from django.urls import reverse
from .models import UserProfile
from django.contrib import messages
from django.contrib.auth.decorators import login_required


def index(request):
    return render(request, 'quiz/index.html')


def register(request):
    registered = False
    if request.method == 'POST':
        user_form = CustomUserCreationForm(request.POST)
        profile_form = UserProfileForm(request.POST, request.FILES)

        if user_form.is_valid() and profile_form.is_valid():

            user = user_form.save()
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'profile_picture' in request.FILES:
                profile.profile_picture = request.FILES['profile_picture']

            profile.streak = 0; 
            profile.save()
            registered = True

            messages.success(request, "Registration successful! You can now log in :)")
            return redirect('quiz:login')
        else:
            for form in [user_form, profile_form]:
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f"{field.capitalize()}: {error}")
    else:
        user_form = CustomUserCreationForm()
        profile_form = UserProfileForm()

    return render(request, 'registration/register.html', {'user_form': user_form, 'profile_form': profile_form, 'registered': registered})


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        remember_me = request.POST.get ('remember_me')

        if user:
            if user.is_active:
                login(request, user)

                if remember_me:
                    request.session.set_expiry(1209600) #equivalent to 2 weeks
                else: 
                    request.session.set_expiry(0)
                return redirect(reverse('quiz:index')) 
            else:
                messages.error(request, "Your account is disabled.")
        else:
            messages.error(request, "Invalid username or password.")
    else: 
        return render(request, 'registration/login.html')
    
    
@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('quiz:index'))


@login_required
def upload_profile_picture(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST' and 'profile_picture' in request.FILES:
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            if user_profile.profile_picture:
                user_profile.profile_picture.delete()

            user_profile.profile_picture = request.FILES['profile_picture']
            UserProfileForm.save()
            messages.success(request, "Profile picture updated successfully.")
            return redirect('quiz:profile')

    return render(request, 'quiz/profile.html', {'form': form})