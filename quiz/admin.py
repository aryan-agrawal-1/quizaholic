from django.contrib import admin
from .models import UserProfile, Category, Question, Answer, GameSession,Quiz,Question


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('category', 'question_text')

admin.site.register(UserProfile)
admin.site.register(Category)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer)
admin.site.register(GameSession)
admin.site.register(Quiz)