import face_recognition
from PIL import Image, ImageDraw
import time

def face_rec():
    first_face_img = face_recognition.load_image_file("img/vitya.jpg")
    first_face_location = face_recognition.face_locations(first_face_img)

    print(first_face_location)
    print(len(first_face_location))

    pil_img1 = Image.fromarray(first_face_img)
    drow1 = ImageDraw.Draw(pil_img1)

    for (top, right, bottom, left) in first_face_location:
        drow1.rectangle(((left, top), (right, bottom)), outline=(9, 254, 7), width=4)

    del drow1
    pil_img1.save("img/new_1.jpg")


def extracting_faces(img_path):
    count = 0
    faces = face_recognition.load_image_file(img_path)
    faces_locations = face_recognition.face_locations(faces)

    for face_location in faces_locations:
        top, right, bottom, left = face_location

        face_img = faces[top:bottom, left:right]
        pil_img = Image.fromarray(face_img)
        pil_img.save(f"img/{count}_face_img.jpg")
        count += 1
    return f"found {count} face(s)"


def compare_faces(img1_path, img2_path):
    img1 = face_recognition.load_image_file(img1_path)
    img1_encodings = face_recognition.face_encodings(img1)[0]
    # print(img1_encodings)

    img2 = face_recognition.load_image_file(img2_path)
    img2_encodings = face_recognition.face_encodings(img2)[0]

    result = face_recognition.compare_faces([img1_encodings], img2_encodings)
    print(result)


def main():
    start_time = time.time()
    # face_rec()
    print(extracting_faces("img/vitya3.jpg"))
    # compare_faces("img/.jpg", "img/vova1.jpg")
    print("--- %s seconds ---" % (time.time() - start_time))


if __name__ == '__main__':
    main()