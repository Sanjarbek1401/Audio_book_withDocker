import os
import uuid
import pyttsx3
import docx
import pymupdf as fitz
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB
ALLOWED_EXTENSIONS = {'.pdf', '.docx', '.txt'}

def validate_file(file):
    if file.size > MAX_FILE_SIZE:
        logger.warning(f"File size ({file.size} bytes) exceeds maximum limit of {MAX_FILE_SIZE} bytes")
        raise ValueError("File size exceeds maximum limit")

    file_extension = os.path.splitext(file.name)[1].lower()
    if file_extension not in ALLOWED_EXTENSIONS:
        logger.warning(f"Invalid file format: {file_extension}")
        raise ValueError("Invalid file format")

    logger.info(f"File validated successfully: {file.name}")
    return file_extension

def extract_text_from_pdf(file):
    try:
        text = ''
        pdf_document = fitz.open(stream=file.read(), filetype="pdf")
        for page_num in range(len(pdf_document)):
            page = pdf_document.load_page(page_num)
            text += page.get_text("text")
        logger.info(f"Successfully extracted text from PDF: {file.name}")
        return text
    except Exception as e:
        logger.error(f"Error processing PDF file {file.name}: {str(e)}")
        raise ValueError(f"Error processing PDF file: {str(e)}")

def extract_text_from_docx(file):
    try:
        doc = docx.Document(file)
        text = '\n'.join([paragraph.text for paragraph in doc.paragraphs])
        logger.info(f"Successfully extracted text from DOCX: {file.name}")
        return text
    except Exception as e:
        logger.error(f"Error processing DOCX file {file.name}: {str(e)}")
        raise ValueError(f"Error processing DOCX file: {str(e)}")

def extract_text_from_txt(file):
    try:
        text = file.read().decode('utf-8')
        logger.info(f"Successfully extracted text from TXT: {file.name}")
        return text
    except UnicodeDecodeError:
        file.seek(0)
        try:
            text = file.read().decode('latin-1')
            logger.info(f"Successfully extracted text from TXT (latin-1 encoding): {file.name}")
            return text
        except Exception as e:
            logger.error(f"Error processing TXT file {file.name}: {str(e)}")
            raise ValueError(f"Error processing TXT file: {str(e)}")

def extract_text(file, file_extension):
    extractors = {
        '.pdf': extract_text_from_pdf,
        '.docx': extract_text_from_docx,
        '.txt': extract_text_from_txt
    }

    extractor = extractors.get(file_extension.lower())
    if not extractor:
        logger.error(f"No text extractor found for {file_extension}")
        raise ValueError(f"No text extractor found for {file_extension}")

    return extractor(file)

def text_to_speech(text, output_file):
    try:
        engine = pyttsx3.init()
        engine.setProperty('rate', 150)
        engine.setProperty('volume', 0.9)
        engine.save_to_file(text, output_file)
        engine.runAndWait()

        if not os.path.exists(output_file):
            raise Exception("Audio file was not created")

        logger.info(f"Successfully created audio file: {output_file}")
        return True
    except Exception as e:
        logger.error(f"Text-to-speech error with pyttsx3: {str(e)}")

        # Fallback to gTTS
        try:
            from gtts import gTTS
            tts = gTTS(text=text, lang='en')
            tts.save(output_file)
            logger.info(f"Successfully created audio file using gTTS fallback: {output_file}")
            return True
        except Exception as fallback_e:
            logger.error(f"Fallback TTS (gTTS) also failed: {str(fallback_e)}")
            raise ValueError("Could not convert text to speech. Please check system configuration.")

def ensure_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
        logger.info(f"Created directory: {directory}")

def process_file(file, file_extension):
    try:
        logger.info(f"Starting to process file: {file.name}")
        text = extract_text(file, file_extension)

        output_filename = f"{uuid.uuid4()}.mp3"
        output_dir = os.path.join(settings.MEDIA_ROOT, 'audio')

        ensure_dir(output_dir)

        output_path = os.path.join(output_dir, output_filename)

        success = text_to_speech(text, output_path)

        if success:
            logger.info(f"Successfully processed file. Audio saved as: {output_path}")
            return output_filename
        else:
            raise ValueError("Failed to convert text to speech")

    except Exception as e:
        logger.error(f"Error processing file {file.name}: {str(e)}")
        raise ValueError(f"Error processing file: {str(e)}")