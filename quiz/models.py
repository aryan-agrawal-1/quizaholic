from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=255)
    created_by = models.ForeignKey(User, on_delete= models.CASCADE, related_name='created_by')

class GameSession(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='game_of')
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='game_category')

    MODE_CHOICES = [
        ('basic', 'Basic'),
        ('timed', 'Timed'),
    ]

    mode = models.CharField(max_length=50, choices=MODE_CHOICES)
    score = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

class Question(models.Model):
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='for_category')
    question_text = models.CharField(max_length=999)

    DIFFICULTY_CHOICES = [
        ('hard', 'Hard'),
        ('medium', 'Medium'),
        ('easy', 'Easy'),
    ]

    difficulty = models.CharField(max_length=30, choices=DIFFICULTY_CHOICES)
    score = models.IntegerField()

class Answer(models.Model):
    question_id = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answer_of')
    answer_text = models.CharField(max_length=999)
    is_correct = models.BooleanField(default=True)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    streak = models.IntegerField()
