import face_recognition
import cv2
import time


def save_src():
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


def compare_faces():
    standard = face_recognition.load_image_file("img/0_face_img.jpg")
    standard_encodings = face_recognition.face_encodings(standard)[0]

    img1 = face_recognition.load_image_file("img/scr9.jpg")
    face_location_1 = face_recognition.face_locations(img1)

    if face_location_1 != 0:
        img1_encodings = face_recognition.face_encodings(img1)[0]
        result = face_recognition.compare_faces([standard_encodings], img1_encodings)
        print(result)

    else:
        img2 = face_recognition.load_image_file("img/scr6.jpg")
        face_location_2 = face_recognition.face_locations(img2)

        if face_location_2 != 0:
            img2_encodings = face_recognition.face_encodings(img2)[0]
            result = face_recognition.compare_faces([standard_encodings], img2_encodings)
            print(result)

        else:
            img3 = face_recognition.load_image_file("img/scr3.jpg")
            face_location_3 = face_recognition.face_locations(img3)

            if face_location_3 != 0:
                img3_encodings = face_recognition.face_encodings(img3)[0]
                result = face_recognition.compare_faces([standard_encodings], img3_encodings)
                print(result)


def main():
    start_time = time.time()
    save_src()
    compare_faces()
    print("--- %s seconds ---" % (time.time() - start_time))


if __name__ == '__main__':
    main()






