
from . import box
from . import main
from . import color

import cv2
import numpy as np
import xml.etree.ElementTree as ET

TAG_ANNOTATION = "annotation"
TAG_FOLDER = "folder"
TAG_FILENAME = "filename"
TAG_PATH = "path"
TAG_SIZE = "size"
TAG_WIDTH = "width"
TAG_HEIGHT = "height"
TAG_DEPTH = "depth"
TAG_OBJECT = "object"

TAG_NAME = "name"
TAG_TRUNCATED = "truncated"
TAG_DIFFICULT = "difficult"
TAG_POSE = "pose"
TAG_OCCLUDED = "occluded"
TAG_BNDBOX = "bndbox"


"""
==========================
Utility functions
==========================
""" 
def find(tree, tag, text=False):
    result = tree.find(tag)
    if text:
        return result.text if result is not None else None
    else:
        return result

def find_and_check(tree, tag, text=False):
    result = tree.find(tag)
    if result is None:
        raise KeyError("Tag '{}' not found.")
    if text:
        return result.text
    return result

def findall_and_check(tree, tag):
    result = tree.findall(tag)
    if result is None:
        raise ValueError
    return result

def set_option(flag, obj, key, value):
    if flag:
        obj.set_option(key, value)


class PascalVOCLoader():

    def __init__(self):
        pass

    def load_all(self, dir_path):
        files = os.path.listdir(dir_path)
        for f in files:
            file_path = os.path.join(dir_path, f)
            if not os.path.isfile(file_path):
                continue
            with open(file_path, "r") as fp:
                text = fp.read()
            annotation = load_pascal_voc(text)
            yield annotation

    def load(self, path):
        pass


def load_pascal_voc(pascal_text, loader=None, use_options=True):
    """ Load annotation object from pascal_voc format annotation file.

    [Top level tag]
    Required
    * filename
    * size
    Optional
    * path
    * folder
    Ignore
    * source
    * owner
    * segmented

    [Object tag]
    Required
    * name
    * bndbox
    Optional

    Args:
        pascal_text (str): pasalVOC text data.
        loader (optional: function): Function load bytes of specified image.
    Returns:
        main.Annotation: Loaded annotation object.
    """

    # Initialize file loader
    if loader is None:
        loader = localfile_lodaer

    root = ET.fromstring(pascal_text)
    if root.tag != TAG_ANNOTATION:
        raise ValueError("Unknown format. PASCAL VOC format must start with 'annotation' tag.")

    # Load Requred tags
    filename = find_and_check(root, TAG_FILENAME, True)
    size = find_and_check(root, TAG_SIZE)
    size_width = float(find_and_check(size, TAG_WIDTH, True))
    size_height = float(find_and_check(size, TAG_HEIGHT, True))
    size_depth = float(find_and_check(size, TAG_DEPTH, True))

    # Define variables
    next_color_idx = 0
    name_to_idx = {}
    idx_to_color = {}

    # Iterate for all object section.
    objects = findall_and_check(root, TAG_OBJECT)
    object_list = []
    for obj in objects:
        # Required tag
        name = find_and_check(obj, TAG_NAME).text # tag name

        # Compute color idx
        if name not in name_to_idx:
            name_to_idx[name] = next_color_idx
            idx_to_color[next_color_idx] = color.get_color(next_color_idx)
            next_color_idx += 1
        color_idx = name_to_idx[name]

        # Create bounding box
        bndbox = find_and_check(obj, TAG_BNDBOX) 
        xmin = float(find_and_check(bndbox, "xmin", True))
        xmax = float(find_and_check(bndbox, "xmax", True))
        ymin = float(find_and_check(bndbox, "ymin", True))
        ymax = float(find_and_check(bndbox, "ymax", True))
        width = xmax - xmin
        height = ymax - ymin
        obj_box = box.Box(color_idx, name, size_width, size_height, xmin, ymin, width, height)

        # Options
        pose = find(obj, TAG_POSE, True)
        truncated = find(obj, TAG_TRUNCATED, True)
        difficult = find(obj, TAG_DIFFICULT, True)
        occluded = find(obj, TAG_OCCLUDED, True) # exist since pascal VOC 2008 ~
        set_option(use_options, obj_box, TAG_DIFFICULT, difficult)
        set_option(use_options, obj_box, TAG_POSE, pose)
        set_option(use_options, obj_box, TAG_OCCLUDED, occluded)
        set_option(use_options, obj_box, TAG_TRUNCATED, truncated)
        object_list.append(obj_box)

    # Load image
    if size_depth == 1:
        image = loader(filename, cv2.IMREAD_IGNORE_ORIENTATION | cv2.IMREAD_GRAYSCALE)
    elif size_depth == 3:
        image = loader(filename, cv2.IMREAD_IGNORE_ORIENTATION | cv2.IMREAD_COLOR)
    else:
        raise ValueError("Unknown depth {}".format(size_depth))

    if image is None:
        raise FileNotFoundError("'{}' is not found.".format(filename))

    # Generate Annotation
    annotation = main.Annotation(filename, image, boxes=object_list)

    # Load Optional tags
    folder = find(root, TAG_FOLDER, True)
    path = find(root, TAG_FILENAME, True)
    set_option(use_options, annotation, TAG_FOLDER, folder)
    set_option(use_options, annotation, TAG_PATH, path)
    annotation.update_colormap(idx_to_color)
    return annotation


def localfile_loader(filepath, flags):
    """ Load image from local storage.
    Args:
        filepath (str)
        flags (int): opencv2 flag.
    Returns:
        ndarray
    """
    image = cv2.imread(filename, flags)
    return image

class COCOLoader():

    def __init__(self):
        pass

    def load_all(self, dir_path):
        files = os.path.listdir(dir_path)
        for f in files:
            file_path = os.path.join(dir_path, f)
            if not os.path.isfile(file_path):
                continue
            with open(file_path, "r") as fp:
                text = fp.read()
            annotation = load_pascal_voc(text)
            yield annotation

    def load(self, path):
        pass

if __name__ == "__main__":
    unittest.main()