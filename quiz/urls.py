from django.urls import path 
from quiz import views 

app_name = 'rango'

urlpatterns = [
    path('', views.index, name = 'index'),
    path('categories/', views.categories, name = 'categories'),
    path('categories/category/',views.category, name ='category' ),
    path('category_page/<slug:quiz_slug/quiz_mode', views.quiz_mode, name = 'quiz_mode'),
    path('categories/category/leaderboard', views.leaderboard, name = 'leaderboard')

]