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
    # Load the grayscale image
    grayscale_image = cv2.imread(input_path, cv2.IMREAD_GRAYSCALE)

    # Create a dummy image with 2 channels (grayscale + alpha)
    dummy_image = np.zeros((grayscale_image.shape[0], grayscale_image.shape[1], 2), dtype=np.uint8)

    # Concatenate the grayscale image and dummy image along the third channel
    lab_image = np.concatenate((grayscale_image[:, :, np.newaxis], dummy_image), axis=2)

    # Modify the A and B channels for colorization
    lab_image[:, :, 1] = 230  # Modify the A channel (green-red)
    lab_image[:, :, 2] = 18  # Modify the B channel (blue-yellow)

    # Convert LAB image to RGB
    colored_image = cv2.cvtColor(lab_image, cv2.COLOR_LAB2BGR)

    # Save the colorized image to a temporary location
    temp_output_filename = 'temp_output.jpg'
    cv2.imwrite(os.path.join(app.config['STORAGE_FOLDER'], temp_output_filename), colored_image)

    return colored_image


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/colorize', methods=['POST'])
def colorize():
    # Get the uploaded file from the form data
    uploaded_file = request.files['file']

    # Save the uploaded file to a temporary location
    # temp_filename = 'temp.jpg'
    # uploaded_file.save(temp_filename)

    # temp_filename = secure_filename(uploaded_file.filename)
    temp_filename = uploaded_file.filename
    uploaded_file.save(os.path.join(app.config['UPLOAD_FOLDER'], temp_filename))

    # Perform colorization
    colored_image = colorize_grayscale_image(os.path.join(app.config['UPLOAD_FOLDER'], temp_filename))
    # Remove the temporary file
    # os.remove(temp_filename)



    # Send the colorized image as a response
    # return send_file(temp_output_filename, mimetype='image/jpeg', as_attachment=True)
    return send_from_directory(app.config['STORAGE_FOLDER'],'temp_output.jpg')
