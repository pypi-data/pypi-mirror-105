

import os
import json
import cv2
from . import color
from . import box, polygon
from .main import Annotation

# Constants
NAME_IMAGES_DIR = 'images'
NAME_ANNOTATION_DIR = 'annotations'
NAME_METAFILE = 'taginfo.json'

KEY_OBJECTS = 'objects'
KEY_TYPE = 'typ'
KEY_TAGS = 'tags'

OBJECT_MAPPER = {
    1: box.Box,
    2: polygon.Polygon,
}

def _load_meta(filepath):
    """ Load tag file

    Load tag inforation from specified json file and
    return tag name list and color index list.

    Args:
        filepath(str): Metafile filepath

    Returns:
        list, list: list of tag name list and color index list

    """
    with open(filepath) as fp:
        obj = json.load(fp)

    if not KEY_TAGS in obj.keys():
        raise RuntimeError('invalid format')

    color_idx_ls = []
    tag_name_ls = []
    for c in obj[KEY_TAGS]:
        color_idx = c['idx']
        tag_name = c['name']
        color_idx_ls.append(color_idx)
        tag_name_ls.append(tag_name)
    return tag_name_ls, color_idx_ls

def _load_image(filepath):
    """ Load image from specified filepath.

    Load image as np.ndarray. Loaded image is rotated
    according to exif meta data.

    Args:
        filepath(str): Image filepath

    Returns:
        np.ndarray
    """
    img = cv2.imread(filepath, cv2.IMREAD_COLOR)
    return img


def _load_annotation(filepath, img_width, img_height, available_tags={}):
    """ Load annotation information from specified filepath.

    Args:
        filepath(str): annotation filepath.
        img_width(int): Image width
        img_height(int): Image height
        available_tags(set, optional): This function read only the tags specified here.

    Returns:
        Annotation
    """
    contents = None
    with open(filepath, 'r') as fp:
        contents = json.load(fp)
    
    if KEY_OBJECTS not in contents:
        return None

    object_list = []
    for obj in contents[KEY_OBJECTS]:
        if obj[KEY_TYPE] not in OBJECT_MAPPER:
            print("Unknown object type")
            continue
        parser = OBJECT_MAPPER.get(obj[KEY_TYPE])
        new_obj = parser.load(obj, img_width, img_height, available_tags)
        object_list.append(new_obj)
    annotation = Annotation(None, None, object_list)
    return annotation

class Loader(object):
    """ Annotated image loader.
    """
    
    def __init__(self, project_dir):
        """ Constructor.
        Args:
            project_dir: path of project directory.
        """
        if not os.path.isdir(project_dir):
            raise IOError(f'{project_dir} not exists')
        self.project_dir = project_dir
        metapath = os.path.join(project_dir, NAME_METAFILE)

        # Load tag list.
        name_ls, idx_ls = _load_meta(metapath)
        self.num_classes = 0
        self.class_dict = {}
        self.class_idx_dict = { i:n for i, n in zip(idx_ls, name_ls)}
        self.color_map = {} # convert color_idx => rgb
        for name, class_idx in zip(name_ls, idx_ls):
            self.num_classes = max(self.num_classes, class_idx)
            self.class_dict[name] = class_idx 
            self.color_map[class_idx] = color.get_color(class_idx)

    def load(self):
        """ load annotation files.

        Args:
            dir_path (str): Annotation directory path.

        Yields:
            Annotation: Loaded Annotation object.
        """
        if not os.path.isdir(self.project_dir):
            raise IOError(f'{self.project_dir} not exists')

        image_dir = os.path.join(self.project_dir, NAME_IMAGES_DIR)
        annt_dir = os.path.join(self.project_dir, NAME_ANNOTATION_DIR)
        
        if not os.path.isdir(image_dir) or not os.path.isdir(annt_dir):
            raise IOError('image dir or annotation dir not exists')

        image_files = os.listdir(image_dir)
        annotation_files = set(os.listdir(annt_dir))

        # Iterate for all annotation files existing in the directory.
        for f in image_files:
            annt_file = f.split(".")[0] + ".json"
            if annt_file not in annotation_files:
                continue
            img = _load_image(os.path.join(image_dir, f))
            img_height, img_width, _ = img.shape
            ant = _load_annotation(os.path.join(annt_dir, annt_file), img_width, img_height, self.class_idx_dict)
            ant.update_colormap(self.color_map)
            ant.filename = f
            ant.image = img
            yield ant


def load(dir_path):
    """ load annotation files.

    Args:
        dir_path (str): Annotation directory path.

    Yields:
        Annotation: Loaded Annotation object.
    """
    if not os.path.isdir(dir_path):
        raise IOError(f'{dir_path} not exists')

    image_dir = os.path.join(dir_path, NAME_IMAGES_DIR)
    annt_dir = os.path.join(dir_path, NAME_ANNOTATION_DIR)
    metapath = os.path.join(dir_path, NAME_METAFILE)
    
    if not os.path.isdir(image_dir) or not os.path.isdir(annt_dir):
        raise IOError('image dir or annotation dir not exists')

    name_ls, idx_ls = _load_meta(metapath)
    tag_dict = { i:n for i, n in zip(idx_ls, name_ls)}
    color_map = {} # convert color_idx => rgb
    for n, ci in zip(name_ls, idx_ls):
        color_map[ci] = color.get_color(ci)
    del(name_ls)
    del(idx_ls)

    image_files = os.listdir(image_dir)
    annotation_files = set(os.listdir(annt_dir))

    # Iterate for all annotation files existing the directory.
    for f in image_files:
        annt_file = f.split(".")[0] + ".json"
        if annt_file not in annotation_files:
            continue
        img = _load_image(os.path.join(image_dir, f))
        img_height, img_width, _ = img.shape
        ant = _load_annotation(os.path.join(annt_dir, annt_file), img_width, img_height, tag_dict)
        ant.update_colormap(color_map)
        ant.filename = f
        ant.image = img
        yield ant

