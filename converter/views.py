import pyttsx3
from django.shortcuts import render
import requests
from django.http import JsonResponse, HttpResponse
from django.core.files.storage import FileSystemStorage
from gtts import gTTS


def upload_file(request):
    if request.method == 'POST' and 'document' in request.FILES:
        document = request.FILES['document']

        # Faylni serverga yuklaymiz
        fs = FileSystemStorage()
        filename = fs.save(document.name, document)
        file_path = fs.path(filename)

        # Fayldan matnni chiqarib olish
        with open(file_path, 'r') as file:
            text = file.read()

        # pyttsx3 orqali matnni ovozga aylantirish
        engine = pyttsx3.init()
        engine.save_to_file(text, 'output_audio.mp3')
        engine.runAndWait()

        # Ovozli faylni foydalanuvchiga qaytarish
        with open('output_audio.mp3', 'rb') as f:
            response = HttpResponse(f.read(), content_type='audio/mpeg')
            response['Content-Disposition'] = 'attachment; filename="output_audio.mp3"'
            return response

    return render(request, 'converter/upload.html')



