import streamlit as st
import streamlit.components.v1 as components

# Custom HTML for webcam and SVG overlay
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

        <!-- Inline SVG Overlay with human head outline -->
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

        captureButton.addEventListener('click', () => {
            const context = canvas.getContext('2d');
            canvas.width = video.videoWidth;
            canvas.height = video.videoHeight;
            context.drawImage(video, 0, 0, canvas.width, canvas.height);
            const dataUrl = canvas.toDataURL('image/png');
            const img = document.createElement('img');
            img.src = dataUrl;
            capturedImages.appendChild(img);
        });
    </script>
</body>
</html>
'''

# Display the HTML with webcam and overlay
components.html(html_code, height=700)
