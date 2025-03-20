from django.db import models

class User(models.Model):
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
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    question_text = models.CharField(max_length=999)
    score = models.IntegerField(default=0)

    def __str__(self):
        return self.question_text[:50]


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
