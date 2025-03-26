from django import forms
from django.contrib.auth.models import User
from .models import *
from quiz.models import UserProfile

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ('username', 'email', 'password',)

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('profile_picture',)


class AddCategoryForm(forms.ModelForm):
    name = forms.CharField(max_length=128)
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Category
        fields = ('name', )

class AddQuestionForm(forms.ModelForm):
    question = forms.CharField(max_length=128)
    option1 = forms.CharField(max_length=128) # correct option
    option2 = forms.CharField(max_length=128) 
    option3 = forms.CharField(max_length=128) 
    option4 = forms.CharField(max_length=128)
    difficulty = forms.ChoiceField(choices=Question.DIFFICULTY_CHOICES, label="Difficulty")

    class Meta:
        model = Question
        fields = ('question_text', 'category', 'score', 'difficulty')

class AnswerForm(forms.Form):
    answers = forms.ChoiceField(widget=forms.RadioSelect, choices= [], required = True)

    def __init__(self,answers, *args,  **kwargs):
        super().__init__(*args, **kwargs)
        if answers:
            self.fields['answers'].choices = [(a['answer_text'], a['answer_text']) for a in answers]


