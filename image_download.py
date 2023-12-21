# Import the modules
import requests
import datetime
import logging
import cv2
import os
import sys
import numpy as np
 
# Configure the logging level and format
logging.basicConfig(level=logging.DEBUG, format="%(levelname)s: %(message)s")

today = datetime.date.today().strftime("%Y-%m-%d")
yesterday = (datetime.date.today()-datetime.timedelta(days=1)).strftime("%Y-%m-%d")

url = "https://www.liveevent.nu/fabege_7/fabege_7_1280.jpg"
dir = "./images/"

#Get latest image
def get_image():
  try:
    # Get the image content from the url
    response = requests.get(url)
    # Check if the response is successful
    if response.status_code == 200:
      return response.content
    else:
      # Log an error message with the status code
      logging.error(f"Image could not be retrieved: {response.status_code}")
  except requests.exceptions.RequestException as e:
    # Log an error message with the exception
    logging.error(f"Image could not be requested: {e}")

#Get store image
def store_image():
  # Get the current date as a string
  try:
    # Open a file with the date as the name and write mode
    with open(dir + today + ".jpg", "wb") as file:
      # Write the image content to the file
      file.write(get_image())
      # Log a debug message
      logging.debug("Image stored successfully.")
  except IOError as e:
    # Log an error message with the exception
    logging.error(f"Image could not be written to file: {e}")
 
def check_similarity():
  if os.path.exists(dir + today + ".jpg"):
    todays_image = cv2.imread(dir + today + ".jpg")
    yesterdays_image = cv2.imread(dir + yesterday + ".jpg")
    new_image = cv2.imdecode(np.frombuffer(get_image(), np.uint8), cv2.IMREAD_COLOR)

    # Calculate the histograms of the input images
    todays_hist = cv2.calcHist([todays_image], [0], None, [256], [0, 256])
    yesterdays_hist = cv2.calcHist([yesterdays_image], [0], None, [256], [0, 256])
    new_histogram = cv2.calcHist([new_image], [0], None, [256], [0, 256])

    # Normalize the histograms computed above for the input images
    cv2.normalize(todays_hist, todays_hist, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX)
    cv2.normalize(yesterdays_hist, yesterdays_hist, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX)
    cv2.normalize(new_histogram, new_histogram, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX)

    # Compare these normalized histograms using cv2.compareHist()
    current_correlation = cv2.compareHist(todays_hist, yesterdays_hist, cv2.HISTCMP_CORREL)
    new_correlation = cv2.compareHist(new_histogram, yesterdays_hist, cv2.HISTCMP_CORREL)
    logging.debug("New score: {new_score}, old score: {old_score}".format(new_score=new_correlation,old_score=current_correlation))
    if new_correlation > current_correlation:
      store_image()
  else:
    store_image()

if __name__ == "__main__":
  if len(sys.argv) > 1 and sys.argv[1] == "--similar":
    check_similarity()
  else:
    store_image()
