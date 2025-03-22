from django.contrib import admin
from .models import User, Category, Question, Answer, GameSession,Quiz,Question


class QuizAdmin(admin.ModelAdmin):
    list_display = ('category', 'question_text')

admin.site.register(Question,QuizAdmin)