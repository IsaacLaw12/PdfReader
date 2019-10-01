import os
from flask import Flask, flash, request, redirect, url_for, send_from_directory
from pdf2image import convert_from_bytes, convert_from_path
from PIL import Image
import pytesseract
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = set(['pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename, allow_exts=None):
    if allow_exts is None:
        allow_exts = ALLOWED_EXTENSIONS
    return '.' in filename and filename.split('.')[-1] in allow_exts

@app.route('/')
def index():
    return "Hello World"

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

@app.route('/char_extract', methods=['POST'])
def char_extract():
    file = request.files.get('file', None)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(full_upload_path(filename))
        images = pdf_to_image(filename)
    else:
        return "File not valid"
    return pytesseract.image_to_boxes(images[0])

def pdf_to_image(filename):
    images = []
    if allowed_file(filename, ['pdf']):
        images = convert_from_path(full_upload_path(filename))
        return images

def full_upload_path(filename):
    return os.path.join(app.config['UPLOAD_FOLDER'], filename)
