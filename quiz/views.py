from django.shortcuts import render, get_object_or_404
from quiz.models import Category, Question, GameSession, Answer
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from .models import *
from django.contrib.auth.decorators import login_required
from .forms import *
from random import choice

def index(request):
    return render(request, 'quiz/index.html',  )

#lists all the different catgeories avaliable
def categories(request):
    categories = Category.objects.all()
    print(categories)
    context_dict={}
    context_dict['categories'] = categories
    return render(request, 'quiz/categories.html', context = context_dict)

#shows catgeory selected and all the quizzes in that category aswell as options to see different modes and leaderboard
def category(request, category_slug):
    context_dict = {}   
    category = get_object_or_404(Category,slug=category_slug)
    questions = Question.objects.filter(category=category)
    print(f"Questions for {category}: {questions}")
    
    modes = ['learn', 'normal', 'timed']
    first_question = questions.first()
    context_dict['category'] = category
    context_dict['questions'] = questions
    context_dict['mode'] = modes
    context_dict['first_question'] = first_question.id if first_question else None
    return render(request, 'quiz/category.html', context = context_dict)

def fetch_question(request, category_slug, mode, question_id): 
    context_dict = {}
    category = get_object_or_404(Category, slug=category_slug)
    question_text = get_object_or_404(Question, category = category, id = question_id)
    answers = question_text.get_answer()
    is_wrong = False
    mode_templates = { 'learn': 'quiz/learn.html', 'normal': 'quiz/play.html', 'timed':'quiz/timed.html'}
    template = mode_templates.get(mode,'quiz/play.html')
    form = AnswerForm(answers = answers)
    value = question_text.score

    #if request.user.is_authenticated:
     #  user = User.objects.get(id=request.user.id)
    #else:
    #    user=None 
    #game_session, created = GameSession.objects.get_or_create(user=user, category=category, mode=mode)

    if request.method == "POST":
        form = AnswerForm(data = request.POST, answers = answers)
        if form.is_valid():
            selected_answer = form.cleaned_data['answers']
            is_correct = False 
            for a in answers:
                if a['answer_text'] == selected_answer:
                    if a['is_correct']:
                        is_correct = True
                        request.session['score'] = request.session.get('score',0) + question_text.score
                        #game_session.score += question_text.score
                        #game_session.save()
                        break
                     
            if not is_correct and mode == 'normal':
                is_wrong = True
                return redirect('quiz:finish_view')    
        question_id = Question.objects.filter(category=category).values_list('id', flat=True)
        next_question= Question.objects.get(id=choice(question_id))
    
        if next_question:
            return redirect( 'quiz:fetch_question', category_slug = category_slug, mode = mode, question_id = next_question.id )
        else:
            return redirect('quiz:category', category_slug = category_slug)
        
    context_dict['category'] = category
    context_dict['question'] = question_text
    context_dict['answers'] = answers
    context_dict['mode'] = mode 
    context_dict['value'] = value
    context_dict[ 'is_wrong'] = is_wrong
    return render(request, template, context = context_dict)

def finish_view(request):
    #user = request.user if request.user.is_authenticated else None
    #game_session = GameSession.objects.filter(user=user).order_by('-created_at').first()

    #score = game_session.score if game_session else 0    
    return render(request, 'quiz/finishplay.html')    


def leaderboard(request ,category_slug):
    context_dict = {} 
    category = get_object_or_404(Category, slug = category_slug)
    leaderboard_entry_normal = GameSession.objects.filter(mode= "normal", category=category).order_by("-score")[:10]
    leaderboard_entry_timed = GameSession.objects.filter(mode = "timed", category=category ).order_by("-score")[:10]

    context_dict['category'] = category
    context_dict['normal'] = leaderboard_entry_normal
    context_dict['timed'] = leaderboard_entry_timed

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

       
    
