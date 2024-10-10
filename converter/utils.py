# converter/utils.py
import os
import pyttsx3
import PyPDF2
import docx

def extract_text_from_pdf(file):
    pdf_reader = PyPDF2.PdfFileReader(file)
    text = ''
    for page_num in range(pdf_reader.numPages):
        text += pdf_reader.getPage(page_num).extract_text()
    return text

def extract_text_from_docx(file):
    doc = docx.Document(file)
    text = '\n'.join([paragraph.text for paragraph in doc.paragraphs])
    return text

def text_to_speech(text, output_file='output.mp3'):
    engine = pyttsx3.init()
    engine.save_to_file(text, output_file)
    engine.runAndWait()
