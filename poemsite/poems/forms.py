from django import forms
from .models import Poem
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class PoemForm(forms.ModelForm):
    class Meta:
        model = Poem
        fields = ['title', 'body']

# FLAW 2: A07:2021 - Add register form
#class RegisterForm(UserCreationForm):
 #   class Meta:
  #      model = User
   #     fields = ['username', 'password1', 'password2']
