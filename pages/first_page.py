import streamlit as st
import cv2
import numpy as np
from PIL import Image

def overlay_image_alpha(img, img_overlay, pos, alpha_mask):
    """Overlay `img_overlay` on top of `img` at the position `pos` and blend using `alpha_mask`."""
    x, y = pos

    # Image ranges
    y1, y2 = max(0, y), min(img.shape[0], y + img_overlay.shape[0])
    x1, x2 = max(0, x), min(img.shape[1], x + img_overlay.shape[1])

    # Overlay ranges
    y1o, y2o = max(0, -y), min(img_overlay.shape[0], img.shape[0] - y)
    x1o, x2o = max(0, -x), min(img_overlay.shape[1], img.shape[1] - x)

    # Exit if there's nothing to overlay
    if y1 >= y2 or x1 >= x2 or y1o >= y2o or x1o >= x2o:
        return

    # Blend overlay within the determined range
    img_crop = img[y1:y2, x1:x2]
    img_overlay_crop = img_overlay[y1o:y2o, x1o:x2o]
    alpha = alpha_mask[y1o:y2o, x1o:x2o, np.newaxis] / 255.0

    img_crop[:] = (1.0 - alpha) * img_crop + alpha * img_overlay_crop

st.title("Webcam with Transparent PNG Overlay")

# Checkbox to enable/disable the camera
enable = st.checkbox("Enable camera")

# Capture a frame from the webcam, disabled if the checkbox is not checked
webcam_input = st.camera_input("Capture a frame from your webcam:", disabled=not enable)

# If a frame is captured, apply the PNG overlay
if webcam_input:
    # Convert the webcam input to an OpenCV image
    img = Image.open(webcam_input)
    img = np.array(img)

    # Load your transparent PNG image
    overlay = Image.open("overlay_image.png").convert("RGBA")
    overlay = np.array(overlay)

    # Separate the color and alpha channels of the PNG image
    overlay_img = overlay[:, :, :3]  # Color
    overlay_alpha = overlay[:, :, 3]  # Alpha channel (transparency)

    # Position to overlay (center of the captured image)
    pos = ((img.shape[1] - overlay_img.shape[1]) // 2, (img.shape[0] - overlay_img.shape[0]) // 2)

    # Overlay the PNG onto the captured image
    overlay_image_alpha(img, overlay_img, pos, overlay_alpha)

    # Display the image with the overlay
    st.image(img, channels="RGB")
