import streamlit as st
from streamlit_webrtc import webrtc_streamer
import av
import cv2

def video_frame_callback(frame):
    img = frame.to_ndarray(format="bgr24")
    
    cv2.putText(img, "Webcam Feed", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    return av.VideoFrame.from_ndarray(img, format="bgr24")

st.title("Webcam Stream using WebRTC")


webrtc_streamer(key="webcam", video_frame_callback=video_frame_callback)
