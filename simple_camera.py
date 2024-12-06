# MIT License
# Copyright (c) 2019-2022 JetsonHacks

# Using a CSI camera (such as the Raspberry Pi Version 2) connected to a
# NVIDIA Jetson Nano Developer Kit using OpenCV
# Drivers for the camera and OpenCV are included in the base image

import cv2
import os
from datetime import datetime

""" 
gstreamer_pipeline returns a GStreamer pipeline for capturing from the CSI camera
Flip the image by setting the flip_method (most common values: 0 and 2)
display_width and display_height determine the size of each camera pane in the window on the screen
Default 1920x1080 displayd in a 1/4 size window
"""

def gstreamer_pipeline(
    sensor_id=0,
    capture_width=3280,
    capture_height=2464,
    display_width=3280,
    display_height=2464,
    framerate=30,
    flip_method=2,
):

    return (
        "nvarguscamerasrc sensor-id=%d ! "
        "video/x-raw(memory:NVMM), width=(int)%d, height=(int)%d, framerate=(fraction)%d/1 ! "
        "nvvidconv flip-method=%d ! "
        "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
        "videoconvert ! "
        "video/x-raw, format=(string)BGR ! appsink"
        % (
            sensor_id,
            capture_width,
            capture_height,
            framerate,
            flip_method,
            display_width,
            display_height,
        )
    )


def show_camera():
    window_title = "CSI Camera"
    # Save the videos and images to this location
    output_dir = os.path.expanduser("~/Pictures/csi_pictures/")
    os.makedirs(output_dir, exist_ok=True)  # Ensure the directory exists


    # To flip the image, modify the flip_method parameter (0 and 2 are the most common)
    print(gstreamer_pipeline(flip_method=2))
    video_capture = cv2.VideoCapture(gstreamer_pipeline(flip_method=0), cv2.CAP_GSTREAMER)
    if video_capture.isOpened():
        try:
            window_handle = cv2.namedWindow(window_title, cv2.WINDOW_AUTOSIZE)
            while True:
                ret_val, frame = video_capture.read()
                if not ret_val:
                    print("Error: Unable to capture video frame.")
                    break
                # Check to see if the user closed the window
                # Under GTK+ (Jetson Default), WND_PROP_VISIBLE does not work correctly. Under Qt it does
                # GTK - Substitute WND_PROP_AUTOSIZE to detect if window has been closed by user
                #if cv2.getWindowProperty(window_title, cv2.WND_PROP_AUTOSIZE) >= 0:
                # Show video feed
                cv2.imshow(window_title, frame)
                # Save video frame if recording
                if recording and video_writer is not None:
                    video_writer.write(frame)

                # Handle keypress events
                keyCode = cv2.waitKey(10) & 0xFF
                if keyCode == ord('q') or keyCode == 27:  # Quit on 'q' or ESC
                    break
                elif keyCode == ord('i'):  # Capture image on 'i'
                    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                    image_path = os.path.join(output_dir, f"image_{timestamp}.jpg")
                    cv2.imwrite(image_path, frame)
                    print(f"Image saved to {image_path}")
                elif keyCode == ord('1') and not recording:  # Start recording on '1'
                    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                    video_path = os.path.join(output_dir, f"video_{timestamp}.avi")
                    fourcc = cv2.VideoWriter_fourcc(*'XVID')  # Codec for AVI format
                    video_writer = cv2.VideoWriter(video_path, fourcc, 30, (frame.shape[1], frame.shape[0]))
                    recording = True
                    print(f"Started recording: {video_path}")
                elif keyCode == ord('0') and recording:  # Stop recording on '0'
                    recording = False
                    video_writer.release()
                    video_writer = None
                    print("Stopped recording.")
        finally:
            if video_writer is not None:
                video_writer.release()
            video_capture.release()
            cv2.destroyAllWindows()
    else:
        print("Error: Unable to open camera")

if __name__ == "__main__":
    show_camera()
