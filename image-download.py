# Import the modules
import requests
import datetime
import logging
 
# Configure the logging level and format
logging.basicConfig(level=logging.WARNING, format="%(levelname)s: %(message)s")
 
# Define the function
def store_image(url):
  # Get the current date as a string
  date = datetime.date.today().strftime("%Y-%m-%d")
  try:
    # Get the image content from the url
    response = requests.get(url)
    # Check if the response is successful
    if response.status_code == 200:
      try:
        # Open a file with the date as the name and write mode
        with open(date + ".jpg", "wb") as file:
          # Write the image content to the file
          file.write(response.content)
          # Log a debug message
          logging.debug("Image stored successfully.")
      except IOError as e:
        # Log an error message with the exception
        logging.error(f"Image could not be written to file: {e}")
    else:
      # Log an error message with the status code
      logging.error(f"Image could not be retrieved: {response.status_code}")
  except requests.exceptions.RequestException as e:
    # Log an error message with the exception
    logging.error(f"Image could not be requested: {e}")
 
# Example usage
store_image("https://www.liveevent.nu/fabege_7/fabege_7_1280.jpg")