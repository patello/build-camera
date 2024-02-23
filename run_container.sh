#!/bin/bash

# Initialize flags
similar=false
blend=false
rebuild=false

# This loop iterates over all arguments passed to the script. For each argument, it checks if it matches a predefined flag.
# If it does, it sets the corresponding flag to true and removes the argument from the list of arguments using shift.

# --similar: Checks similarity between images and stores the one with the highest similarity
# --blend: Blends the images in the input path before generating the timelapse video
# --rebuild: Rebuilds the Docker image before running the container
for arg in "$@"
do
    case $arg in
        --similar)
            similar=true
            shift
            ;;
        --blend)
            blend=true
            shift
            ;;
        --rebuild)
            rebuild=true
            shift
            ;;
        *)
            # If the argument doesn't match any of the predefined flags, print an error message and exit
            echo "Unknown flag: $arg"
            exit 1
            ;;
    esac
done


# Set the container name, Docker image name and image directory based on the --similar flag
# container_name: The name of the container to be started.
# docker_image: The tag of the Docker image to be used.
# image_dir: The directory which will be mounted to the container. Contains the images to be stored and processed.
if [ "$similar" = true ]; then
    container_name="build-camera-similar"
    docker_image="build-camera:similar"
    image_dir="similar_images"
else
    container_name="build-camera"
    docker_image="build-camera:latest"
    image_dir="images"
fi

# Stop all containers called $container_name
docker stop $container_name

# Get the directory path of the script. This is needed to mount the image directory to the container.
# See https://stackoverflow.com/a/246128/10491322
# /dev/null is used to suppress the output of the cd command
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

# Rebuild the Docker image if the --rebuild flag is set or if the image doesn't exist
if [ "$rebuild" = true ] || [ "$(docker images -q $docker_image 2> /dev/null)" = "" ]; then
    docker build --build-arg similar=$similar --build-arg blend=$blend -t $docker_image $DIR
fi

# Start a new container from the image
docker run --rm -d -v $DIR/$image_dir:/images --name $container_name $docker_image