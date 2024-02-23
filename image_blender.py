import os
import cv2
import logging

import numpy as np

def get_images(images_folder: str) -> list:
    """
    Get the list of image files in the input folder

    Parameters:
        images_folder (str): The input folder where the images are stored
    Returns:
        list: The list of image file paths
    """
    # Get the list of image files in the input folder
    image_files = [f for f in os.listdir(images_folder) if f.endswith('.jpg') or f.endswith('.png')]

    # Sort the image files
    image_files.sort()

    # Return the list of image file paths
    return [os.path.join(images_folder, f) for f in image_files]

def weighted_moving_average(image_paths: list, output_folder: str, weights: list) -> None:
    """
    Apply a weighted moving average to a list of images. The resulting image is saved in the output folder.

    Parameters:
        image_paths (list): The list of image file paths
        output_folder (str): The output folder where the resulting images will be saved
        weights (list): The list of weights for the moving average
    """
    # Create the output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # Create a buffer to hold the last few images
    image_buffer = []

    for image_file in image_paths:
        # Read the image
        logging.debug(f"Processing image: {image_file}")
        image = cv2.imread(image_file)

        # Add the image to the buffer
        image_buffer.append(image)

        # If the buffer is too large, remove the oldest image
        if len(image_buffer) > len(weights):
            image_buffer.pop(0)
        logging.debug(f"Buffer size for averaging: {len(image_buffer)}")

        # Apply the weighted moving average
        weighted_average = np.zeros_like(image, dtype=np.float32)
        total_weight = 0

        for i, weight in enumerate(weights[-len(image_buffer):]):
            # Accumulate the weighted average
            weighted_average += weight * image_buffer[i]
            total_weight += weight

        weighted_average /= total_weight

        # Save the resulting image
        image_name = os.path.basename(image_file)
        output_path = os.path.join(output_folder, image_name)
        cv2.imwrite(output_path, weighted_average)
        logging.debug(f"Weighted moving average image saved: {output_path}")

    logging.info(f"{len(images)} images processed and saved in {output_folder}.")

if __name__ == "__main__":
    # Example parameters, weights are from oldest to newest
    images_folder = 'similar_images'
    output_folder = 'test'
    weights = [0.1, 0.2, 0.3, 0.4]

    # Get the list of image files in the input folder
    images = get_images(images_folder)
    # Apply the weighted moving average, also save the resulting images in the output folder
    weighted_moving_average(images, output_folder, weights)