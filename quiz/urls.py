from django.urls import path, include
from quiz import views 


app_name = 'quiz'

urlpatterns = [
    path('', views.index, name = 'index'),
    path('categories/', views.categories, name = 'categories'),
    path('categories/<slug:category_name>/',views.category, name ='category' ),
    path('categories/<slug:category_name>/leaderboard', views.leaderboard, name = 'leaderboard'),
    path('categories/<slug:category_name>/<str:mode>/question/<int:question_id>/', views.fetch_question, name = 'fetch_question')

]


urlpatterns = [
    path('profile/', views.profile, name='profile'),
    path('add_category/', views.add_category, name='add_category'),
    path('<slug:category_name_slug>/add_question', views.add_question, name='add_question'),
]
