from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'index.html', {})

def messages(request):
    return render(request, 'messages.html', {})

def profile(request):
    return render(request, 'profile.html', {})

def logout(request):
    return render(request, 'logout.html', {})