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
from django.core.files.base import ContentFile
import base64
from backend.board_detection import board_to_fen



# Create your views here.

@login_required()
def index(request):
    return render(request, 'chessapp/index.html', {})

@login_required()
def save_image(request):
    if request.method == 'POST':
        image_file = request.FILES['image']
        image_data = image_file.read()
        encoded_image_data = trim_image(image_data)
        request.session['image_data'] = encoded_image_data
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

@login_required()
def analysis(request):
    encoded_image_data = request.session.get('image_data')
    if encoded_image_data:
        image_data = base64.b64decode(encoded_image_data)
        image = ContentFile(image_data, 'capture.png')
        # position = board_to_fen(image)
    else:
        image = None
    return render(request, 'chessapp/analysis.html', {'image': image})


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