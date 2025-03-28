from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import *
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils import timezone
from datetime import timedelta
from django.conf import settings

class ModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', 
            password='12345'
        )

        self.category = Category.objects.create(
            name='Test Category', 
            created_by=self.user
        )

    # is category created and slug name generated correctly
    def test_category_creation(self):
        self.assertEqual(self.category.name, 'Test Category')
        self.assertEqual(self.category.slug, 'test-category')
        self.assertEqual(self.category.created_by, self.user)

    # are questions being assigned the right points based on difficulty
    def test_question_creation(self):
        question = Question.objects.create(
            category=self.category,
            question_text='Test Question',
            difficulty='easy'
        )
        
        self.assertEqual(question.score, 10)
        self.assertEqual(question.difficulty, 'easy')

        question_medium = Question.objects.create(
            category=self.category,
            question_text='Test Medium Question',
            difficulty='medium'
        )
        self.assertEqual(question_medium.score, 20)

        question_hard = Question.objects.create(
            category=self.category,
            question_text='Test Hard Question',
            difficulty='hard'
        )
        self.assertEqual(question_hard.score, 30)

    # is the model able to correctly identify the correct answers for each question
    def test_answer_creation(self):
        question = Question.objects.create(
            category=self.category,
            question_text='Test Question',
            difficulty='easy'
        )
        
        correct_answer = Answer.objects.create(
            question=question,
            answer_text='Correct Answer',
            is_correct=True
        )
        
        incorrect_answer = Answer.objects.create(
            question=question,
            answer_text='Incorrect Answer',
            is_correct=False
        )
        
        self.assertTrue(correct_answer.is_correct)
        self.assertFalse(incorrect_answer.is_correct)

class UserProfileTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', 
            password='12345'
        )

    # Testing if a user profile gets created
    def test_user_profile_creation(self):
        profile = UserProfile.objects.create(
            user=self.user,
            streak=0
        )
        
        self.assertEqual(profile.user, self.user)
        self.assertEqual(profile.streak, 0)

class GameSessionTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', 
            password='12345'
        )
        UserProfile.objects.create(user=self.user)
        
        self.category = Category.objects.create(name='Test Category')

    # Testing profile streak logic, does it increment each day and does it reset
    def test_game_session_streak(self):
        first_session = GameSession.objects.create(
            user=self.user,
            category=self.category,
            mode='normal',
            score=100
        )
        user_profile = UserProfile.objects.get(user=self.user)
        self.assertEqual(user_profile.streak, 1)

    
class ViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser', 
            password='12345'
        )
        UserProfile.objects.create(user=self.user)

        self.category = Category.objects.create(name='Test Category')
        self.question = Question.objects.create(
            category=self.category,
            question_text='Test Question',
            difficulty='easy'
        )
        Answer.objects.create(
            question=self.question,
            answer_text='Correct Answer',
            is_correct=True
        )
        Answer.objects.create(
            question=self.question,
            answer_text='Wrong Answer 1',
            is_correct=False
        )

    # does logged in user have access to categories page
    def test_categories_view(self):
        response = self.client.get(reverse('quiz:categories'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'quiz/categories.html')

    # can logged in user access the individual category page
    def test_category_view(self):
        response = self.client.get(reverse('quiz:category', kwargs={'category_slug': self.category.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'quiz/category.html')

    # can user log in
    def test_login_view(self):
        response = self.client.post(reverse('quiz:login'), {
            'username': 'testuser',
            'password': '12345'
        })
        self.assertRedirects(response, reverse('quiz:index'))

    # can user register
    def test_register_view(self):
        response = self.client.post(reverse('quiz:register'), {
            'username': 'newuser',
            'password1': 'testpass123',
            'password2': 'testpass123',
        })
        # Check that a new user was created
        self.assertTrue(User.objects.filter(username='newuser').exists())

    # does leaderboard load correctly
    def test_leaderboard_view(self):
        # Create some game sessions for leaderboard
        GameSession.objects.create(
            user=self.user,
            category=self.category,
            mode='normal',
            score=100
        )
        
        response = self.client.get(reverse('quiz:leaderboard', kwargs={'category_slug': self.category.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'quiz/leaderboards.html')

class ProfileTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser', 
            password='12345'
        )
        UserProfile.objects.create(user=self.user)

    # can user upload a profile picture
    def test_profile_picture_upload(self):
        """Test profile picture upload"""
        self.client.login(username='testuser', password='12345')
        
        test_image = SimpleUploadedFile(
            name='test_image.jpg', 
            content=b'', 
            content_type='image/jpeg'
        )
        
        response = self.client.post(reverse('quiz:upload_profile_picture'), 
                                    {'profile_picture': test_image})
        
        user_profile = UserProfile.objects.get(user=self.user)
        self.assertTrue(user_profile.profile_picture)

class QuizNavigationTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser', 
            password='12345'
        )
        
        self.category = Category.objects.create(name='Test Category')
        self.question1 = Question.objects.create(
            category=self.category,
            question_text='Question 1',
            difficulty='easy'
        )
        self.question2 = Question.objects.create(
            category=self.category,
            question_text='Question 2',
            difficulty='medium'
        )
    
        Answer.objects.create(
            question=self.question1,
            answer_text='Correct Answer 1',
            is_correct=True
        )
        Answer.objects.create(
            question=self.question2,
            answer_text='Correct Answer 2',
            is_correct=True
        )

    # does the quiz flow correctly
    def test_quiz_flow(self):
        self.client.login(username='testuser', password='12345')
    
        response = self.client.get(reverse('quiz:fetch_question', 
                                           kwargs={
                                               'category_slug': self.category.slug, 
                                               'mode': 'normal', 
                                               'question_id': self.question1.id
                                           }))
        
        self.assertEqual(response.status_code, 200)

        response = self.client.post(reverse('quiz:fetch_question', 
                                             kwargs={
                                                 'category_slug': self.category.slug, 
                                                 'mode': 'normal', 
                                                 'question_id': self.question1.id
                                             }), 
                                    {'answers': 'Correct Answer 1'})
        
        self.assertIn(response.status_code, [200, 302])



class AdvancedQuizFunctionalityTests(TestCase):
    def setUp(self):
        self.client = Client()
        
        self.user = User.objects.create_user(
            username='testuser', 
            password='12345'
        )
        UserProfile.objects.create(user=self.user)
   
        self.category = Category.objects.create(
            name='Test Quiz Category', 
            slug='test-quiz-category'
        )
        
        self.questions = []
        for i in range(5):
            question = Question.objects.create(
                category=self.category,
                question_text=f'Test Question {i+1}',
                difficulty='medium'
            )
            
            Answer.objects.create(
                question=question,
                answer_text='Correct Answer',
                is_correct=True
            )
            for j in range(3):
                Answer.objects.create(
                    question=question,
                    answer_text=f'Wrong Answer {j+1}',
                    is_correct=False
                )
            
            self.questions.append(question)

    
        # does user score update when scoring higher in a previous game session and is it appended the leaderboard correctly
        def test_leaderboard_score_override(self):
            self.client.login(username='testuser', password='12345')
            
            first_session = GameSession.objects.create(
                user=self.user,
                category=self.category,
                mode='normal',
                score=50
            )
            
            second_session = GameSession.objects.create(
                user=self.user,
                category=self.category,
                mode='normal',
                score=100
            )
    
            response = self.client.get(reverse('quiz:leaderboard', kwargs={'category_slug': self.category.slug}))
            self.assertContains(response, '100')
            
        
            normal_leaderboard = response.context['normal']
            user_scores = [entry.score for entry in normal_leaderboard if entry.user == self.user]
            
            # Assert that there's only one score for the user, and it's the highest score
            self.assertEqual(len(user_scores), 1)
            self.assertEqual(user_scores[0], 100)
            
            # Verify lower score is not in the leaderboard context
            self.assertNotIn(50, user_scores)

    # testing normal mode point scoring with multiple difficulties
    def test_normal_mode_point_system(self):
        self.client.login(username='testuser', password='12345')
        
        session = GameSession(
            user=self.user,
            category=self.category,
            mode='normal'
        )
        
        easy_question = Question.objects.create(
            category=self.category,
            question_text='Easy Question',
            difficulty='easy'
        )
        medium_question = Question.objects.create(
            category=self.category,
            question_text='Medium Question',
            difficulty='medium'
        )
        hard_question = Question.objects.create(
            category=self.category,
            question_text='Hard Question',
            difficulty='hard'
        )
        expected_score = easy_question.score + medium_question.score + hard_question.score
        
        self.assertEqual(
            easy_question.score + medium_question.score + hard_question.score, 
            60  # 10 (easy) + 20 (medium) + 30 (hard)
        )

    # testing timed mode leaderboard functionality
    def test_timed_mode_leaderboard(self):
        self.client.login(username='testuser', password='12345')
        
        # Create multiple timed mode sessions
        timed_sessions = [
            GameSession.objects.create(
                user=self.user,
                category=self.category,
                mode='timed',
                score=i * 20
            ) for i in range(1, 4)
        ]
        
        response = self.client.get(reverse('quiz:leaderboard', kwargs={'category_slug': self.category.slug}))
        
        self.assertContains(response, '40')

    # does remember me checkbox work
    def test_remember_me_functionality(self):
            def setUp(self):
                self.user = User.objects.create_user(username="testuser", password="testpassword")

            def test_remember_me_functionality(self):
            
                self.client.post(reverse("login"), {"username": "testuser", "password": "testpassword"})
                self.assertEqual(self.client.session.get_expiry_age(), 0) 

                self.client.post(reverse("login"), {"username": "testuser", "password": "testpassword", "remember_me": "on"})
                self.assertEqual(self.client.session.get_expiry_age(), 1209600)

    # does game session reset when switching category or game mode
    def test_game_session_reset(self):
        self.client.login(username='testuser', password='12345')
        
        another_category = Category.objects.create(
            name='Another Test Category', 
            slug='another-test-category'
        )
        
        first_question = Question.objects.create(
            category=self.category,
            question_text='First Test Question',
            difficulty='easy'
        )
        Answer.objects.create(
            question=first_question,
            answer_text='Test Answer',
            is_correct=True
        )
        
        new_question = Question.objects.create(
            category=another_category,
            question_text='New Test Question',
            difficulty='medium'
        )
        Answer.objects.create(
            question=new_question,
            answer_text='New Test Answer',
            is_correct=True
        )
        
        # Set up session data
        session = self.client.session
        session['current_score'] = 50
        session['current_difficulty'] = ['easy', 'medium']
        session['current_category'] = self.category.slug
        session['mode'] = 'normal'
        session['played'] = True
        session.save()
    
        response = self.client.get(reverse('quiz:fetch_question', 
                                        kwargs={
                                            'category_slug': another_category.slug, 
                                            'mode': 'normal', 
                                            'question_id': new_question.id
                                        }))
        
        updated_session = self.client.session
        self.assertEqual(updated_session.get('current_score'), 0)
        self.assertEqual(updated_session.get('current_difficulty'), [])
        self.assertEqual(updated_session.get('current_category'), another_category.slug)
        self.assertEqual(updated_session.get('mode'), 'normal')
        self.assertFalse(updated_session.get('played'))



# create empty category and check if appropriate message/page is displayed
class EdgeCaseTests(TestCase):
    def setUp(self):
        # Create a user
        self.user = User.objects.create_user(
            username='testuser', 
            password='12345'
        )
        UserProfile.objects.create(user=self.user)
        
        # Create a category with no questions
        self.empty_category = Category.objects.create(
            name='Empty Category', 
            slug='empty-category'
        )
        

    def test_quiz_with_no_questions(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('quiz:category', kwargs={'category_slug': self.empty_category.slug}))
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.context['questions']) == 0)

class SecurityTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser', 
            password='12345'
        )
        UserProfile.objects.create(user=self.user)
        
        self.category = Category.objects.create(
            name='Test Category', 
            slug='test-category'
        )

    # tests that non logged in users cant access restricted pages
    def test_unauthorized_access_to_protected_views(self):
        protected_urls = [
            reverse('quiz:profile'),
        ]

        for url in protected_urls:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 302, f"URL {url} should redirect for unauthenticated users")
            self.assertTrue(response.url.startswith(reverse('quiz:login')))
