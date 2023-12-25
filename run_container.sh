#!/bin/bash

# Check if the first argument is "similar" to run the similar images container
# or if it is empty to run the normal images container
# If the first argument is not empty and not "similar" then exit with an error
similar=false
if [ "$1" = "--similar" ]; then
    similar=true
elif [ -n "$1" ]; then
    echo "Unknown flag: $1"
    exit 1
fi

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

# Get the directory path of the script
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

# Start a new container from the image build-camera:latest

docker run --rm -d -v $DIR/$image_dir:/images --name $container_name $docker_image
