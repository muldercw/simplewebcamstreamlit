import streamlit as st
import streamlit.components.v1 as components
import base64
from io import BytesIO
from PIL import Image
import numpy as np

# Function to apply transformations to the image
def transform_image(image_data):
    img = Image.open(BytesIO(image_data))
    
    # Example transformation: Convert the image to grayscale
    grayscale_img = img.convert('L')
    
    # Convert the transformed image back to base64 for display
    buffered = BytesIO()
    grayscale_img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
    
    return img_str

# JavaScript/HTML code for webcam capture with SVG overlay
html_code = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Webcam Capture with SVG Overlay</title>
    <style>
        body {
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
            background-color: #f0f0f0;
        }
        #camera {
            position: relative;
        }
        video, canvas {
            width: 100%;
            max-width: 500px;
        }
        #svg-overlay {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
        }
        #controls {
            display: flex;
            justify-content: center;
            margin-top: 10px;
        }
        #capture {
            padding: 10px 20px;
            font-size: 16px;
        }
        #captured-images {
            margin-top: 20px;
        }
        #captured-images img {
            display: block;
            max-width: 500px;
            margin-bottom: 10px;
        }
    </style>
</head>
<body>
    <div id="camera">
        <video id="video" autoplay playsinline></video>
        <canvas id="canvas" style="display: none;"></canvas>

        <!-- Inline SVG Overlay -->
        <svg id="svg-overlay" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 600">
            <g><path style="opacity:1" fill="#fe0000" d="M 329.5,230.5 C 328.3,236.04 326.633,241.54 324.5,247..."></path></g>
        </svg>
    </div>

    <div id="controls">
        <button id="capture">Capture</button>
    </div>

    <div id="captured-images"></div>

    <script>
        const video = document.getElementById('video');
        const canvas = document.getElementById('canvas');
        const captureButton = document.getElementById('capture');
        const capturedImages = document.getElementById('captured-images');

        navigator.mediaDevices.getUserMedia({ video: true }).then(stream => {
            video.srcObject = stream;
        });

        captureButton.addEventListener('click', async () => {
            const context = canvas.getContext('2d');
            canvas.width = video.videoWidth;
            canvas.height = video.videoHeight;
            context.drawImage(video, 0, 0, canvas.width, canvas.height);

            // Convert canvas to base64
            const dataUrl = canvas.toDataURL('image/png');

            // Send image to Streamlit for processing
            const response = await fetch('/process_image', {
                method: 'POST',
                body: JSON.stringify({ image: dataUrl }),
                headers: { 'Content-Type': 'application/json' }
            });

            const result = await response.json();
            const img = document.createElement('img');
            img.src = result.transformed_image;
            capturedImages.appendChild(img);
        });
    </script>
</body>
</html>
'''

# Display the HTML with webcam and overlay
components.html(html_code, height=700)

# Process the captured image from JavaScript
def process_image():
    data = st.experimental_get_query_params()  # Simulate endpoint

    if "image" in data:
        image_base64 = data["image"][0]
        image_data = base64.b64decode(image_base64.split(",")[1])  # Remove base64 header
        transformed_image = transform_image(image_data)
        st.write({"transformed_image": f"data:image/png;base64,{transformed_image}"})

# Add a hidden function call that runs on page load
st.experimental_set_query_params(image=st.text_input("Paste the image data here", value=""))

# Process the image if we have one
if st.experimental_get_query_params():
    process_image()
