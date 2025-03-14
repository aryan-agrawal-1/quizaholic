from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Profile, Category, Quiz, Question


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text="Please enter a valid email address.")

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ('username', 'password')


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('profile_picture',)

class AddQuestionsForm(forms.Form):
    # users get a choice of which category they want to add questions to
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        help_text="Select the category you want to add questions to."
    )

    # Number of questions to add (1, 2, or 3)
    num_questions = forms.ChoiceField(
        choices=[(1, '1'), (2, '2'), (3, '3')],
        help_text="How many questions would you like to add?"
    )

    # basically like a dynamic form where the user selects the number of questions they want to add, and depending on that answer it will show 1,2 or 3 question forms at once
    # this will be done using javascript in its template