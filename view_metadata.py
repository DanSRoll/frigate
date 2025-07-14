from astropy.io import fits

file_path = '/path/to/fits' #local path to fits folder

with fits.open(file_path) as hdul:
    hdul.info()

    primary_hdu = hdul[0]

    print(primary_hdu.header)