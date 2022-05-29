from django import forms
from django.contrib.auth.models import User
from blog_app.models import UserProfileInfo, Post



class UserForm(forms.ModelForm):
    password = forms.CharField(widget = forms.PasswordInput)

    class Meta():
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password')

class UpdateUserForm(forms.ModelForm): 
    class Meta():
        model = User
        fields = ('first_name', 'last_name', 'username', 'email')

class UserProfileInfoForm(forms.ModelForm):
    class Meta():
        model = UserProfileInfo
        fields = ['profile_pic']


class PostForm(forms.ModelForm):
    class Meta():
        model = Post
        exclude = ['author']
        fields = ['title',  'content', 'status',  'blog_pic']

