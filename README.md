# Real-Time Motion Detection and Alert System

This project is a real-time motion detection system that uses OpenCV to monitor video from the default camera. When it detects significant motion in the video, it captures an image of the frame, sends an email with the image attached, and cleans up the images folder.

![DEMO](https://i.imgur.com/UCKx85b.gif)
## Setup and Installation

### Requirements

- Python: You can download Python from [here](https://www.python.org/downloads/).
- OpenCV: Install it using pip: `pip install opencv-python`

### Installation Steps

1. Clone the repository to your local machine:

```bash
git clone https://github.com/phucleit96/python_camera_sensor_app_9.git
```
2. Navigate to the project directory:
3. Run the main.py script:
```python main.py```

# How the app Works
The script starts by capturing video from the default camera. Each frame is converted to grayscale and a Gaussian blur is applied. The script then calculates the absolute difference between the current frame and the first frame, applies a binary threshold, and dilates the result to fill in holes. Contours are then found in the dilated image.

If a contour is large enough, a bounding box is drawn around it on the frame, the status is updated, and the frame is saved as an image. The script also selects the middle image from all saved images.

If the status changes from 1 to 0 and an image was selected, a new thread is started to send an email with the selected image attached. Another thread is started to clean the images folder.

The cleaning process involves getting a list of all .png images in the images folder and removing each image. This is done to ensure that the images folder does not get filled up with unnecessary images.

Technologies Used
Python
OpenCV