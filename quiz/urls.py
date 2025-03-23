"""quizaholic URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from quiz import views
from django.contrib import admin


app_name = 'quiz'

urlpatterns = [
    path('', views.index, name = 'index'),
    path('admin/', admin.site.urls),
    path('index/', views.index, name='index'),
    path('categories/', views.categories, name = 'categories'),
    path('categories/<slug:category_name>/leaderboard', views.leaderboard, name = 'leaderboard'),
    path('categories/<slug:category_name>/',views.category, name ='category' ),
    path('register/',views.register, name = 'register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('upload-profile-picture/', views.upload_profile_picture, name='upload_profile_picture'),
    path('profile/', views.profile, name='profile'),
    path('add_category/', views.add_category, name='add_category'),
    path('<slug:category_name_slug>/add_question/', views.add_question, name='add_question'),
]
