import random
import html
import time
import requests

from django.core.management.base import BaseCommand
from django.db import transaction

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quizaholic.settings')
django.setup()

from quiz.models import Category, Question, Answer, User, GameSession, UserProfile

BASE_URL = "https://opentdb.com/api.php"
CATEGORY_URL = "https://opentdb.com/api_category.php"

class Command(BaseCommand):

    def handle(self, *args, **options):
        api_categories = self.get_api_categories()
        if not api_categories:
            return

        desired_categories = [
            "Science & Nature",
            "Science: Computers",
            "General Knowledge",
            "Mythology",
            "Sports",
            "Geography",
            "History",
            "Vehicles"
        ]
        selected_categories = [cat for cat in api_categories if cat['name'] in desired_categories]

        for cat in selected_categories:
            category_obj, _ = Category.objects.get_or_create(name=cat['name'])
            for i in range(2):
                params = {
                    'amount': 50,
                    'category': cat['id'],
                    'type': 'multiple',
                }
                response = requests.get(BASE_URL, params=params)
                if response.status_code != 200:
                    print("failed to connect")
                    time.sleep(5)
                    continue
                data = response.json()
                if data.get('response_code') != 0:
                    print("failed")
                    time.sleep(5)
                    continue
                questions = data.get('results', [])
                self.populate_questions(category_obj, questions)
                print("done 1")
                time.sleep(5)
        self.create_demo_users_and_gamesessions()

    def get_api_categories(self):
        response = requests.get(CATEGORY_URL)
        if response.status_code != 200:
            return []
        data = response.json()
        return data.get('trivia_categories', [])

    @transaction.atomic
    def populate_questions(self, category_obj, questions):
        for item in questions:
            question_text = html.unescape(item.get('question'))
            correct_answer = html.unescape(item.get('correct_answer'))
            incorrect_answers = [html.unescape(ans) for ans in item.get('incorrect_answers', [])]
            if Question.objects.filter(category=category_obj, question_text=question_text).exists():
                continue
            question_obj = Question.objects.create(
                category=category_obj,
                question_text=question_text,
                score=0
            )
            Answer.objects.create(
                question=question_obj,
                answer_text=correct_answer,
                is_correct=True
            )
            for ans in incorrect_answers:
                Answer.objects.create(
                    question=question_obj,
                    answer_text=ans,
                    is_correct=False
                )

    def create_demo_users_and_gamesessions(self):
        if User.objects.count() < 30:
            for i in range(1, 31):
                user, created = User.objects.get_or_create(username=f"User{i}")
                UserProfile.objects.get_or_create(user=user, defaults={'streak': random.randint(0, 10)})
        
        categories = list(Category.objects.all())
        modes = ['normal', 'timed']
        
        for profile in UserProfile.objects.all():
            category = random.choice(categories)
            GameSession.objects.create(
                user=profile.user,
                category=category,
                mode=random.choice(modes),
                score=random.randint(0, 1000)
            )

if __name__ == '__main__':
    print('Starting population script may take 1 minute...')
    command = Command()
    command.handle()
