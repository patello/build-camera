# Use ubuntu as the base image
FROM ubuntu:latest
 
# Install python and cron
RUN apt-get update && apt-get -y install python3 python3-pip cron

# Copy the requirements.txt file into the image
COPY requirements.txt /tmp/requirements.txt

# Install the required modules from the requirements.txt file
RUN pip3 install -r /tmp/requirements.txt

# Copy the python script to the container
COPY image-download.py /root/image-download.py
 
# Give execution rights to the python script
RUN chmod 0644 /root/image-download.py

# Set the timezone to Europe/Stockholm
ENV TZ=Europe/Stockholm
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN apt-get install -y tzdata

# Add the cron job to run the python script every day at 12:00
RUN crontab -l | { cat; echo "0 12 * * * python3 /root/image-download.py"; } | crontab -
 
# Create a volume to store the images
VOLUME /images
 
# Modify the python script to save the images to the volume
RUN sed -i 's/date + ".jpg"/"\/images\/" + date + ".jpg"/g' /root/image-download.py
 
# Run the cron service in the foreground
CMD ["cron", "-f"]