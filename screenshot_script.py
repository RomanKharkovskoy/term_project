from cv2 import cv2
import os

def take_screenshot(qwerty):
    cap = cv2.VideoCapture("cache/video.mp4")#Принимает в качестве параметра адрес на видео
    count = 0
    if not os.path.exists(f'{qwerty}'):#это нужно будет усовершенствовать и сделать папки для каждого профиля в данной директории
        os.mkdir(f'{qwerty}')

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
                cv2.imwrite(f"{qwerty}/{count}.jpg", frame)
                print(f"Сделал скриншот {count}")
                count += 1 
        else:
            # print("Ошибка. Не могу сделать скриншот!")#в конце ошибка это нормально, потому что заканчивается видео
            break

    cap.release()
    cv2.destroyAllWindows()    
