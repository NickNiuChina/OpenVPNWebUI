from django import forms
from .models import User


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            "username",
            "password",
            "name",
            "email",
            "group",
            "log_size",
            "page_size"                   
        ]
