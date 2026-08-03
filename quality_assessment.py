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

def check_brightness(
    image: np.ndarray,
    min_threshold: float = 50,
    max_threshold: float = 210
) -> dict:
    """
    Measure image brightness using mean grayscale intensity.

    Parameters
    ----------
    image : numpy.ndarray
        Input BGR image.

    min_threshold : float
        Minimum acceptable brightness.

    max_threshold : float
        Maximum acceptable brightness.

    Returns
    -------
    dict
    """

    # Convert image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Compute average brightness
    brightness = float(np.mean(gray))

    return {

        "brightness": round(brightness, 2),

        "too_dark": bool(brightness < min_threshold),

        "too_bright": bool(brightness > max_threshold)

    }


def check_glare(
    image: np.ndarray,
    max_glare_ratio: float = 0.05
) -> dict:
    """
    Detect glare using overexposed pixel ratio.

    Parameters
    ----------
    image : numpy.ndarray
        Input BGR image.

    max_glare_ratio : float
        Maximum acceptable glare ratio.

    Returns
    -------
    dict
    """

    # Convert image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Count pixels brighter than 240
    glare_pixels = np.sum(gray > 240)

    # Total pixels
    total_pixels = gray.size

    # Compute glare ratio
    glare_ratio = glare_pixels / total_pixels

    return {

        "glare_ratio": round(float(glare_ratio), 4),

        "has_glare": bool(glare_ratio > max_glare_ratio)

    }