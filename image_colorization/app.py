from flask import Flask, render_template, request, send_from_directory
import cv2
import numpy as np
import os
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'rawImages')
STORAGE_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'colorizedImages')
ALLOWED_EXTENSIONS = {'jpg', 'png', 'gif'}
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['STORAGE_FOLDER'] = STORAGE_FOLDER

def colorize_grayscale_image(input_path):
    grayscale_image = cv2.imread(input_path, cv2.IMREAD_GRAYSCALE)

    dummy_image = np.zeros((grayscale_image.shape[0], grayscale_image.shape[1], 2), dtype=np.uint8)

    lab_image = np.concatenate((grayscale_image[:, :, np.newaxis], dummy_image), axis=2)

    lab_image[:, :, 1] = 230
    lab_image[:, :, 2] = 18

    colored_image = cv2.cvtColor(lab_image, cv2.COLOR_LAB2BGR)

    temp_output_filename = 'temp_output.jpg'
    cv2.imwrite(os.path.join(app.config['STORAGE_FOLDER'], temp_output_filename), colored_image)

    return colored_image


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/colorize', methods=['POST'])
def colorize():
    uploaded_file = request.files['file']

    temp_filename = uploaded_file.filename
    uploaded_file.save(os.path.join(app.config['UPLOAD_FOLDER'], temp_filename))

    colored_image = colorize_grayscale_image(os.path.join(app.config['UPLOAD_FOLDER'], temp_filename))

    return send_from_directory(app.config['STORAGE_FOLDER'],'temp_output.jpg')
