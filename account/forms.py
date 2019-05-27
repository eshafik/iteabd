from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Profile


class UserRegistrationForm(UserCreationForm):
    """Form for user registration"""

    email = forms.EmailField(max_length=200,
                             help_text='Required')
    password1 = forms.CharField(label="Password",
                                widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirm Password",
                                widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password1'] != cd['password2']:
            raise forms.ValidationError("Password didn't match")
        else:
            return cd['password2']


class UserEditForm(forms.ModelForm):
    """User edit form"""

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class ProfileEditForm(forms.ModelForm):
    """Profile data edit form"""

    class Meta:
        model = Profile
        exclude = ['user', 'itea_status', 'finance', 'status']
