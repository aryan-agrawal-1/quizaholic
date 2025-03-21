from django.contrib import admin
from .models import User, Category, Question, Answer, GameSession,Quiz

admin.site.register(User)
admin.site.register(Category)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(GameSession)
admin.site.register(Quiz,Question)

class QuizAdmin(admin.ModelAdmin):
    list_display = ('category, question')

class QuestionAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('question',)}

admin.site.register(QuizAdmin,QuestionAdmin)