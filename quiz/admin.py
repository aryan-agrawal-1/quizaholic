from django.contrib import admin
from quiz.models import Quiz, Question, Profile

# Register your models here.

class QuizAdmin(admin.ModelAdmin):
    list_display = ('question', 'category', 'url')

class QuestionAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}

admin.site.register(Quiz, QuizAdmin, QuestionAdmin,Profile, Question)