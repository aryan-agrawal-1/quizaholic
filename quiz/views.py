from django.shortcuts import render, redirect
from django.urls import reverse
from .models import *
from django.contrib.auth.decorators import login_required
from .forms import *

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

       
    