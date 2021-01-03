from django import forms
from django.contrib.auth.forms import UserCreationForm
from captcha.fields import ReCaptchaField

from .models import User


# display name, email
class RegistrationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('username', 'email')
        labels = {
            'username': 'Display name'
        }

    captcha = ReCaptchaField()