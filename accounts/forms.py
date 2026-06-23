from django import forms 
from django.contrib.auth.forms import UserCreationForm
from .models import User

class SignUpForm(UserCreationForm):
    role = forms.ChoiceField(choices=User.Role.choices)
    class Meta:
        model = User
        fields = ("first_name", "last_name", "username", "email", "password1", "password2")
        
class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "username", "email","address", "phone_number", "image")