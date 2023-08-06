
import numpy as np
from . import utils

class Box():

    KEY_TAGIDX = "tagIdx"
    KEY_POSITION = "position"

    """
    Properties:
        idx:
        tag:
        x: x-coordinate of left-top corner
        y: y-coordinate of left-top corner
        w: width of box
        h: height of box
        nx: normalized x
        ny: normalized y
        nw: normalized w
        nh: normalized h
        top: distance from top edge.
        bottom: distance from bottom edge.
        left: distance from left edge.
        right: distance from right edge.
        image_width: width of image.
        image_height: height of image.
        options: optional data dictionary
        ===REQUESTED TO IMPLEMENT===
        pose:
        truncated:
        difficult:
        occluded:
    """

    @classmethod
    def load(cls, obj, imgw, imgh, available_tags):
        """
        Args:
            obj (dict)
            imgw (int)
            imgh (int)
            avalilable_tags (dict)
        Returns:
            Box
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
        if len(obj[cls.KEY_POSITION]) != 4:
            raise ValueError("Invalid input. Position length must be 4.")
        x, y, w, h = obj[cls.KEY_POSITION]
        box = Box(tagIdx, tag, imgw, imgh, x, y, w, h)
        return box

    def __init__(self, idx, tag, iwidth, iheight, x, y, w, h):
        """
        Args:
            idx (int): color idx
            tag (str): tag name
            iwidth (int): image width
            iheight (int): image height
            x (int): x coordinate of lef-top corner.
            x (int): y coordinate of lef-top corner.
            w (int): width of the box.
            h (int): height of the box.
        """
        self.idx = idx
        self.tag = tag
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.image_width = iwidth
        self.image_height = iheight
        self.options = {}

    def __repr__(self):
        return f'Box - x: {self.x}, y: {self.y}, w: {self.w}, h: {self.h}'

    def __str__(self):
        return f'Box - x: {self.x}, y: {self.y}, w: {self.w}, h: {self.h}'

    def set_option(self, key, value):
        self.options[key] = value

    def get_option(self, key):
        if key in self.options:
            return self.options[key]
        return  None

    def show(self, img, color, new_width, new_height):
        resized = self.resize(new_width, new_height)
        x1 = int(resized.x)
        y1 = int(resized.y)
        x2 = int(resized.x + resized.w)
        y2 = int(resized.y + resized.h)
        img = utils.draw_rectangle(img, (x1, y1), (x2, y2), color, 0.5, self.tag)
        return img

    def resize(self, new_width, new_height):
        """ Create copy and resize with specified rate.
        Args:
            r_width: rate of new_width / old_width.
            r_height: rate of new_height / old_height.
        """
        r_width = new_width / self.image_width
        r_height = new_height / self.image_height
        x = int(self.x * r_width)
        y = int(self.y * r_height)
        w = int(self.w * r_width)
        h = int(self.h * r_height)
        new_box = Box(self.idx, self.tag, new_width, new_height, x, y, w, h)
        return new_box

    def rotate(self, rot_m, new_width, new_height):
        """
        Args:
            rotation_matrix (np.array)
        """
        coord_arr = np.array([
            [self.x, self.y, 1],  # Left-Top
            [self.x, self.y+self.h, 1],  # Left-Bottom
            [self.x+self.w, self.y, 1],  # Right-Top
            [self.x+self.w, self.y+self.h, 1],  # Right-Botto
        ])
        new_coord = rot_m.dot(coord_arr.T)
        x_ls = new_coord[0]
        y_ls = new_coord[1]
        x = int(min(x_ls))
        y = int(min(y_ls))
        w = int(max(x_ls) - x)
        h = int(max(y_ls) - y)
        new_box = Box(self.idx, self.tag, new_width, new_height, x, y, w, h)
        return new_box

    def flip(self, flip_x, flip_y):
        x = self.left
        y = self.top
        if flip_x:
            x = self.right
        if flip_y:
            y = self.bottom
        new_box = Box(self.idx, self.tag, self.image_width, self.image_height, x, y, self.w, self.h)
        return new_box

    @property
    def top(self):
        return self.y

    @top.setter
    def top(self, value):
        prev_bottom = self.y + self.h
        self.y = value
        self.h = prev_bottom - self.y

    @property
    def right(self):
        return self.image_width - self.x - self.w

    @right.setter
    def right(self, value):
        self.w = self.image_width - value - self.x

    @property
    def bottom(self):
        return self.image_height - self.y - self.h

    @bottom.setter
    def bottom(self, value):
        self.h = self.image_height - value - self.y

    @property
    def left(self):
        return self.x 

    @left.setter
    def left(self, value):
        prev_right = self.x + self.w
        self.x = value
        self.w = prev_right - self.x

    @property
    def nx(self):
        return self.x / self.image_width
    
    @nx.setter
    def nx(self, value):
        self.x = value * self.image_width

    @property
    def ny(self):
        return self.y / self.image_height

    @ny.setter
    def ny(self, value):
        self.y = value * self.image_height

    @property
    def nw(self):
        return self.w / self.image_width

    @nw.setter
    def nw(self, value):
        self.w = value * self.image_width

    @property
    def nh(self):
        return self.h / self.image_height

    @nh.setter
    def nh(self, value):
        self.h = value * self.image_height
