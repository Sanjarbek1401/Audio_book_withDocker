from django.contrib.auth import authenticate,login
from django.http import JsonResponse
from django.shortcuts import render
from .utils import process_file, validate_file
import logging
from django.conf import settings
from django.shortcuts import render,redirect
from django.contrib import messages
from . forms import  UserRegisterForm

logger = logging.getLogger(__name__)

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'converter/register.html', {'form': form})



def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request,user)
            return render(request,'converter/upload.html')
        else:
            messages.error(request, 'Username or Password is incorrect')
    return render(request, 'converter/login.html')





def file_upload_view(request):
    if request.method == 'GET':
        return render(request, 'converter/upload.html')

    if request.method == 'POST':
        if 'file' not in request.FILES:
            return JsonResponse({
                "success": False,
                "error": "No file provided"
            }, status=400)

        file = request.FILES['file']

        try:
            # Validate and process file
            file_extension = validate_file(file)
            output_filename = process_file(file, file_extension)

            return JsonResponse({
                "success": True,
                "audio_file_url": f'{settings.MEDIA_URL}audio/{output_filename}',
                "message": "File processed successfully"
            }, status=201)

        except ValueError as e:
            logger.error(f"Processing error: {str(e)}")
            return JsonResponse({
                "success": False,
                "error": str(e)
            }, status=400)
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            return JsonResponse({
                "success": False,
                "error": "An unexpected error occurred. Please try again later."
            }, status=500)