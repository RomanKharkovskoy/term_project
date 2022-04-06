import face_recognition
import numpy as np
import cv2

video_capture = cv2.VideoCapture("img/video.mp4")

while True:
    _, frame = video_capture.read()
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb_small_frame = small_frame[:, :, ::-1]
    first_face_location = face_recognition.face_locations(rgb_small_frame)
    if len(first_face_location) == 0:
        continue
    else:
        print("face found")
        break

