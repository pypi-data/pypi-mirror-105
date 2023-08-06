import cv2
import numpy as np


def roi(img, x1, x2, y1, y2):
    return img[x1:x2, y1:y2]
