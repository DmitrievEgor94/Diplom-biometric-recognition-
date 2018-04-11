import cv2
import dlib
import numpy as np
import os

"Возвращает изображение с лицом"

predictor_path = 'shape_predictor_68_face_landmarks.dat'

detector = dlib.get_frontal_face_detector()
sp = dlib.shape_predictor(predictor_path)


def make_part_screen_dull(image):
    img = np.zeros((image.shape[0], image.shape[1]), np.uint8)
    cv2.circle(img, (image.shape[1]//2, image.shape[0]//2), min([image.shape[1], image.shape[0]])//4, 255, -1)

    points = np.where(img == 0)
    image[points] = image[points]/3

    cv2.putText(image, 'Put face in circle', (image.shape[1]//8, image.shape[0]//10), cv2.FONT_HERSHEY_COMPLEX,
                1, (255, 255, 255))

    center = (image.shape[1]//2, image.shape[0]//2)
    radius = min([image.shape[1], image.shape[0]])//4

    cv2.circle(image, center, radius, (0, 0, 255))

    left_x = center[1] - radius
    top_y = center[0] - radius
    right_x = center[1] + radius
    bottom_y = center[0] + radius

    return [left_x, top_y, right_x, bottom_y]


def find_face(image):
    image = cv2.resize(image, None, fx=0.6, fy=0.6, interpolation=cv2.INTER_AREA)
    img_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    orig_image_copy = image.copy()
    roi_of_face = make_part_screen_dull(orig_image_copy)

    cv2.imshow('image_with_rec', orig_image_copy)
    button = cv2.waitKey(4)

    if button == 13:
        img_rgb_for_detection = img_rgb[roi_of_face[0]:roi_of_face[2], roi_of_face[1]:roi_of_face[3]]

        dets = detector(img_rgb_for_detection, 1)

        if np.size(dets) == 0:
            print("Can't find face")
            return []

        final_image_with_face = dlib.get_face_chip(img_rgb_for_detection, sp(img_rgb_for_detection, dets[0]))

        dets = detector(final_image_with_face, 1)

        if np.size(dets) == 0:
            return final_image_with_face

        final_image_with_face = final_image_with_face[dets[0].top():dets[0].bottom(), dets[0].left():dets[0].right()]

        return final_image_with_face

    return []


def get_faces_from_camera(number_of_images, path_to_save):
    cap = cv2.VideoCapture(0)

    position_in_directory = 1

    if not os.path.exists(path_to_save):
        os.makedirs(path_to_save)
    else:
        position_in_directory = len(os.listdir(path_to_save))

    while number_of_images > 0:
        ret, frame = cap.read()

        found = find_face(frame)

        if len(found) != 0:
            gray_image = cv2.cvtColor(found, cv2.COLOR_BGR2GRAY)
            cv2.imshow('face', mat=gray_image)
            cv2.imwrite(path_to_save + '/' + str(position_in_directory)+'.png', gray_image)
            position_in_directory += 1
            number_of_images -= 1

get_faces_from_camera(5, 'faces/Egor')