from django.urls import path, include
from quiz import views 


app_name = 'quiz'

urlpatterns = [
    path('', views.index, name = 'index'),
    path('categories/', views.categories, name = 'categories'),
    path('categories/<slug:category_slug>/',views.category, name ='category' ),
    path('categories/<slug:category_slug>/leaderboard', views.leaderboard, name = 'leaderboard'),
    path('categories/<slug:category_slug>/<str:mode>/question/<int:question_id>/', views.fetch_question, name = 'fetch_question'),
    path('profile/', views.profile, name='profile'),
    path('add_category/', views.add_category, name='add_category'),
    path('<slug:category_name_slug>/add_question', views.add_question, name='add_question'),
]
