from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
# from django.http import HttpRequest
from .forms import UserRegisterForm
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives
from django.contrib import messages



# Create your views here.

def index(request):
    return render(request, 'chessapp/index.html', {})

@login_required()
def profile(request):
    return render(request, 'chessapp/profile.html', {})


