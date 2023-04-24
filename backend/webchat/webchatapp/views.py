import os
from django.utils import timezone
from django.shortcuts import render, redirect
from .models import Message, UserKey
from .forms import UserRegistrationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
import django.contrib.auth.hashers as hasher

from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64


# Create your views here.
def home(request):
    return render(request, 'index.html', {})


@login_required
def profile(request):
    user_keys = UserKey.objects.get(user=request.user)
    user_public_key = user_keys.publicKey
    return render(request, 'profile.html', { 'publickey':user_public_key})


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
    

def generate_keys_from_password(password):

    password = bytes(password,'UTF-8')

    # Generate private_key
    privateKey = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
    )


    # Public key format.
    publicKey = privateKey.public_key().public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )

    # Encrypting the private key with the user password.
    salt = bytes(str(os.urandom(16)), 'UTF-8')
    kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=32,
    salt=salt,
    iterations=100000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(password))

    private_key_enrypted = Fernet(key).encrypt(bytes(str(privateKey), 'UTF-8'))

    return publicKey, private_key_enrypted 



def register_user(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']

            public_key, private_key_enrypted = generate_keys_from_password(password)



            #passwordConfirm = form.cleaned_data['passwordConfirm']
            user = authenticate(username=username, password=password)


            if user is not None:
                userkey = UserKey(user=user, publicKey=public_key, privateCryptedKey=private_key_enrypted)
                userkey.save()

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


def encrypt_message(message, receiver):
    receiver_keys = UserKey.objects.get(user=receiver)
    receiver_public_key = receiver_keys.publicKey

    # Crypting the message with receiver's public key.
    ciphertext = receiver_public_key.encrypt(
    message,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)

    print(ciphertext)
    return ciphertext


@login_required
def chat(request):
    if request.method == 'POST':
        recipient = request.POST['recipient']
        content = request.POST['content']
        recipient_user = User.objects.get(username=recipient)

        message = Message(sender=request.user, recipient=recipient_user, 
                          content=encrypt_message(content, recipient_user), 
                          created_at=timezone.now())
        message.save()
        return redirect('chat')
    
    # Set of messaging partners of user
    messages1 = Message.objects.filter(recipient=request.user).order_by('-created_at')
    senders = set()
    for message in messages1:
        sender = message.sender
        senders.add(sender)

    for message in messages1:
        try:
            # TODO decrypt message content with your password
            message.content = message.content
        except Exception:
            message.content = 'Message content could not be decrypted.'

    return render(request, 'chat.html', {'messages1': messages1, 'senders': senders})
