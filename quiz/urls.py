from django.urls import path, include
from quiz import views

app_name = 'quiz'

urlpatterns = [
    path('', views.index, name='index'),
    path('index/', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('restricted/', views.restricted, name='restricted'),
    path('upload-profile-picture/', views.upload_profile_picture, name='upload_profile_picture'),
    path("accounts/", include("django.contrib.auth.urls")),
]
