
import cv2
import numpy as np

EDGE_COLOR = (0, 0, 0)
EDGE_THICKNESS = 2

def draw_rectangle(image, p1, p2, color, alpha, tag_text=""):

    # Fill rectangle
    overlay = image.copy()
    cv2.rectangle(image, p1, p2, color, -1)
    image = cv2.addWeighted(overlay, alpha, image, 1-alpha, 0)

    # Stroke rectangle
    cv2.rectangle(image, p1, p2, EDGE_COLOR, EDGE_THICKNESS)

    # Put Text
    width = abs(p2[0] - p1[0])
    font = cv2.FONT_HERSHEY_DUPLEX
    font_size = 0.5
    font_thickness = 1
    color_code = (0, 0, 0)
    shrinked = False

    while cv2.getTextSize(tag_text, font, font_size, font_thickness)[0][0] > width:
        if tag_text == "":
            break
        tag_text = tag_text[:-1]
        shrinked = True
    if shrinked:
        tag_text += ".."
    x = p1[0]
    y = max(p1[1] - 5, 0)
    cv2.putText(image, tag_text, (x, y), font, font_size, color_code, font_thickness)
    return image

def draw_polygon(image, points, color, alpha):
    """ Fill and stroke polygon
    Args:
        img (np.ndarray): Image array.
        points (list): List of points like (x, y)
        color (list): List of RGB.
        alpha (float) Alpha value. Value must be between 0 and 1.
    Returns:
        (np.ndarray): Drawed Image.
    """
    # Fill polygon
    overlay = image.copy()
    points = np.array(points).reshape([-1, 1, 2]).astype(np.int32)
    cv2.fillPoly(image, [points], color)
    image = cv2.addWeighted(overlay, alpha, image, 1-alpha, 0)

    # Stroke lines
    cv2.polylines(image, [points], True, EDGE_COLOR, EDGE_THICKNESS)
    return image