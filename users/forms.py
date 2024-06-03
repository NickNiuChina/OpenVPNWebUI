from django import forms
from .models import User
from django.contrib.auth.hashers import make_password


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = [
            "username",
            "password",
            "confirm_password",
            "name",
            "email",
            "group",
            "log_size",
            "page_size"                   
        ]

        def clean(self):
            cleaned_data = super(UserForm, self).clean()
            password = cleaned_data.get("password")
            confirm_password = cleaned_data.get("confirm_password")

            if password != confirm_password:
                raise forms.ValidationError(
                    "password and confirm_password does not match"
                )

        widgets = {
            # telling Django your password field in the mode is a password input on the template
            'password': forms.PasswordInput() 
        }

        def clean_password(self):
            password = self.cleaned_data['password']
            return make_password(password)
