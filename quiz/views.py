from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponse
from django.urls import reverse
from .models import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required


def index(request):
    return render(request, 'quiz/index.html')

#lists all the different catgeories avaliable
def categories(request):
    categories = Category.objects.all()
    context_dict={}
    context_dict['categories'] = categories
    return render(request, 'quiz/categories.html', context = context_dict)

#shows catgeory selected and all the quizzes in that category aswell as options to see different modes and leaderboard
def category(request,category_slug):
    context_dict = {}   
    category = get_object_or_404(Category,slug=category_slug)
    questions = Question.objects.filter(category=category) 
    first_question = questions.first()  # Get the first question


    context_dict['category'] = category
    context_dict['questions'] = questions
    context_dict['first_question'] = first_question

    return render(request, 'quiz/category.html', context = context_dict)

def leaderboard(request, category_slug):
    context_dict = {} 
    category = get_object_or_404(Category, slug=category_slug)
    leaderboard_entry_normal = GameSession.objects.filter(mode= "normal", category=category)
    leaderboard_entry_timed = GameSession.objects.filter(mode = "timed", category=category )

    scores = GameSession.objects.filter(category=category).order_by("-score")

    user_score_normal = None
    user_score_timed = None

    if request.user.is_authenticated:
        user_score_normal  = GameSession.objects.filter(mode = "normal", category=category , user = request.user )
        user_score_timed = GameSession.objects.filter(mode = "timed", category=category , user = request.user )


    context_dict['category'] = category
    context_dict['normal'] = leaderboard_entry_normal
    context_dict['timed'] = leaderboard_entry_timed
    context_dict['score'] = scores
    context_dict['user_score_normal'] = user_score_normal
    context_dict['user_score_timed'] = user_score_timed

    return render(request, 'quiz/leaderboards.html', context = context_dict)


# def fetch_question(request, category_slug, mode, question_id): 
#     context_dict = {}
#     category = get_object_or_404(Category, slug=category_slug)
#     question_text = get_object_or_404(Question, category = category, id = question_id)
#     answers = question_text.get_answer()

#     mode_templates = { 'learn': 'quiz/learn.html', 'normal': 'quiz/play.html', 'timed':'quiz/timed.html'}
#     template = mode_templates.get(mode,'quiz/play.html')
#     form = AnswerForm(answers=answers)
#     if request.method == "POST":
#         form = AnswerForm(request.POST, answers = answers)
#         if form.is_valid():
#             selected_answer = form.cleaned_data['answer']
#             for a in answers:
#                 if a['is_correct'] == True:
#                     request.session['score'] = request.session.get('score',0) + question_text.score
#                     break
        
#         next_question = Question.objects.filter(category = category).first()

#         if next_question:
#             return redirect( 'quiz:fetch_question', category_slug = category_slug, mode = mode, question_id = next_question.id )
#         else:
#             return redirect('quiz:category', category_slug = category_slug)
        
#     context_dict['category'] = category
#     context_dict['question'] = question_text
#     context_dict['answers'] = answers
#     context_dict['mode'] = mode 
#     return render(request, template, context = context_dict)


def fetch_question(request, category_slug, mode, question_id):
    context_dict = {}
    category = get_object_or_404(Category, slug=category_slug)
    question_text = get_object_or_404(Question, category=category, id=question_id)
    answers = question_text.get_answer()
    request.session.setdefault('score', 0)

    mode_templates = {'learn': 'quiz/learn.html', 'normal': 'quiz/play.html', 'timed': 'quiz/timed.html'}
    template = mode_templates.get(mode, 'quiz/play.html')

    form = AnswerForm(answers=answers)

    if request.method == "POST":
        form = AnswerForm(request.POST, answers=answers)
        if form.is_valid():
            selected_answer = form.cleaned_data['answer']
            correct_answer_found = False
            for a in answers:
                if a['is_correct']:
                    if a['id'] == int(selected_answer):
                        request.session['score'] += question_text.score
                        messages.success(request, "Correct! You've earned points.")
                    else:
                        messages.error(request, "Incorrect answer. Try the next question.")
                    correct_answer_found = True
                    break

        next_question = Question.objects.filter(category=category, id__gt=question_id).order_by('id').first()

        if next_question:
            return redirect('quiz:fetch_question', category_slug=category_slug, mode=mode, question_id=next_question.id)
        else:
            messages.info(request, f"You've completed the quiz! Final score: {request.session['score']}")
            return redirect('quiz:category', category_slug=category_slug)

    context_dict['category'] = category
    context_dict['question'] = question_text
    context_dict['answers'] = answers
    context_dict['mode'] = mode
    context_dict['form'] = form
    return render(request, template, context=context_dict)


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
    return render(request, 'quiz/profile.html', {'categories': categories})

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
