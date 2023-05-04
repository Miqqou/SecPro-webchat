from django import forms
from django.contrib.auth.models import User
#from models import User
from django import forms  
from django.contrib.auth.forms import UserCreationForm  
from django.core.exceptions import ValidationError  
from django.forms.fields import EmailField  
from django.forms.forms import Form  

class UserRegistrationForm(UserCreationForm):
    username = forms.CharField(label='Username* ', help_text="4-20 letters/numbers/symbols (@ . + - _) allowed", min_length=4, max_length=20
                               ,widget=forms.TextInput(attrs={'class':'form-control'}))  
    password1 = forms.CharField(label='Password* ', help_text="12 characters minimum", widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2 = forms.CharField(label='Confirm password* ', widget=forms.PasswordInput(attrs={'class':'form-control'}))  
    
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')



    def username_clean(self):  
        username = self.cleaned_data['username'].lower()  
        new = User.objects.filter(username = username) 
        print(len(username))
        if len(username) < 4:
            raise ValidationError("Username should be longer than 3 chars", code="invalid")  
        if new.count():  
            raise ValidationError("User Already Exist!!", code="invalid")  
        return username  
  
    def clean_password2(self):  
        password1 = self.cleaned_data['password1']  
        password2 = self.cleaned_data['password2']  
  
        if password1 and password2 and password1 != password2:  
            raise ValidationError("Password don't match", code="invalid")  
        return password2  
  
    def save(self, commit = True):  
        user = User.objects.create_user(  
            username = self.cleaned_data['username'],  
            password = self.cleaned_data['password1']  
        )  
        return user
    