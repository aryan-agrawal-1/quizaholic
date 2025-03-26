from django.db import models
import random
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from datetime import datetime, timedelta

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    streak = models.PositiveIntegerField(default=0)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True, default='profile_pics/default.png')

    def __str__(self):
        return self.user.username


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    category_image = models.ImageField(upload_to='category_imgs', blank=True, default='category_imgs/default.jpg')
    created_by = models.ForeignKey(User,on_delete=models.CASCADE, null=True)

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

    def save(self, *args, **kwargs):
        # Get user's latest game session before this one
        
        last_session = GameSession.objects.filter(user=self.user).order_by('-created_at').first()
        
        if last_session:
            # Check if last session was yesterday
            yesterday = datetime.now().date() - timedelta(days=1)
            if last_session.created_at.date() == yesterday:
                # Increment streak if played yesterday
                self.user.userprofile.streak += 1
            else:
                # Reset streak if not played yesterday
                self.user.userprofile.streak = 1
        else:
            # First game session
            self.user.userprofile.streak = 1
            
        self.user.userprofile.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.category.name} ({self.mode}) - {self.score}"

