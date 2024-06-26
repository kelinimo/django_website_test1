from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm


class UserForm(forms.ModelForm):

    class Meta:
        model = get_user_model()
        fields = ["username", "first_name", "last_name", "email"]


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = get_user_model()
        fields = UserForm.Meta.fields
