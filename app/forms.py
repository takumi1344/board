from django import forms
from .models import Board, Comment
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class BoardForm(forms.ModelForm):
    class Meta:
        model = Board
        fields = ['title', 'content']
       

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']



class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text="emailアドレスは必須です。")

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']