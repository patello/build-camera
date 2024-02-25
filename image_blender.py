import os
import cv2
import logging
import sys

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

        # If buffer is filled, do a weighted moving average, otherwise skip to the next image
        if len(image_buffer) < len(weights):
            continue
        else:
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

            # Remove the oldest image from the buffer
            image_buffer.pop(0)
        logging.info(f"{len(images)} images processed and saved in {output_folder}.")

if __name__ == "__main__":
    # Example weights, weights are from oldest to newest
    weights = [0.1, 0.2, 0.3, 0.4]

    # Get input and output folders from command line arguments
    if len(sys.argv) > 2:
        images_folder = sys.argv[1]
        output_folder = sys.argv[2]
        # Sanity check that input and output folders are different
        if images_folder == output_folder:
            raise ValueError("Input and output folders must be different.")
    else:
        raise ValueError("Please provide input and output folders as command line arguments.")

    # Get the list of image files in the input folder
    images = get_images(images_folder)

    # Get list of existing base names of images in the output folder
    existing_images = [os.path.basename(image) for image in get_images(output_folder)]

    # Get indices of images that not already processed, remove indices from the list of images except
    # for the number of images prior to the existing ones equal to the lenght of the weights. Then
    # remove the images that are already processed based on the indices. Also remove the indices lower 
    # than the number of weights since they are not processed because there doesn't exist enough prior
    # images to apply the weighted moving average on them.
    indices = [i for i, image in enumerate(images) if os.path.basename(image) not in existing_images]
    indices = [i for i in indices if i >= len(weights)]
    if len(indices) > 0:
        indices = list(range(max(0, indices[0]-len(weights)+1), indices[0])) + indices
        images = [images[i] for i in indices]
    else:
        logging.info(f"All images in {images_folder} are already processed.")
        sys.exit()

    # Apply the weighted moving average, also save the resulting images in the output folder
    weighted_moving_average(images, output_folder, weights)