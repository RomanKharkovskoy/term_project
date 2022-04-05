from cv2 import cv2
import os


def take_screenshot():
    cap = cv2.VideoCapture("video.mp4")#Принимает в качестве параметра адрес на видео
    count = 0
    if not os.path.exists("dataset_from_video"):#это нужно будет усовершенствовать и сделать папки для каждого профиля в данной директории
        os.mkdir("dataset_from_video")

    while True:
        ret, frame = cap.read()
        fps = round(cap.get(cv2.CAP_PROP_FPS))
        print(fps)
        if ret:
            frame_id = int(round(cap.get(1)))
            print(frame_id)
            cv2.imshow("frame", frame)
            cv2.waitKey(50)

            if frame_id % 10 == 0: #тут каждый десятый кадр скриншотится(позже сделать зависимость от fps)
                cv2.imwrite(f"dataset_from_video/{count}.jpg", frame)
                print(f"Сделал скриншот {count}")
                count += 1 
        else:
            print("Ошибка. Не могу сделать скриншот!")#в конце ошибка это нормально, потому что заканчивается видео
            break

    cap.release()
    cv2.destroyAllWindows()    

take_screenshot()