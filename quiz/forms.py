from django import forms
from django.contrib.auth.models import User
from .models import *

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

