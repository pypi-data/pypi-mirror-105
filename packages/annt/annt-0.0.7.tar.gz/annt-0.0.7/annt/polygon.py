
import cv2
import numpy as np

from . import utils

class Polygon():

    KEY_TAGIDX = "tagIdx"
    KEY_POSITION = "position"

    @classmethod
    def load(cls, obj, imgw, imgh, available_tags):
        """ Load a polygon objects from json formatted dictionary.
        Args:
            obj (dict)
            imgw (int)
            imgh (int)
            avalilable_tags (dict)
        Returns:
            (Polygon)
        """
        # Check input
        if cls.KEY_TAGIDX not in obj or cls.KEY_POSITION not in obj:
            raise ValueError("Invalid input. Insufficient tags.")

        # Load tag information.
        tagIdx = obj[cls.KEY_TAGIDX]
        if tagIdx not in available_tags:
            tag = None
        else:
            tag = available_tags[tagIdx]

        # Load position information
        points = obj[cls.KEY_POSITION]
        pol = Polygon(tagIdx, tag, imgw, imgh, points)
        return pol
    
    def __init__(self, idx, tag, iwidth, iheight, points):
        """ Constructor of the Polygon object.
        Args:
            idx (int): Tag idx.
            tag (str) Tag name.
            iwidth (int) Image width.
            iheight (int) Image height.
            points (list) List of coordination of polygon corners.
        """
        self.idx = idx
        self.tag = tag
        self.image_width = iwidth
        self.image_height = iheight
        self.points = points

    def show(self, img, color, new_width, new_height):
        """ Draw polygon to the image specfied as the first argument.
        """
        resized = self.resize(new_width, new_height)
        img = utils.draw_polygon(img, resized.points, color, 0.5)
        return img

    def resize(self, new_width, new_height):
        r_width = new_width / self.image_width
        r_height = new_height / self.image_height

        new_points = []
        for p in self.points:
            x = p[0] * r_width
            y = p[1] * r_height
            new_points.append([x, y])

        new_pol = Polygon(self.idx, self.tag, new_width, new_height, new_points)
        return new_pol

    def rotate(self, rot_m, new_width, new_height):
        point_matrix = []
        for p in self.points:
            point_matrix.append([p[0], p[1], 1])
        # Execute rotate
        point_matrix = np.array(point_matrix)
        point_rotated = rot_m.dot(point_matrix.T)
        x_ls = point_rotated[0]
        y_ls = point_rotated[1]

        new_points = []
        for x, y in zip(x_ls, y_ls):
            new_points.append([x, y])
        new_pol = Polygon(self.idx, self.tag, new_width, new_height, new_points)
        return new_pol

    def flip(self, flip_x, flip_y):
        # Copy points
        new_points = []
        for p in self.points:
            x = p[0]
            y = p[1]
            if flip_x:
                x = self.image_width - x
            if flip_y:
                y = self.image_height - y
            new_points.append([x, y])
        new_pol = Polygon(self.idx, self.tag, self.image_width, self.image_height, new_points)
        return new_pol