import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
from astropy.visualization import simple_norm
import cv2

'''
This is a work-in-progress script with some issues that still need resolving!
'''

# Path to the FITS file
fits_path = '/path/to/difference/image.fits'

# Parameters
low_thresh = 50
high_thresh = 150
padding = 10

def load_fits_image(file_path):
    """Load a FITS file and return float32 image."""
    with fits.open(file_path) as hdul:
        return hdul[0].data.astype(np.float32)

def convert_to_uint8(image):
    """Convert float image to 8-bit uint8, normalised 0–255."""
    image = np.nan_to_num(image)
    image = np.clip(image, a_min=np.percentile(image, 5), a_max=np.percentile(image, 99.9))
    normed = (255 * (image - image.min()) / (image.max() - image.min())).astype(np.uint8)
    return normed

def find_bounding_box(image, padding=10):
    """Detect bounding box using Canny and dilation."""
    edges = cv2.Canny(image, low_thresh, high_thresh)
    dilated = cv2.dilate(edges, np.ones((3, 3), np.uint8), iterations=1)
    contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if not contours:
        return None

    x_min, y_min, w_min, h_min = cv2.boundingRect(contours[0])
    x_max = x_min + w_min
    y_max = y_min + h_min

    for contour in contours[1:]:
        x, y, w, h = cv2.boundingRect(contour)
        x_min = min(x_min, x)
        y_min = min(y_min, y)
        x_max = max(x_max, x + w)
        y_max = max(y_max, y + h)

    x_min = max(x_min - padding, 0)
    y_min = max(y_min - padding, 0)
    x_max = min(x_max + padding, image.shape[1])
    y_max = min(y_max + padding, image.shape[0])

    return x_min, y_min, x_max - x_min, y_max - y_min

def draw_bounding_box(image, bbox):
    """Draw a green bounding box on a grayscale image."""
    image_bgr = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
    x, y, w, h = bbox
    return cv2.rectangle(image_bgr, (x, y), (x + w, y + h), (0, 255, 0), 2)

# Load and convert the FITS difference image
original_float_image = load_fits_image(fits_path)
image_uint8 = convert_to_uint8(original_float_image)

# Detect bounding box
bbox = find_bounding_box(image_uint8, padding=padding)

if bbox:
    annotated = draw_bounding_box(image_uint8, bbox)

    # Display original (normalised) and annotated version
    norm = simple_norm(original_float_image, 'linear', min_cut=np.percentile(original_float_image, 5), max_cut=np.percentile(original_float_image, 99.9))

    fig, axes = plt.subplots(1, 2, figsize=(20, 10))
    axes[0].imshow(original_float_image, cmap='gray', norm=norm)
    axes[0].set_title("Original FITS Image")
    axes[0].axis('off')

    axes[1].imshow(cv2.cvtColor(annotated, cv2.COLOR_BGR2RGB))
    axes[1].set_title("Annotated Bounding Box")
    axes[1].axis('off')

    plt.tight_layout()
    plt.show()
else:
    print("No bounding box detected.")