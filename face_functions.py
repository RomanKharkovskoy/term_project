from itertools import count
import json
import os
import cv2
import numpy as np
from PIL import Image
import face_recognition
import time

# Функция, которая добавляет эталонную фотографию(с ней будет сравниваться видео загруженное в ТГ)
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

def frame_count(temp):
    video = f"images_to_compare/{temp}.mp4"
    video_capture = cv2.VideoCapture(video)
    frame_array = []
    cur_vr = 0
    max_vr = 0
    frame_array_cur = []
    length = int(video_capture.get(cv2.CAP_PROP_FRAME_COUNT))
    while True:
        _, frame = video_capture.read()
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = small_frame[:, :, ::-1]
        first_face_location = face_recognition.face_locations(rgb_small_frame)
        if len(first_face_location) == 0:
            frame_array.append(0)
            if len(frame_array) == length:
                break
            continue
        else:
            frame_array.append(1)
            if len(frame_array) == length:
                break
            else:
                continue
    # print(frame_array)
    frame_array_cur.append([0, 0])
    for x in range(1,len(frame_array)):
        if frame_array[x-1] == 0 and frame_array[x] == 1:
            frame_array_cur.append([x, x])
        if frame_array[x-1] == 1 and frame_array[x] == 0:
            frame_array_cur[len(frame_array_cur)-1][1] = x-1
    for x in range(len(frame_array_cur)):
        cur_vr = frame_array_cur[x][1] - frame_array_cur[x][0]
        if max_vr < cur_vr:
            max_vr = cur_vr
            res = frame_array_cur[x]
    # print(res)
    # print(res[1] - res[0] + 1)
    return res[0], res[1] - res[0] + 1

# Функция, которая вырезает из видео 3 идеальных кадра
def save_src(temp, res, fin):
    video = f"images_to_compare/{temp}.mp4"
    video_capture = cv2.VideoCapture(video)
    have_face = False
    den = int(round(fin/3))
    length = int(video_capture.get(cv2.CAP_PROP_FRAME_COUNT))
    final = [even_frame * den for even_frame in range(3)]
    # print(final)
    fr_num = [even_frame + res for even_frame in final]
    # print(fr_num)
    while True:
        frame_id = int(round(video_capture.get(1)))
        _, frame = video_capture.read()
        if frame_id == fr_num[1]:
            cv2.imwrite(f"images_to_compare/scr{frame_id}.jpg", frame)
        if frame_id == length - 1:
            break
    return have_face

def discr_compare(known_enc, destination):
    image_to_compare = face_recognition.load_image_file(destination)  # загружаем фото которое надо сравнить
    image_to_compare_encoding = face_recognition.face_encodings(image_to_compare)[0]  # вычисляем дескриптор
    result = face_recognition.compare_faces([known_enc], image_to_compare_encoding, tolerance=0.5)  # получаем результат сравнения
    return result

def cleaning():
    os.remove('images_to_compare/scr3.jpg')
    os.remove('images_to_compare/scr6.jpg')
    os.remove('images_to_compare/scr9.jpg')

start_time = time.time()
a, b = frame_count("temp_video4")
save_src("temp_video4", a, b)

print("--- %s seconds ---" % (time.time() - start_time))