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


def check_blur(image: np.ndarray, threshold: float = 10.0) -> dict:
    """
    Detects whether an image is blurry using the
    Variance of Laplacian method.

    Parameters
    ----------
    image : numpy.ndarray
        Input BGR image.

    threshold : float
        Blur threshold.

    Returns
    -------
    dict
        Dictionary containing blur score and status.
    """

    # Convert image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Compute Laplacian
    laplacian = cv2.Laplacian(gray, cv2.CV_64F)

    # Variance of Laplacian
    blur_score = laplacian.var()

    return {
    "blur_score": round(float(blur_score), 2),
    "is_blurry": bool(blur_score < threshold)
}