from django.urls import path 
from quiz import views 

app_name = 'rango'

urlpatterns = [
    path('', views.index, name = 'index'),
    path('categories/', views.categories, name = 'categories'),
    path('categories/<slug:category_name>/',views.category, name ='category' ),
    path('categories/<slug:category_name>/leaderboard', views.leaderboard, name = 'leaderboard'),
    path('categories/<slug:category_name>/<str:mode>/question/<int:question_id>/', views.fetch_question, name = 'fetch_question')

]