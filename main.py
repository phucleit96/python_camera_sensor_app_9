# Import necessary libraries
import cv2
import time
from emailing import send_email
import glob
import os
from threading import Thread

# Start video capture from the default camera (camera index 0)
video = cv2.VideoCapture(0)

# Check if the video capture was successfully opened
if not video.isOpened():
    print("Could not open video")
    exit()

# Delay for 1 second to allow the camera to warm up
time.sleep(1)

# Initialize variables
first_frame = None
status_list = []
count = 1
image_with_object = None  # Initialize variable

# Define a function to clean the images folder
def clean_folder():
    print("Clean started")
    # Get a list of all .png images in the images folder
    images = glob.glob("images/*.png")
    # Remove each image
    for image in images:
        os.remove(image)
    print("Clean ended")

# Main loop
while True:
    status = 0
    # Read a frame from the video capture
    check, frame = video.read()

    # If the frame could not be read, break the loop
    if not check:
        break  

    # Convert the frame to grayscale
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Apply Gaussian blur to the grayscale frame
    gray_frame_gau = cv2.GaussianBlur(gray_frame, (21, 21), 0)

    # If this is the first frame, save it
    if first_frame is None:
        first_frame = gray_frame_gau

    # Calculate the absolute difference between the current frame and the first frame
    delta_frame = cv2.absdiff(first_frame, gray_frame_gau)
    # Apply a binary threshold to the difference
    thresh_frame = cv2.threshold(delta_frame, 60, 255, cv2.THRESH_BINARY)[1]
    # Dilate the thresholded image to fill in holes
    dil_frame = cv2.dilate(thresh_frame, None, iterations=2)
    # Find contours in the dilated image
    contours, _ = cv2.findContours(dil_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Loop over the contours
    for contour in contours:
        # If the contour is too small, ignore it
        if cv2.contourArea(contour) < 5000:
            continue
        # Get the bounding box of the contour
        x, y, w, h = cv2.boundingRect(contour)
        # Draw the bounding box on the frame
        rectangle = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
        # If a rectangle was drawn, update the status and save the frame as an image
        if rectangle.any():
            status = 1
            cv2.imwrite(f"images/{count}.png", frame)
            count += 1
            # Get a list of all images and select the middle one
            all_images = glob.glob("images/*.png")
            index = int(len(all_images) / 2)
            image_with_object = all_images[index] if all_images else None

    # Update the status list and keep only the last two statuses
    status_list.append(status)
    status_list = status_list[-2:]

    # If the status changed from 1 to 0 and an image was selected, start the email and clean threads
    if status_list[0] == 1 and status_list[1] == 0 and image_with_object is not None:
        email_thread = Thread(target=send_email, args=(image_with_object, ))
        email_thread.daemon = True
        clean_thread = Thread(target=clean_folder)
        clean_thread.daemon = True
        email_thread.start()
        clean_thread.start()

    # Display the frame
    cv2.imshow("Video", frame)
    # If the 'q' key is pressed, break the loop
    if cv2.waitKey(1) == ord("q"):
        break

# Release the video capture and close all windows
video.release()
cv2.destroyAllWindows()