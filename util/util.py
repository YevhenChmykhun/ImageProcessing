import glob
import os

import cv2


def copy_file(src_path, dest_path):
    with open(src_path, mode='rb') as src_file:  # b -> binary
        file_content = src_file.read()

        with open(dest_path, 'wb') as dest_file:
            dest_file.write(file_content)


def find_smallest_image(image_folder):
    minH = minW = None
    for imagePath in glob.glob(os.path.join(image_folder, "*")):
        image = cv2.imread(imagePath)

        if minH is None or (image is not None and hasattr(image, 'shape') and minH > image.shape[0]):
            minH = image.shape[0]

        if minW is None or (image is not None and hasattr(image, 'shape') and minW > image.shape[1]):
            minW = image.shape[1]
    return minH, minW
