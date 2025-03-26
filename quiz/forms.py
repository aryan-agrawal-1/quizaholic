from django import forms
from django.contrib.auth.models import User
from .models import *

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    email = forms.EmailField(widget=forms.EmailInput())
    class Meta:
        model = User
        fields = ('username', 'email', 'password',)
        exclude = ('category',)
        help_texts = {
            'username': None,
        }


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('profile_picture',)

class AddCategoryForm(forms.ModelForm):
    name = forms.CharField(max_length=128)
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)
    category_image = forms.ImageField(required=False)

    class Meta:
        model = Category
        fields = ('name', 'category_image')
    
    def save(self, user, commit=True):
        category = super().save(commit=False)
        category.slug = slugify(self.cleaned_data['name'])
        category.created_by = user  # Set the current user

        if commit:
            category.save()
        return category

class AddQuestionForm(forms.Form):
    question_text = forms.CharField(max_length=999)
    option1 = forms.CharField(max_length=999)  # correct option
    option2 = forms.CharField(max_length=999)
    option3 = forms.CharField(max_length=999)
    option4 = forms.CharField(max_length=999)
    difficulty = forms.ChoiceField(choices=Question.DIFFICULTY_CHOICES, label="Difficulty")

    def __init__(self, *args, **kwargs):
        super(AddQuestionForm, self).__init__(*args, **kwargs)
        self.fields['option1'].label = "Option 1 (Correct Option)"
        self.fields['option2'].label = "Option 2"
        self.fields['option3'].label = "Option 3"
        self.fields['option4'].label = "Option 4"

class AnswerForm(forms.Form):
    answers = forms.ChoiceField(widget=forms.RadioSelect, choices= [], required = True)

    def __init__(self, *args, answers =None, **kwargs):
        super().__init__(*args, **kwargs)
        if answers:
            self.fields['answers'].choices = [(a['answer'], a['answer']) for a in answers]