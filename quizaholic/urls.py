from django.contrib import admin
from django.urls import path, include
from quiz import views

urlpatterns = [
    path('quiz/', include('quiz.urls')),
    path('admin/', admin.site.urls),
]
