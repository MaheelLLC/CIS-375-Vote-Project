from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already taken.")
        if not username.isalnum():
            raise forms.ValidationError("The username should only contain letters and numbers.")
        return username

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        if len(password1) < 8:
            raise forms.ValidationError("The password must be at least 8 characters long.")
        if not any(char.isdigit() for char in password1):
            raise forms.ValidationError("The password must contain at least one digit.")
        if not any(char.isalpha() for char in password1):
            raise forms.ValidationError("The password must contain at least one letter.")
        return password1
