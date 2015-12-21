from django import forms
from .models import User


class RegistrationForm(forms.Form):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField(max_length=50)
    phone_number = forms.CharField(max_length=15)
    password = forms.PasswordInput()

    def send_email(self):
        # send email using the self.cleaned_data dictionary
        pass

    class Meta:
        model = User


class LogInForm(forms.Form):
    email = forms.EmailField(max_length=50)
    password = forms.PasswordInput()

    class Meta:
        model = User


class ProfileForm(forms.Form):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    phone = forms.CharField(max_length=30)
    email = forms.EmailField(max_length=254)

    class Meta:
        model = User
