import cv2
import numpy as np
import os

def colorize_grayscale_images(input_paths, output_folder):
    for input_path in input_paths:
        # Extract the filename and extension
        filename = os.path.basename(input_path)
        filename_without_ext = os.path.splitext(filename)[0]

        # Create the output file path
        output_path = os.path.join(output_folder, f"{filename_without_ext}_colored.jpg")

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

        # Save the colorized image
        cv2.imwrite(output_path, colored_image)

input_folder = "/Users/mac/Downloads/pele1.jpeg"  # Replace with the folder path containing the input grayscale images
output_folder = "/path/to/output/folder"  # Replace with the folder path where the colored images will be saved

# Get a list of all input image files in the input folder
input_files = [os.path.join(input_folder, file) for file in os.listdir(input_folder) if file.endswith('.jpeg')]

# Colorize the grayscale images and save the colored images
colorize_grayscale_images(input_files, output_folder)
