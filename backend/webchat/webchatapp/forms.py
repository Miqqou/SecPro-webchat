from django import forms
from .models import User

class UserRegistrationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'password')
        widgets = {
            'password' : forms.PasswordInput(render_value=True)
        }