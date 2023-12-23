# Build Camera Timelapse

This project is designed to automatically download images from a webcam on a schedule and save them to a specified folder. The images are then compiled into a timelapse video using ffmpeg. 

The primary use case of this project is to monitor and document changes in a specific location over time. For example, it can be used to capture the progress of a construction site, document the growth of a natural landscape, or observe changes in a public square. 

Optionally, you can set the script to compare the current image to the last image to minimize differences between two consecutive downloads. This helps to create a smoother timelapse video.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Installation

# Opt1. Python and ffmpeg installation
1. Install Python: Make sure you have Python installed on your system. You can download it from the official website: [https://www.python.org/downloads/](https://www.python.org/downloads/)
2. Install ffmpeg: ffmpeg is required for generating the timelapse video. You can download it from the official website: [https://ffmpeg.org/download.html](https://ffmpeg.org/download.html)
3. Clone the repository: Clone the repository that contains the `image_download.py`, `generate_timelapse.sh` and `requirements.txt` files.
4. Install Python dependencies: Navigate to the directory containing `requirements.txt` and run the following command to install the necessary Python dependencies:
pip install -r requirements.txt
5. Execute the scripts: You can now execute `image_download.py` and `generate_timelapse.sh` scripts as per your requirements.
6. For best result, put the scripts into a crontab to execute on a schedule.

# Opt2. Docker installation
1. Install Docker: Docker is required to build and run the Dockerfile. You can download Docker from the official website: [https://www.docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop)
2. Clone the repository: Clone the repository that contains the `Dockerfile` and `run_container.sh` files.
3. Build the Docker image: Navigate to the directory containing the `Dockerfile` and run the following command to build the Docker image:
docker build -t your_image_name .
4. Run the Docker container: After the Docker image has been built, you can run it using the following command:
./run_container.sh

## Usage

Modify the url varible in the image_download.py script to the url of the webcam you want to download images from. You can also modify the output directory and the filename of the downloaded images.

You can call the image_download.py script with the --similar flag to enable image comparison between the current image and the last downloaded image. This flag helps to minimize differences between consecutive downloads resulting in a smoother timelapse video.

Similarly, you can build the Dockerfile with the --similar flag to include the necessary configurations for image comparison in the Docker image.

## Contributing

Thank you for your interest in contributing to this project! As a single-person hobby project, contributions are not expected but always welcome. If you have any ideas, bug fixes, or improvements, feel free to submit a pull request.

To contribute to this project, please follow these guidelines:

1. Fork the repository and create a new branch for your contribution.
2. Make your changes and ensure that the code is clean and well-documented.
3. Test your changes thoroughly to ensure they do not introduce any regressions.
4. Submit a pull request, explaining the purpose and details of your contribution.

Please note that as a hobby project, there may be limited resources available for reviewing and merging pull requests. Your patience is appreciated.

Thank you for your support and happy coding!

## License

Please make sure that you are allowed to download images from the webcam you are using. The author of this project is not responsible for any legal issues that may arise from the use of this project. The url used in the example script is only for demonstration purposes and should not be used without permission.

The code in this project is licensed under the MIT License. See [LICENSE](LICENSE) file for details.

Please note that this project uses other libraries. The licenses for these libraries are as follows:

- Docker: Docker Engine software is released under the Apache 2.0 license.
- ffmpeg: ffmpeg is licensed under the LGPLv2.1 license.
- Libraries in `requirements.txt`:
  - requests: Apache License 2.0

Please respect the licenses for these libraries when using this project.

