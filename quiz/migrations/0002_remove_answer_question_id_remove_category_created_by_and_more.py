# Generated by Django 5.0.3 on 2025-03-21 14:03

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("quiz", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name="answer",
            name="question_id",
        ),
        migrations.RemoveField(
            model_name="category",
            name="created_by",
        ),
        migrations.RemoveField(
            model_name="gamesession",
            name="category_id",
        ),
        migrations.RemoveField(
            model_name="gamesession",
            name="user_id",
        ),
        migrations.RemoveField(
            model_name="question",
            name="category_id",
        ),
        migrations.AddField(
            model_name="answer",
            name="question",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="quiz.question",
            ),
        ),
        migrations.AddField(
            model_name="category",
            name="slug",
            field=models.SlugField(blank=True, max_length=255, unique=True),
        ),
        migrations.AddField(
            model_name="gamesession",
            name="category",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="quiz.category",
            ),
        ),
        migrations.AddField(
            model_name="gamesession",
            name="user",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="question",
            name="category",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="quiz.category",
            ),
        ),
        migrations.AddField(
            model_name="userprofile",
            name="image",
            field=models.ImageField(blank=True, null=True, upload_to="user_images"),
        ),
        migrations.AlterField(
            model_name="answer",
            name="is_correct",
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name="category",
            name="name",
            field=models.CharField(max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name="gamesession",
            name="mode",
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name="gamesession",
            name="score",
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name="question",
            name="difficulty",
            field=models.CharField(
                choices=[("easy", "Easy"), ("medium", "Medium"), ("hard", "Hard")],
                max_length=10,
            ),
        ),
        migrations.AlterField(
            model_name="question",
            name="score",
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name="userprofile",
            name="streak",
            field=models.PositiveIntegerField(default=0),
        ),
    ]
