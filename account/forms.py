from django import forms
from django.contrib.auth.forms import UserCreationForm
from captcha.fields import ReCaptchaField

from .models import User


class RegistrationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('username', 'email')
        labels = {
            'username': 'Display name'
        }

    captcha = ReCaptchaField()

class GroupForm(forms.Form):
    group = forms.ChoiceField(choices=User.GROUP_CHOICES)