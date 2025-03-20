from django.shortcuts import render, get_object_or_404
from models import Category, Quiz, Question, LeaderboardEntry, Answer
from django.shortcuts import render, redirect
from django.http import HttpResponse

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
    answers = Answer.objects.filter(Answer, question=question_text)

    mode_templates = { 'learn': 'learn.html', 'play': 'play.html', 'timed':'timed.html'}
    template = mode_templates.get(mode,'play.html')
    context_dict['category'] = category
    context_dict['question'] = question_text
    context_dict['answers'] = answers
    context_dict['mode'] = mode 
    return render(request, template, context = context_dict)


@login_required
def delete_question(request, category_slug, question_id):


@login_required
def delete_category(request, category_slug):

def leaderboard(request):
    context_dict = {} 
    category = get_object_or_404(Category, category)
    leaderboard_entry_basic = LeaderboardEntry.objects.filter(mode= "basic", category=category)
    leaderboard_entry_timed = LeaderboardEntry.objects.filter(mode = "timed", category=category )

    context_dict['category'] = category
    context_dict['basic'] = leaderboard_entry_basic
    context_dict['timed'] = leaderboard_entry_timed

    return render(request, 'quiz/leaderboards.html', context = context_dict)


