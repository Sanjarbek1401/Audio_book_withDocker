# converter/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import UploadedFile
from .utils import extract_text_from_pdf, extract_text_from_docx, text_to_speech
import os


class FileUploadView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        file = request.FILES['file']
        file_instance = UploadedFile.objects.create(user=request.user, file=file)

        # Fayl turini aniqlash
        file_extension = os.path.splitext(file.name)[1]
        if file_extension == '.pdf':
            text = extract_text_from_pdf(file)
        elif file_extension == '.docx':
            text = extract_text_from_docx(file)
        elif file_extension == '.txt':
            text = file.read().decode('utf-8')
        else:
            return Response({"error": "Fayl formati noto'g'ri!"}, status=400)

        # Matnni ovozga aylantirish
        output_file = f'media/audio/{file_instance.id}.mp3'
        text_to_speech(text, output_file)

        # Ovozli faylni foydalanuvchiga qaytarish
        return Response({"audio_file_url": request.build_absolute_uri(output_file)}, status=201)
