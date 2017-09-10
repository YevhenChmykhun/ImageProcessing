import argparse
import glob
from queue import Queue

from feature_detection.feature_detector import FeatureDetector, find_keypoints_and_descriptors

THREADS_NUMBER = 8

ap = argparse.ArgumentParser()
ap.add_argument('-qf', '--query_folder', required=True, help='Path to a folder with query images')
ap.add_argument('-tf', '--train_folder', required=True, help='Path to a folder with train images')
ap.add_argument("-df", "--destination_folder", required=True, help="Path to a folder in which save the result")
args = vars(ap.parse_args())

# find the keypoints and descriptors for all query images
query_images = []
for image_path in glob.glob(args['query_folder'] + '/*'):
    keypoints, descriptors = find_keypoints_and_descriptors(image_path)
    query_images.append(dict(keypoints=keypoints, descriptors=descriptors))

train_image_paths = Queue()
for image_path in glob.glob(args['train_folder'] + '/*'):
    train_image_paths.put(image_path)

for n in range(0, THREADS_NUMBER):
    thread = FeatureDetector(train_image_paths, query_images, args['destination_folder'])
    thread.start()

train_image_paths.join()
