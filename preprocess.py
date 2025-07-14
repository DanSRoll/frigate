import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
from scipy.ndimage import gaussian_filter
from pathlib import Path

# User-defined input and output directories
# Set these paths before running the script
base_dir = Path("/path/to/fits")        # Directory containing all FITS files
output_dir = Path("/path/to/output")        # Output directory for processed PNGs
output_dir.mkdir(parents=True, exist_ok=True)

# Number of neighbouring frames on each side used for background subtraction
num_adj = 10

def load_fits(file_path):
    """
    Load a FITS file and return the image data as float32
    """
    with fits.open(file_path) as hdul:
        data = hdul[0].data
        return data.astype(np.float32)

def subtract_background(current_index, files, num_adj=10, sigma=5):
    """
    Estimate and subtract the median background using surrounding frames.
    A Gaussian blur is applied to the median background to reduce artefacts.
    """
    start = max(0, current_index - num_adj)
    end = min(len(files), current_index + num_adj + 1)
    surrounding = [load_fits(files[i]) for i in range(start, end) if i != current_index]

    if len(surrounding) == 0:
        return None

    raw_background = np.median(surrounding, axis=0)
    background = gaussian_filter(raw_background, sigma=sigma)
    target = load_fits(files[current_index])
    result = target - background
    return np.clip(result, a_min=0, a_max=None)

def sharpen_image(image, sigma=10, strength=10):
    """
    Apply unsharp masking to enhance local contrast and sharpen features.
    """
    blurred = gaussian_filter(image, sigma=sigma)
    sharpened = image + (image - blurred) * strength
    return np.clip(sharpened, 0, 65535)

all_fits_files = sorted(base_dir.rglob("*.fits"))
print(f"Found {len(all_fits_files)} FITS files.")

# Only process if enough frames are available
if len(all_fits_files) < 2 * num_adj + 1:
    print("Not enough frames to perform background subtraction.")
else:
    for i in range(num_adj, len(all_fits_files) - num_adj):
        file_path = all_fits_files[i]

        result = subtract_background(i, all_fits_files, num_adj=num_adj)
        if result is None:
            continue

        sharpened = sharpen_image(result, sigma=10, strength=10)

        # Stretch image contrast using percentile clipping
        vmin = np.percentile(sharpened, 5)
        vmax = np.percentile(sharpened, 99.9)

        # Save as PNG using matplotlib
        output_file = output_dir / (file_path.stem + ".png")
        plt.figure(figsize=(10, 10))
        plt.imshow(sharpened, cmap='gray', vmin=vmin, vmax=vmax)
        plt.axis('off')
        plt.savefig(output_file, bbox_inches='tight', pad_inches=0, dpi=300)
        plt.close()

        print(f"Processed: {file_path.name} → {output_file.name}")