"""
quality_assessment.py

Core image quality assessment module for
Contactless Fingerprint Authentication.

Author: Mohammed Shoaib
"""

import cv2
import numpy as np

def load_image(image_path: str):
    """
    Loads an image from disk.

    Args:
        image_path (str): Path to image.

    Returns:
        numpy.ndarray
    """

    image = cv2.imread(image_path)

    if image is None:
        raise ValueError(f"Could not read image: {image_path}")

    return image