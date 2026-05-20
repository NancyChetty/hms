from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import User
from .models import Slot


class SignupForm(UserCreationForm):

    class Meta:

        model = User

        fields = [
            'username',
            'email',
            'role',
            'password1',
            'password2'
        ]


class SlotForm(forms.ModelForm):

    class Meta:

        model = Slot

        fields = [
            'start_time',
            'end_time'
        ]

        widgets = {

            'start_time': forms.DateTimeInput(
                attrs={
                    'type': 'datetime-local'
                }
            ),

            'end_time': forms.DateTimeInput(
                attrs={
                    'type': 'datetime-local'
                }
            ),

        }