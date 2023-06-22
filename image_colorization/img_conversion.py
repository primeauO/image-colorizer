import cv2
import numpy as np
import os

def colorize_grayscale_images(input_paths, output_folder):
    for input_path in input_paths:
        filename = os.path.basename(input_path)
        filename_without_ext = os.path.splitext(filename)[0]

        output_path = os.path.join(output_folder, f"{filename_without_ext}_colored.jpg")

        grayscale_image = cv2.imread(input_path, cv2.IMREAD_GRAYSCALE)

        dummy_image = np.zeros((grayscale_image.shape[0], grayscale_image.shape[1], 2), dtype=np.uint8)

        lab_image = np.concatenate((grayscale_image[:, :, np.newaxis], dummy_image), axis=2)

        lab_image[:, :, 1] = 230
        lab_image[:, :, 2] = 18

        colored_image = cv2.cvtColor(lab_image, cv2.COLOR_LAB2BGR)

        cv2.imwrite(output_path, colored_image)

input_folder = "/Users/mac/Downloads/pele1.jpeg"
output_folder = "/path/to/output/folder"

input_files = [os.path.join(input_folder, file) for file in os.listdir(input_folder) if file.endswith('.jpeg')]

colorize_grayscale_images(input_files, output_folder)
