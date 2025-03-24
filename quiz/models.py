from django.db import models
import random
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User

class User(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    streak = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='user_images', null=True, blank=True)

    def __str__(self):
        return self.username

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class Quiz(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_quizzes')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='quizzes')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.save = slugify(self.name)
        super(Quiz, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class Question(models.Model):
    DIFFICULTY_CHOICES = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ]

    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    question_text = models.CharField(max_length=999)
    score = models.IntegerField(default=0)
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES)

    def __str__(self):
        return self.question_text[:50]
    
    def get_answer(self):
        answers= list(Answer.objects.filter(question = self))
        data = []
        random.shuffle(answers)
        for answer in answers:
            data.append({'answer_text' : answer.answer_text, 'is_correct': answer.is_correct})
        return data

    def save(self, *args, **kwargs):
        if self.difficulty == 'easy':
            self.score = 10
        elif self.difficulty == 'medium':
            self.score = 20
        elif self.difficulty == 'hard':
            self.score = 30
        
        super().save(*args, **kwargs)


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer_text = models.CharField(max_length=999)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.answer_text[:50]
    



class GameSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    mode = models.CharField(max_length=30)
    score = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.category.name} ({self.mode}) - {self.score}"
