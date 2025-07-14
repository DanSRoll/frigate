import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
from astropy.io.fits import PrimaryHDU
from astropy.visualization import simple_norm
from pathlib import Path

def load_and_process_sequence(fits_dir, start_filename, num_frames, output_fits_path, output_png_path=None):
    """
    Generate an average difference image from a sequence of FITS frames.

    Parameters:
    - fits_dir (Path): Directory containing the FITS files.
    - start_filename (str): Filename of the first frame in the sequence.
    - num_frames (int): Number of consecutive frames to use.
    - output_fits_path (Path): Path to save the output difference image as a FITS file.
    - output_png_path (Path, optional): Path to save the difference image as a PNG for quick inspection.

    Returns:
    - diff_image (ndarray): The computed average difference image.
    """

    fits_dir = Path(fits_dir)
    output_fits_path = Path(output_fits_path)

    # Get a sorted list of all .fits files
    fits_files = sorted(fits_dir.glob('*.fits'))

    # Locate the start index
    start_index = next((i for i, path in enumerate(fits_files) if path.name == start_filename), None)
    if start_index is None:
        raise ValueError(f"Start file {start_filename} not found in {fits_dir}")

    end_index = min(start_index + num_frames, len(fits_files))

    # Load the first frame to get the shape
    base_frame = fits.getdata(fits_files[start_index])
    diff_image = np.zeros_like(base_frame)

    # Accumulate absolute differences between adjacent frames
    for i in range(start_index + 1, end_index):
        current = fits.getdata(fits_files[i])
        previous = fits.getdata(fits_files[i - 1])
        diff_image += np.abs(current - previous)

    if end_index > start_index + 1:
        diff_image /= (end_index - start_index - 1)

    # Save as FITS
    hdu = PrimaryHDU(diff_image)
    hdu.writeto(output_fits_path, overwrite=True)

    # Optionally save as PNG (8-bit scaled for quick viewing)
    if output_png_path:
        from PIL import Image

        normed = np.clip(diff_image, a_min=0, a_max=None)
        normed = (255 * normed / normed.max()).astype(np.uint8)
        Image.fromarray(normed).save(output_png_path)

    # Display using percentile-based contrast stretch
    vmin = np.percentile(diff_image, 5)
    vmax = np.percentile(diff_image, 99.9)
    norm = simple_norm(diff_image, 'linear', min_cut=vmin, max_cut=vmax)

    plt.figure(figsize=(10, 10))
    plt.imshow(diff_image, cmap='gray', norm=norm)
    plt.title("Average Difference Image")
    plt.axis('off')
    plt.show()

    return diff_image

# Provide your paths below:
fits_directory = Path('/path/to/fits/')
start_frame = 'your_start_frame.fits'
frame_count = 25

output_fits = Path('/path/to/save/difference_image.fits')
output_png = Path('/path/to/save/difference_image.png')  # Optional PNG

# Run the function
difference_image = load_and_process_sequence(
    fits_dir=fits_directory,
    start_filename=start_frame,
    num_frames=frame_count,
    output_fits_path=output_fits,
    output_png_path=output_png
)