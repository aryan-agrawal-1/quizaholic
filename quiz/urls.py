from django.urls import path, include
from quiz import views
from django.contrib import admin


app_name = 'quiz'

urlpatterns = [

    path('', views.index, name='index'),
    path('index/', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('admin/', admin.site.urls),
    path('categories/', views.categories, name = 'categories'),
    path('categories/<slug:category_slug>/',views.category, name ='category' ),
    path('categories/<slug:category_slug>/leaderboard', views.leaderboard, name = 'leaderboard'),
    path('categories/<slug:category_slug>/<str:mode>/<int:question_id>/', views.fetch_question, name = 'fetch_question'),
    path('register/',views.register, name = 'register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('upload-profile-picture/', views.upload_profile_picture, name='upload_profile_picture'),
    path("accounts/", include("django.contrib.auth.urls")),
    path('profile/', views.profile, name='profile'),
    path('add_category/', views.add_category, name='add_category'),
    path('<slug:category_name_slug>/add_question/', views.add_question, name='add_question'),
    path('quiz/finish/', views.finish_view, name="finish_view"),

]
