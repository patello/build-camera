# Use ubuntu as the base image
FROM ubuntu:latest

#Select wether to use similarity score or not
ARG similar=false

# Install python, cron and libgl1-mesa-glx, libglib2 and cmake
RUN apt-get update && apt-get -y install python3 python3-pip cron libgl1-mesa-glx libglib2.0-0 cmake

# Copy the requirements.txt file into the image
COPY requirements.txt /tmp/requirements.txt


# Install the required modules from the requirements.txt file
RUN pip3 install -r /tmp/requirements.txt

# Copy the python script to the container
COPY image_download.py /image_download.py
 
# Give execution rights to the python script
RUN chmod 0644 /image_download.py

# Set the timezone to Europe/Stockholm
ENV TZ=Europe/Stockholm
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN apt-get install -y tzdata

# Add the cron job to run the python script at 12 every day if similar is false, otherwise run every 10 minutes between 11 and 13 with the --similar flag
RUN if [ "$similar" = "false" ] ; then crontab -l | { cat; echo "0 12 * * * python3 /image_download.py >> /images/image_download.log 2>&1"; } | crontab - ; else crontab -l | { cat; echo "*/10 11-13 * * * python3 /image_download.py --similar >> /images/image_download.log 2>&1"; } | crontab - ; fi
 
# Create a volume to store the images
VOLUME /images
 
# Modify the python script to save the images to the volume
RUN sed -i 's/dir = "\.\/images\/"/dir = "\/images\/"/g' /image_download.py
 
# Run the cron service in the foreground
CMD ["cron", "-f"]