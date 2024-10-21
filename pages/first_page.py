import streamlit as st
import cv2
import numpy as np
from PIL import Image

# Checkbox to enable/disable the camera
enable = st.checkbox("Enable camera")

# Capture a frame from the webcam, disabled if the checkbox is not checked
webcam_input = st.camera_input("Capture a frame from your webcam:", disabled=not enable)

# If a frame is captured, apply the circle overlay and display it
if webcam_input:
    # Convert the webcam input to an OpenCV image
    img = Image.open(webcam_input)
    img = np.array(img)

    # Get the dimensions of the image
    height, width, _ = img.shape

    # Define the center and radius for the circle
    center = (width // 2, height // 2)
    radius = min(height, width) // 4

    # Define the color (BGR format for OpenCV)
    color = (0, 255, 0)  # Green color
    thickness = 5  # Thickness of the circle

    # Draw the circle on the image
    img_with_circle = cv2.circle(img.copy(), center, radius, color, thickness)

    # Display the image with the overlayed circle
    st.image(img_with_circle, channels="RGB")
