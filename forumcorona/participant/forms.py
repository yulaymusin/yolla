from django import forms
from django.contrib.auth.forms import UserCreationForm
from . import models as m


class SignUpForm(UserCreationForm):
    class Meta:
        model = m.Participant
        fields = ('username', 'name', 'email', 'password1', 'password2')


class UserForm(forms.ModelForm):
    class Meta:
        model = m.Participant
        fields = ('name', 'email', 'time_zone', 'l1', 'l2', 'about')

    def __init__(self, time_zones, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['time_zone'] = forms.ChoiceField(choices=time_zones)
