from django.shortcuts import render, get_object_or_404
from models import Category, Quiz, Question, LeaderboardEntry
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
def category(request):
    context_dict = {}   
    category = get_object_or_404(Category,category)
    context_dict['category'] = category
    return render(request, 'quiz/category.html', context = context_dict)


def leaderboard(request):
    context_dict = {} 
    category = get_object_or_404(Category, category)
    leaderboard_entry_basic = LeaderboardEntry.objects.filter(mode= "basic", category=category)
    leaderboard_entry_timed = LeaderboardEntry.objects.filter(mode = "timed", category=category )

    context_dict['category'] = category
    context_dict['basic'] = leaderboard_entry_basic
    context_dict['timed'] = leaderboard_entry_timed

    return render(request, 'quiz/leaderboards.html', context = context_dict)


