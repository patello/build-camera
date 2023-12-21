#!/bin/bash

# Stop all containers called build-camera
docker stop $(docker ps -a -q --filter name=build-camera-similar)

# Get the directory path of the script
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

# Start a new container from the image build-camera:latest
docker run --rm -d -v $DIR/similar_images:/images --name build-camera-similar build-camera:similar