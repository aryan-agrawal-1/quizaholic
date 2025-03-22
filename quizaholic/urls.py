from django.contrib import admin
from django.urls import path
from django.urls import include 
from quiz import views 
from django.conf import settings 

urlpatterns = [
    path('quiz/', include('quiz.urls')),
    path('admin/', admin.site.urls),
    path('quiz/', include('quiz.urls')),
    
]
