
""" Core module of annt-python

This module provides functions related Boudning Box and Annotation information,
which are important for handling annotation information.
"""

import os
import json
import cv2
import numpy as np

from . import color
from . import utils
from . import box
from . import polygon


class Annotation():

    """
    Image and annotation information holder.

    Attributes:
        filename (str): filename of the image.
        image (np.ndarray): Image array in opencv2 format.
        boxes (list): List of box and polygon.
    """

    def __init__(self, filename, image, boxes=[]):
        self.filename = filename
        self.image = image
        self.boxes = boxes
        self.color_map = {}
        self.options = {}

    def __repr__(self):
        return self.filename

    def update_colormap(self, color_dict):
        """ Update color map.
        Args:
            color_dict (dict): Dictionary that convert color_idx => rgb
        """
        self.color_map = color_dict

    def set_option(self, key, value):
        self.options[key] = value

    def get_option(self, key):
        if key in self.options:
            return self.options[key]
        return None

    def show(self, max_width=500, max_height=500):
        """ Display image with annotation information.

        Notes:
            Press any key to close image window.
        """
        height, width, _ = self.image.shape

        if width/height > max_width/max_height:
            rate = max_width/width
        else:
            rate = max_height/height
        new_width = int(width * rate)
        new_height = int(height * rate)
        resized = cv2.resize(self.image, (new_width, new_height))

        # Resize boxes
        for obj in self.boxes:
            color = self.color_map.get(obj.idx, (0, 0, 0))
            resized = obj.show(resized, color, new_width, new_height)
        cv2.imshow(self.filename, resized)
        cv2.waitKey()

    def resize(self, width, height):
        """ Resize image to the spcified size.
        This method is non-destructive.

        Args:
            width(int): width
            height(int): height
        Returns:
            Annotate: Resized annotate object.
        """
        c_height, c_width = self.image.shape[:2]
        img = cv2.resize(self.image, (width, height))

        # Resize boxes.
        new_objects = []
        for obj in self.boxes:
            new_objects.append(obj.resize(width, height))

        new_ant = Annotation(self.filename, img, new_objects)
        new_ant.color_map = self.color_map
        return new_ant

    def rotate(self, angle):
        """ Rotate image at the specified angle.
        Create copy of itself and rotate.
        This method is non-destructive.

        Args:
            angle(int): Rotate angle (degree).

        Returns:
            Annotate: Rotated annotate object.

        """
        img = self.image.copy()
        h, w = img.shape[:2]

        r = np.radians(angle)
        s = np.abs(np.sin(r))
        c = np.abs(np.cos(r))

        # Compute image size after rotation.
        nw = int(c*w + s*h)
        nh = int(s*w + c*h)

        # Compute affine matrix and apply to image.
        center = (w/2, h/2)
        rot_m = cv2.getRotationMatrix2D(center, angle, 1.0)
        rot_m[0][2] = rot_m[0][2] + (nw - w) // 2
        rot_m[1][2] = rot_m[1][2] + (nh - h) // 2
        img = cv2.warpAffine(img, rot_m, (nw, nh), flags=cv2.INTER_CUBIC)

        new_objects = []
        for obj in self.boxes:
            new_objects.append(obj.rotate(rot_m, nw, nh))

        new_ant = Annotation(self.filename, img, new_objects)
        new_ant.color_map = self.color_map
        return new_ant

    def flip(self, flip_x=True, flip_y=False):
        """ Flip image.
        Thie method flip image by the axis given by argument.
        This method is non-destructive.

        Args:
            flip_x (bool, optional): Whether flip with x axis. Default True.
            flip_y (bool, optional): Whether flip with y axis. Default True.
        Returns:
            Annotate: Rotated annotate object.
        """
        ih, iw = self.image.shape[:2]
        img = self.image.copy()
        if flip_x:
            img = np.fliplr(img)
        if flip_y:
            img = np.flipud(img)

        # Flip boxes
        new_boxes = []
        for box in self.boxes:
            new_boxes.append(box.flip(flip_x, flip_y))
        new_ant = Annotation(self.filename, img, new_boxes)
        new_ant.color_map = self.color_map
        return new_ant


