import argparse
import glob

import os

from util.util import copy_file

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-f", "--first_images_folder", required=True, help="Path to the first folder of images")
ap.add_argument("-s", "--second_images_folder", required=True, help="Path to the second folder of images ")
ap.add_argument("-d", "--result_destination", required=True, help="Path to the folder in which save the result")
args = vars(ap.parse_args())

# build a dict where key is an image name and value is a full path to that image
def build_dict(images_folder):
    d = {}
    for image_path in glob.glob(os.path.join(images_folder, "*")):
        key = image_path.rsplit(os.sep, 1)[-1]
        value = image_path
        d[key] = value
    return d


f = build_dict(args["first_images_folder"])
s = build_dict(args["second_images_folder"])

f_keys = set(f.keys())
s_keys = set(s.keys())

# find difference
diff = f_keys - s_keys


for key in diff:
    copy_file(f[key], os.path.join(args["result_destination"], key))
