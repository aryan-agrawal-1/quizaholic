from django.contrib import admin
from .models import User, Category, Question, Answer, GameSession

admin.site.register(User)
admin.site.register(Category)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(GameSession)
