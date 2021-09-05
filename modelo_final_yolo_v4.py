# functions detection objects

# import dependencies
from IPython.display import display
from darknet import *
from PIL import Image
import cv2
import argparse
import os
import glob




"""
  detect_objects_in_image: function to detect objects in image
  args:
    image_path: path image
    network: mo
"""


def detect_objects_in_image(image_path, network, class_names, class_colors, thresh=.5, show=False):
    width = network_width(network)
    height = network_height(network)
    darknet_image = make_image(width, height, 3)

    image = cv2.imread(image_path)
    print(image, image_path)
    original_height, original_width, foo = image.shape

    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image_resized = cv2.resize(image_rgb, (width, height),
                               interpolation=cv2.INTER_LINEAR)

    copy_image_from_bytes(darknet_image, image_resized.tobytes())
    detections = detect_image(network, class_names, darknet_image, thresh=thresh)
    free_image(darknet_image)
    image = draw_boxes(detections, image_resized, class_colors)

    # original resize image
    image = cv2.resize(image, (original_width, original_height),
                       interpolation=cv2.INTER_LINEAR)

    if show:
        display(Image.fromarray(image))

    return get_info(image_path, detections, class_names)


# get info detection image
def get_info(image_path, detections, class_names):
    image_name = os.path.splitext(os.path.split(image_path)[1])[0]
    detected_objects = [{'object': x[0], 'confidence': x[1], 'square_points': x[2]} for x in detections]
    list_objects = how_many_objects_in_image(detections, class_names)

    return {'image_name': image_name, 'detected_objects': detected_objects, 'quantity_objects': list_objects}

# count quantity objects by class
def how_many_objects_in_image(detections, class_names):
    list_objects = {x: 0 for x in class_names}
    for detection in detections:
        if detection[0] in class_names:
            list_objects[detection[0]] = list_objects[detection[0]] + 1

    return list_objects




# get args python command

parser = argparse.ArgumentParser()
parser.add_argument("--path_image", "-p", type=str, help="path image to detect violent objects")
parser.add_argument("--path_dir", "-d", type=str, help="path dir in where are the images to detect violent objects")

args = parser.parse_args()
path_image = args.path_image

# use function detect_objects_in_image
print(path_image,"------------------")
if path_image != None:
    network, class_names, class_colors = load_network("/model/yolov4/cfg/yolov4-custom.cfg",
                                                      "/model/yolov4/data/obj.data",
                                                      "/model/yolov4/data/yolov4-custom_best.weights")

    print(detect_objects_in_image(path_image, network, class_names, class_colors, thresh=.5, show=False))
else:
    print("No arguments")







