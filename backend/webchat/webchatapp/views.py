import os
from django.utils import timezone
from django.shortcuts import render, redirect
from .models import Message, PublicKey
from .forms import UserRegistrationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
import django.contrib.auth.hashers as hasher


# Create your views here.
def home(request):
    return render(request, 'index.html', {})


@login_required
def profile(request):
    return render(request, 'profile.html', {})


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

@login_required
def logout_user(request):
    logout(request)
    messages.success(request, ("Log out successfully!"))
    return redirect('home')


def encrypt_message(message, key):
    salt = os.urandom(16)

    password_hash = hasher.make_password(key, salt=str(salt), hasher='argon2')

    print(hasher.check_password(key,password_hash))

    # TODO
    # message hash with 'password_hash as pub'


    print(password_hash)
    return password_hash


@login_required
def chat(request):
    if request.method == 'POST':
        recipient = request.POST['recipient']
        content = request.POST['content']
        recipient_user = User.objects.get(username=recipient)

        # Encrypt message content
        #ph = hasher.Argon2PasswordHasher
        #encrypted_content, salt = ph.encode(password=content,salt= os.urandom(16))

        message = Message(sender=request.user, recipient=recipient_user, content=encrypt_message(content, "12345"), created_at=timezone.now())
        message.save()
        return redirect('chat')
    
    messages1 = Message.objects.filter(recipient=request.user).order_by('-created_at')
    for message in messages1:
        try:
            # TODO decrypt message content with your password
            message.content = verify(message.content, content)
        except Exception:
            message.content = 'Message content could not be decrypted.'

    return render(request, 'chat.html', {'messages1': messages1})
