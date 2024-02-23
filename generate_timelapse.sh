#!/bin/bash


# This script takes an input path and a output file name and generates a timelapse video from the images in the input path
# Optionally, the argument --blend can be supplied, which first blends the images in the input path before generating the timelapse video

# Example usage:
# ./generate_timelapse.sh /path/to/input/folder /path/to/output/file.mp4 --blend

# Take the first two arguments and store them in the variables folder_path and output_file
folder_path=$1
output_file=$2

# Path to store the blended images if the --blend flag is present
blended_images_path="$(dirname "$0")/blended_images"

# Check if the --blend flag is present in the arguments
for arg in "$@"
do
    if [ "$arg" == "--blend" ]; then
        # Create the directory to store the blended images
        mkdir -p $blended_images_path
        # If the --blend flag is present, blend the images in the input path
        python3 "$(dirname "$0")/image_blender.py" $folder_path $blended_images_path
        # Set the folder_path to the path of the blended images
        folder_path=$blended_images_path
        break
    fi
done

ffmpeg -framerate 60 -pattern_type glob -i "${folder_path}/*.jpg" -vf scale=720:-1 -c:v libx264 -pix_fmt yuv420p "${output_file}" -y
