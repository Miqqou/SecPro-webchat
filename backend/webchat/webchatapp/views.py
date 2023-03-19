from django.shortcuts import render, redirect
from .models import User
from .forms import UserRegistrationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

# Create your views here.
def index(request):
    return render(request, 'index.html', {})

def chat(request):
    return render(request, 'chat.html', {})

def profile(request):
    return render(request, 'profile.html', {})

#def logout(request):
    #return render(request, 'logout.html', {})

#def login(request):
    #return render(request, 'authentication/login.html', {})

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
                return redirect('index')
            else:
                # No backend authenticated the credentials
                messages.error(request, ("Error login"))
                return redirect('login')
    else:
        return render(request, 'authentication/login.html', {})


