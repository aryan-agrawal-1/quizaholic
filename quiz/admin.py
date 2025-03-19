from django.contrib import admin
from .models import UserProfile, Category, Question, Answer, GameSession

admin.site.register(UserProfile)
admin.site.register(Category)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(GameSession)
