import streamlit as st
import cv2
import numpy as np
from PIL import Image

overlay_path = "outline.png"

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

# Add custom CSS to overlay an image on all video elements
st.markdown(
    """
    <style>
    video {
        position: relative;
    }
    .video-overlay {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: url('outline.png') no-repeat center center;
        background-size: contain;
        pointer-events: none; /* Allow clicks to pass through */
    }
    </style>
    """,
    unsafe_allow_html=True
)

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
    overlay = Image.open(overlay_path).convert("RGBA")
    overlay = np.array(overlay)

    # Separate the color and alpha channels of the PNG image
    overlay_img = overlay[:, :, :3]  # Color
    overlay_alpha = overlay[:, :, 3]  # Alpha channel (transparency)

    # Resize the overlay to fit within the webcam image while maintaining aspect ratio
    overlay_height, overlay_width = overlay_img.shape[:2]
    img_height, img_width = img.shape[:2]

    # Calculate the scale factor to fit the overlay inside the image
    scale_factor = min(img_width / overlay_width, img_height / overlay_height)

    # Resize the overlay
    new_overlay_size = (int(overlay_width * scale_factor), int(overlay_height * scale_factor))
    overlay_img_resized = cv2.resize(overlay_img, new_overlay_size, interpolation=cv2.INTER_AREA)
    overlay_alpha_resized = cv2.resize(overlay_alpha, new_overlay_size, interpolation=cv2.INTER_AREA)

    # Position to overlay (center of the captured image)
    pos = ((img_width - overlay_img_resized.shape[1]) // 2, (img_height - overlay_img_resized.shape[0]) // 2)

    # Overlay the resized PNG onto the captured image
    overlay_image_alpha(img, overlay_img_resized, pos, overlay_alpha_resized)

    # Display the image with the overlay
    st.image(img, channels="RGB")
