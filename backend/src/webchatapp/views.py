import os
from django.utils import timezone
from django.shortcuts import render, redirect
from .models import Message, UserKey
from .forms import UserRegistrationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
from django.views.decorators.cache import never_cache
from django.http import JsonResponse


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
    

def generate_keys_from_password(password):

    password = bytes(password,'UTF-8')

    # Generate private_key
    privateKey = rsa.generate_private_key(
    public_exponent=65537,
    key_size=4096,
    )

    encryption_algorithm = serialization.BestAvailableEncryption(password)

    private_key_enrypted = privateKey.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=encryption_algorithm,
        )

    # Public key format.
    publicKey = privateKey.public_key().public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )

    # Encrypting the private key with the user password.
    salt = os.urandom(32)
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=480000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(password))

    private_key_enrypted = Fernet(key).encrypt(private_key_enrypted)

    return publicKey, private_key_enrypted, salt 


def register_user(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            try:
                username = form.cleaned_data['username']
                password = form.cleaned_data['password1']

                # For axes, limits account creation to failed login amount
                authenticate(request=request,)

                form.save()

                public_key, private_key_enrypted, salt = generate_keys_from_password(password)

                user = authenticate(request=request, username=username, password=password)
            except:
                user == None


            if user is not None:
                userkey = UserKey(user=user, publicKey=public_key, 
                                  privateCryptedKey=private_key_enrypted,
                                  salt=salt)
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

    # Fetching the public key of the recipient.
    receiver_keys = UserKey.objects.get(user=receiver)
    receiver_public_key = receiver_keys.publicKey
    public_key = serialization.load_pem_public_key(receiver_public_key)

    # Encoding Bytes
    message_encoded = message.encode('UTF-8')

    # Encrypting the message with receiver's public key.
    encrypted_message = public_key.encrypt(
        message_encoded,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    return encrypted_message

def decrypt_message(encrypted_message, user, pw):

    # Fetch recipient's encrypted privatekey and salt
    user_keys = UserKey.objects.get(user=user)
    user_private_key_encrypted = user_keys.privateCryptedKey
    salt = user_keys.salt

    # Derive the Fernet key from the password and salt
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=480000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(pw))

    # Decrypt the private_key with the key.
    private_key = Fernet(key).decrypt(user_private_key_encrypted)

    # Decrypt the serialization level with the password
    private_key = serialization.load_pem_private_key(
        private_key,
        password=pw
        )
    
    # Decrypt the message
    decrypted_message = private_key.decrypt(
        encrypted_message,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    return decrypted_message.decode('UTF-8')


@login_required
def chat(request):
    if request.method == 'POST':
        try:
            recipient = str(request.POST['recipient']).strip()
            content = str(request.POST['content'])
            recipient_user = User.objects.get(username=recipient)

            if len(content) > 500:
                messages.error(request, ("Too long message! 500 char max"))
            else:
    
                    message = Message(sender=request.user, recipient=recipient_user, 
                                        content=encrypt_message(content, recipient_user), 
                                        created_at=timezone.now())
                    message.save()
            return redirect('chat') 
        except Exception as e:
            messages.error(request, ("Couldn't sent message! User not found."))
                
    
    return render(request, 'chat.html', {})


@login_required
@never_cache
def inbox(request):        
    # Set of messaging partners of user
    messages1 = Message.objects.filter(recipient=request.user).order_by('-created_at')
    messages2 = messages1

    number_of_messages = 0

    senders = set()
    for message in messages1:
        sender = message.sender
        senders.add(sender)
        if message.read_at != "":
            number_of_messages +=1


    if request.method == 'POST':
        password = bytes(request.POST['password'], 'UTF-8')
        user = authenticate(request=request, username=request.user.username, password=password)
        try:
            for message in messages1:
                
                message.content = decrypt_message(message.content, request.user, password)

                message.read_at = timezone.now()

            return render(request, 'messages.html', {'messages1': messages1, 'senders': senders}) 
                            
        except Exception:
            messages.error(request, ("Wrong password, couldn't decrypt!"))
            return render(request, 'messages.html', {'number_of_messages' : number_of_messages})   
            
    else:
        return render(request, 'messages.html', {'number_of_messages' : number_of_messages, 'senders': senders}) 

# Django axes lockout/cooldown message page
def lockout(request, credentials, *args, **kwargs):
    return JsonResponse({"status": "COOLDOWN: Too many login failures. Wait 10 minutes to try again."}, status=403)