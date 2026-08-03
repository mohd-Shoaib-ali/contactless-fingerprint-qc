"""
quality_assessment.py

Core image quality assessment module for
Contactless Fingerprint Authentication.

Author: Mohammed Shoaib
"""
import cv2
import numpy as np

# ==========================================================
# Default Threshold Configuration
# ==========================================================

DEFAULT_THRESHOLDS = {

    "blur": 5.0,

    "brightness_min": 50,

    "brightness_max": 210,

    "glare": 0.05,

    "roi": 0.15,

    "ridge": 15.0

}


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

def check_roi_completeness(
    image: np.ndarray,
    min_roi_ratio: float = 0.15
) -> dict:

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    blur = cv2.GaussianBlur(gray, (5,5), 0)

    _, thresh = cv2.threshold(
        blur,
        0,
        255,
        cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )

    kernel = np.ones((5,5), np.uint8)

    clean = cv2.morphologyEx(
        thresh,
        cv2.MORPH_OPEN,
        kernel
    )

    contours, _ = cv2.findContours(
        clean,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    if len(contours) == 0:

        return {

            "roi_ratio":0.0,

            "roi_complete":False

        }

    largest = max(contours, key=cv2.contourArea)

    area = cv2.contourArea(largest)

    total = image.shape[0] * image.shape[1]

    roi_ratio = area / total

    return {

        "roi_ratio": round(float(roi_ratio),4),

        "roi_complete": bool(roi_ratio >= min_roi_ratio)

    }


def check_ridge_clarity(
    image: np.ndarray,
    threshold: float = 15.0
) -> dict:
    """
    Estimate ridge clarity using a Gabor filter.

    Parameters
    ----------
    image : numpy.ndarray
        Input BGR image.

    threshold : float
        Minimum acceptable ridge score.

    Returns
    -------
    dict
    """

    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Create Gabor kernel
    kernel = cv2.getGaborKernel(
        (21, 21),      # kernel size
        5.0,           # sigma
        np.pi / 4,     # theta
        10.0,          # lambda
        0.5,           # gamma
        0              # psi
    )

    # Apply filter
    filtered = cv2.filter2D(
        gray,
        cv2.CV_64F,
        kernel
    )

    # Response variance
    ridge_score = np.var(filtered) / 100.0

    return {

        "ridge_score": round(float(ridge_score), 2),

        "ridges_clear": bool(ridge_score >= threshold)

    }

def normalize_scores(
    blur,
    brightness,
    glare,
    roi,
    ridge
):

    n_blur = min(1.0, blur["blur_score"] / 50.0)

    n_brightness = max(
        0.0,
        1.0 - abs(brightness["brightness"] - 128.0) / 128.0
    )

    n_glare = max(
        0.0,
        1.0 - glare["glare_ratio"] / 0.05
    )

    n_roi = min(
        1.0,
        roi["roi_ratio"] / 0.35
    )

    n_ridge = min(
        1.0,
        ridge["ridge_score"] / 100.0
    )

    return {

        "blur": n_blur,

        "brightness": n_brightness,

        "glare": n_glare,

        "roi": n_roi,

        "ridge": n_ridge

    }

def calculate_composite_score(scores):

    composite = (

        0.25 * scores["blur"] +

        0.15 * scores["brightness"] +

        0.15 * scores["glare"] +

        0.20 * scores["roi"] +

        0.25 * scores["ridge"]

    )

    return round(composite * 100,1)

def quality_gate(image_or_path):

    # Accept either image path or numpy array
    if isinstance(image_or_path, str):
        image = load_image(image_or_path)
    else:
        image = image_or_path

    # Validate image
    if image is None:
        raise ValueError("Invalid image supplied.")

    blur = check_blur(
        image,
        DEFAULT_THRESHOLDS["blur"]
    )

    brightness = check_brightness(
        image,
        DEFAULT_THRESHOLDS["brightness_min"],
        DEFAULT_THRESHOLDS["brightness_max"]
    )

    glare = check_glare(
        image,
        DEFAULT_THRESHOLDS["glare"]
    )

    roi = check_roi_completeness(
        image,
        DEFAULT_THRESHOLDS["roi"]
    )

    ridge = check_ridge_clarity(
        image,
        DEFAULT_THRESHOLDS["ridge"]
    )

    normalized = normalize_scores(
        blur,
        brightness,
        glare,
        roi,
        ridge
    )

    composite = calculate_composite_score(normalized)

    hard_failure = (
        blur["is_blurry"]
        or brightness["too_dark"]
        or brightness["too_bright"]
        or glare["has_glare"]
        or not roi["roi_complete"]
        or not ridge["ridges_clear"]
    )

    passed = composite >= 60 and not hard_failure

    if blur["is_blurry"]:
        guidance = "Image is blurry. Hold the phone steady."
    elif brightness["too_dark"]:
        guidance = "Image is too dark. Increase lighting."
    elif brightness["too_bright"]:
        guidance = "Image is too bright. Reduce lighting."
    elif glare["has_glare"]:
        guidance = "Glare detected. Tilt your finger."
    elif not roi["roi_complete"]:
        guidance = "Move your finger closer to the camera."
    elif not ridge["ridges_clear"]:
        guidance = "Fingerprint ridges are unclear."
    else:
        guidance = "Good capture - ready for processing."

    return {
        "passed": passed,
        "composite_score": composite,
        "normalized_scores": normalized,
        "blur": blur,
        "brightness": brightness,
        "glare": glare,
        "roi": roi,
        "ridge": ridge,
        "guidance": guidance
    }