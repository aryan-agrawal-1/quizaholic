from django import forms
from django.contrib.auth.models import User
from quiz.models import UserProfile

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    email = forms.EmailField(widget=forms.EmailInput())
    class Meta:
        model = User
        fields = ('username', 'email', 'password',)
        exclude = ('category',)

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('profile_picture',)
