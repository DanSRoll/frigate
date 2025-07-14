import matplotlib.pyplot as plt
from astropy.io import fits
from astropy.visualization import simple_norm
from google.colab import drive
import numpy as np

fits_path = '/path/to/fits' #local path to fits folder

with fits.open(fits_path) as hdul:
    fits_data = hdul[0].data

data_mean = np.mean(fits_data)
data_std = np.std(fits_data)

vmin = data_mean - 0.5 * data_std
vmax = data_mean + 2 * data_std

norm = simple_norm(fits_data, 'linear', min_cut=vmin, max_cut=vmax)
#norm = simple_norm(fits_data, 'sqrt', min_cut=vmin, max_cut=vmax)
#norm = simple_norm(fits_data, 'log', min_cut=vmin, max_cut=vmax)
#norm = simple_norm(fits_data, 'asinh', min_cut=vmin, max_cut=vmax)

plt.figure(figsize=(10, 10))
plt.imshow(fits_data, cmap='gray', norm=norm)
#plt.colorbar()
plt.axis('off')
plt.show()