from django.shortcuts import render, redirect
from .models import *

# Create your views here.

def profile(request):
    categories = Category.objects.filter(created_by = request.user)
    return render(request, 'quiz/profile.html', {categories: categories})

