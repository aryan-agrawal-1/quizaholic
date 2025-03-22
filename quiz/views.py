from django.shortcuts import render, redirect
from .forms import *
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponse
from django.urls import reverse
from .models import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required


def index(request):
    return render(request, 'quiz/index.html')

def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST, request.FILES)

        if user_form.is_valid() and profile_form.is_valid():

            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'profile_picture' in request.FILES:
                profile.profile_picture = request.FILES['profile_picture']
            profile.streak = 0; 
            profile.save()
            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request, 'quiz/register.html', {'user_form': user_form, 'profile_form': profile_form, 'registered': registered})


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
            print(f"Invalid logsein details: {username}, {password}")
            return HttpResponse("Invalid login details supplied.")
    else: 
        return render(request, 'quiz/login.html')
    
    
@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('quiz:index'))

#are we going to remove this
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
    return render(request, 'quiz/changepfp.html', {'form': form})

@login_required
def profile(request):
    categories = Category.objects.filter(created_by = request.user)
    return render(request, 'quiz/profile.html', {categories: categories})

@login_required
def add_category(request):
    form = AddCategoryForm()

    if request.method == 'POST':
        form = AddCategoryForm(request.POST, request.FILES)
        
        if form.is_valid():
            category = form.save(user = request.user)
            return redirect(reverse('quiz:add_question', kwargs={'category_name_slug': category.slug}))
        else:
            print(form.errors)
    
    return render(request, 'quiz/add_category.html', {'form': form })

@login_required
def add_question(request, category_name_slug):
    try:
        category = Category.objects.get(slug = category_name_slug)
    except Category.DoesNotExist:
        category = None
    
    if category == None:
        return redirect('/quiz/')
    
    form = AddQuestionForm()

    if request.method == 'POST':
        form = AddQuestionForm(request.POST)

        if form.is_valid():
            question = Question.objects.create(
                category=category,
                question_text=form.cleaned_data['question_text'],
                difficulty=form.cleaned_data['difficulty']
            )

            Answer.objects.create(
                question=question,
                answer_text=form.cleaned_data['option1'],
                is_correct=True
            )

            Answer.objects.create(
                question=question,
                answer_text=form.cleaned_data['option2'],
                is_correct=False
            )

            Answer.objects.create(
                question=question,
                answer_text=form.cleaned_data['option3'],
                is_correct=False
            )

            Answer.objects.create(
                question=question,
                answer_text=form.cleaned_data['option4'],
                is_correct=False
            )

            return redirect('quiz:add_question', category_name_slug=category_name_slug)
        else:
            print(form.errors)

    return render(request, 'quiz/add_question.html', {'form': form, 'category': category})
