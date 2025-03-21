from django.urls import path, include
from quiz import views

app_name = 'quiz'

urlpatterns = [
    path('profile/', views.profile, name='profile'),
    path('add_category/', views.add_category, name='add_category'),
    path('<slug:category_name_slug>/add_question', views.add_question, name='add_question'),
]
