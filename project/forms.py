from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
 
 
 
class UserRegisterForm(UserCreationForm):
    username = forms.CharField(max_length = 20)
    first_name = forms.CharField(max_length = 20)
    last_name = forms.CharField(max_length = 20)
    email = forms.EmailField()
    checkBoxInput = forms.BooleanField(required=False)
    class Meta:
        model = User
        fields = ['email', 'password1', 'password2', 'first_name', 'last_name', 'username']