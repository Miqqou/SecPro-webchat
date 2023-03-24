from django.shortcuts import render, redirect
#from .models import User
from .forms import UserRegistrationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm

# Create your views here.
def home(request):
    return render(request, 'index.html', {})

def chat(request):
    return render(request, 'chat.html', {})

def profile(request):
    return render(request, 'profile.html', {})


'''def create(request):
    if request.method == 'POST':
        form = UserRegistrationForm.objects.get(username=username)
        if form.is_valid():
            user = form.save(commit=False)
            username = request.POST.get('inputUsername')
            password = request.POST.get('inputPassword')
            passwordConfirm = request.get('inputPasswordConfirm')
            print(username, password)

            if password == passwordConfirm:
                form.save()
            else:
                print("passwords not matching")

    else:
        form = UserRegistrationForm()
    
    return render(request, 'authentication/create.html', {'form': form})'''

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # A backend authenticated the credentials
            login(request, user)
            return redirect('home')
        else:
            # No backend authenticated the credentials
            messages.error(request, ("Error login"))
            return redirect('login')
    else:
        return render(request, 'authentication/login.html', {})


def register_user(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            #passwordConfirm = form.cleaned_data['passwordConfirm']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, ("Successfully created a new user!"))
                return redirect('home')
            else:
                # No backend authenticated the credentials
                messages.error(request, ("Error registering"))
                return redirect('create')
    else:
        form = UserRegistrationForm

    return render(request, 'authentication/create.html', {'form':form})


def logout_user(request):
    logout(request)
    messages.success(request, ("Log out successfully!"))
    return redirect('home')
