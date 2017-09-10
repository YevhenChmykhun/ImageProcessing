import os
from threading import Thread

import cv2

from util.util import copy_file

FLANN_INDEX_KDTREE = 0
LOWE_RATIO = 0.7
MIN_MATCH_COUNT = 3


def find_keypoints_and_descriptors(image_path):
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    # find the keypoints and descriptors with SIFT
    sift = cv2.xfeatures2d.SIFT_create()
    return sift.detectAndCompute(image, None)


def retain_best(matches):
    good = []
    for m, n in matches:
        if m.distance < LOWE_RATIO * n.distance:
            good.append(m)
    return good


class FeatureDetector(Thread):
    def __init__(self, train_image_paths, query_images, destination_folder):
        Thread.__init__(self)
        self.train_image_paths = train_image_paths
        self.query_images = query_images
        self.destination_folder = destination_folder
        self.daemon = True

    def run(self):
        # FLANN parameters
        index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
        search_params = dict(checks=100)

        flann = cv2.FlannBasedMatcher(index_params, search_params)

        while True:
            train_image_path = self.train_image_paths.get()
            print(train_image_path)
            self.detect(flann, train_image_path)
            self.train_image_paths.task_done()

    def detect(self, flann, train_image_path):
        keypoints, descriptors = find_keypoints_and_descriptors(train_image_path)

        for query_image in self.query_images:
            matches = flann.knnMatch(descriptors, query_image['descriptors'], k=2)

            # store all the good matches as per Lowe's ratio test.
            best = retain_best(matches)

            if len(best) >= MIN_MATCH_COUNT:
                dest_path = os.path.join(self.destination_folder, train_image_path.rsplit('\\', 1)[-1])
                copy_file(train_image_path, dest_path)
