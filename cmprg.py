import json
import os

import cv2
import face_recognition
import numpy as np
from PIL import Image


# Функция, которая добавляет эталонную фотографию(с ней будет сравниваться видео)
def extracting_faces(img_path, username):
    faces = face_recognition.load_image_file(img_path)
    faces_locations = face_recognition.face_locations(faces)

    for face_location in faces_locations:
        top, right, bottom, left = face_location

        face_img = faces[top:bottom, left:right]
        pil_img = Image.fromarray(face_img)
        pil_img.save(f"ideal_images/{username}.jpg")
    known_photo = face_recognition.load_image_file(f"ideal_images/{username}.jpg")
    known_encodings = np.array(face_recognition.face_encodings(known_photo)[0]).tolist()
    return json.dumps(known_encodings)

# Функция, которая вырезает из видео 3 идеальных кадра
def save_src(temp):
    video = f"images_to_compare/{temp}.mp4"
    video_capture = cv2.VideoCapture(video)
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
                    cv2.imwrite(f"images_to_compare/scr{count}.jpg", frame)
                count += 1
            else:
                break

def discr_compare(known_enc):
    image_to_compare = face_recognition.load_image_file("images_to_compare/scr9.jpg")  # загружаем фото которое надо сравнить
    image_to_compare_encoding = face_recognition.face_encodings(image_to_compare)[0]  # вычисляем дескриптор
    result = face_recognition.compare_faces([known_enc], image_to_compare_encoding, tolerance=0.5)  # получаем результат сравнения
    return result

def cleaning():
    os.remove('images_to_compare/scr3.jpg')
    os.remove('images_to_compare/scr6.jpg')
    os.remove('images_to_compare/scr9.jpg')


