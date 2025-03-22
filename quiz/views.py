from django.shortcuts import render, get_object_or_404
from models import Category, Quiz, Question, GameSession, Answer
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from .models import *
from django.contrib.auth.decorators import login_required
from .forms import *

def index(request):
    return render(request, 'quiz/index.html',  )

#lists all the different catgeories avaliable
def categories(request):
    categories = Category.objects.all()
    context_dict={}
    context_dict['categories'] = categories
    return render(request, 'quiz/categories.html', context = context_dict)

#shows catgeory selected and all the quizzes in that category aswell as options to see different modes and leaderboard
def category(request, category_slug):
    context_dict = {}   
    category = get_object_or_404(Category,slug=category_slug)
    context_dict['category'] = category
    return render(request, 'quiz/category.html', context = context_dict)

def fetch_question(request, category_slug, question_id,mode): 
    context_dict = {}
    category = get_object_or_404(Category, slug=category_slug)
    question_text = get_object_or_404(Question, category = category, id = question_id)
    answers = Question.get_answer()

    mode_templates = { 'learn': 'quiz/learn.html', 'play': 'quiz/play.html', 'timed':'quiz/timed.html'}
    template = mode_templates.get(mode,'quiz/play.html')
    context_dict['category'] = category
    context_dict['question'] = question_text
    context_dict['answers'] = answers
    context_dict['mode'] = mode 
    return render(request, template, context = context_dict)

    
def leaderboard(request):
    context_dict = {} 
    category = get_object_or_404(Category, category)
    leaderboard_entry_normal = GameSession.objects.filter(mode= "normal", category=category)
    leaderboard_entry_timed = GameSession.objects.filter(mode = "timed", category=category )
    scores = GameSession.objects.order_by("-score").all()

    context_dict['category'] = category
    context_dict['normal'] = leaderboard_entry_normal
    context_dict['timed'] = leaderboard_entry_timed
    context_dict['score'] = scores

    return render(request, 'quiz/leaderboards.html', context = context_dict)



@login_required
def profile(request):
    categories = Category.objects.filter(created_by = request.user)
    return render(request, 'quiz/profile.html', {categories: categories})

@login_required
def add_category(request):
    form = AddCategoryForm()

    if request.method == 'POST':
        form = AddCategoryForm(request.POST)

        if form.is_valid():
            category = form.save(commit=True)
            return redirect(reverse('quiz:add_question', kwargs={'category_name_slug': category.slug}))
        else:
            print(form.errors)
    
    return render(request, 'quiz/add_category.html', {'form': form})

@login_required
def add_question(request, category_name_slug):
    try:
        category = Category.objects.get(slug = category_name_slug)
    except Category.DoesNotExist:
        category = None
    
    if category == None:
        return redirect('/quiz/')
    
    form = AddCategoryForm()

    if request.method == 'POST':
        form = AddQuestionForm(request.POST)

        if form.is_valid():
            question = Question(
                category = category,
                question_text = form.cleaned_data['question'],
                difficulty = form.cleaned_data['difficulty']
            )
            question.save()

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

            return redirect(request.path)
        
        else:
            print(form.errors)

    return render(request, 'quiz/add_question.html',  context={'form': form})

       
    
