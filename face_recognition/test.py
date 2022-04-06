import face_recognition
import numpy as np
import cv2

video_capture = cv2.VideoCapture("img/video_vitya.mp4")
count = 0

while True:
    frame_id = int(round(video_capture.get(1)))
    _, frame = video_capture.read()
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb_small_frame = small_frame[:, :, ::-1]
    first_face_location = face_recognition.face_locations(rgb_small_frame)
    if len(first_face_location) == 0:
        continue
    else:
        if count < 10:
            if count == 3 or count == 6 or count == 9:
                cv2.imwrite(f"img/scr{count}.jpg", frame)
                print(frame_id)
                print("face found")
            count += 1
        else:
            break




