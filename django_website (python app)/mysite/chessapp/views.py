from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth.forms import UserCreationForm
# from django.http import HttpRequest
from .forms import UserRegisterForm
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives
from django.contrib import messages
from django.http import JsonResponse
from .models import CapturedImage
from .scripts import trim_image
from django.http import HttpResponseRedirect


# Create your views here.

@login_required()
def index(request):
    return render(request, 'chessapp/index.html', {})

@login_required()
def save_image(request):
    if request.method == 'POST':
        image_data = request.POST.get('image_data')
        image_data = trim_image(image_data)
        captured_image = CapturedImage(image=image_data)
        captured_image.save()

        request.session['captured_image'] = image_data
        return

    return JsonResponse({'error': 'Image capture failed.'})

@login_required()
def analysis(request):

    if request.method == 'POST':
        print("houston we have a problem")

    print('analysis board time!')

    image_data = request.session.get('captured_image', None)

    context = {
        'base64_image': image_data
    }
    return render(request, 'chessapp/analysis.html', context=context)


@login_required()
def profile(request):

    username = request.user.username

    context = {
        'username': username,
    }


    return render(request, 'chessapp/profile.html', context=context)

def logout_view(request):
    logout(request)
    return redirect('/login')