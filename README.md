# frigate
Frigate: A Novel Dataset Comprising Wide Field-of-View Astronomical FITS Images of Low Earth Orbit Scenes for Machine Learning Applications

# Overview

This repository provides the associated pipeline for processing raw astronomical imaging data - specifically FITS files such as those in the frigate dataset (avaiable at: TBC)- into enhanced difference images suitable for streak detection and annotation. The data used typically consists of time-sequenced space surveillance images in .fits format, which may contain fast-moving orbital debris or artificial satellites represented as streaks.

The primary goal of this pipeline is to:  
	•	Load and inspect FITS image data  
	•	Extract and display metadata  
	•	Perform preprocessing steps including background leveling and contrast adjustment  
	•	Generate difference images from consecutive frames to isolate motion artifacts  
	•	(In development) Automatically detect and annotate streaks using edge detection and line fitting techniques.  

This system is useful in contexts such as optical space surveillance, orbital debris research, and training data generation for object detection models.

# File Descriptions

# display_image.py

Displays a FITS image with appropriate scaling for visual inspection. It uses percentile-based stretching to enhance visibility of dim features in the data. This is useful for quickly reviewing raw or processed images.

# view_metadata.py

Parses and prints the metadata (headers) of a FITS file. This allows researchers to inspect acquisition parameters such as observation time, exposure duration, telescope settings, and sensor information.

# preprocess.py

Applies image-level preprocessing to raw FITS data. This includes background subtraction, optional flat-field correction, and smoothing to improve the visibility of faint streaks or suppress fixed pattern noise. This prepares the data for more effective difference imaging.

# generate_difference_image.py

Computes an average difference image over a sequence of FITS frames. It highlights transient or moving objects - such as satellites or debris—by suppressing static background stars. The resulting image can be saved in both FITS and PNG formats for analysis or visualization.

# annotate.py

(In Progress)

This script is intended to perform automatic streak annotation using edge detection (e.g. Canny) and Hough line transforms. It will identify streak-like features in the difference image and output bounding boxes or masks for further processing or model training.
Note: As of this release, annotate.py is under active development and may not yet function reliably. Further updates are planned to improve robustness and accuracy.

⸻

# Requirements

The code was executed in a Conda enviroment using Jupyter Notebooks. To build a similar enviroment, please use the environment.yml file:

conda env create -f environment.yml

The scripts rely on a number of libraries, including the following:   
	•	numpy  
	•	matplotlib  
	•	opencv-python  
	•	astropy  
	•	scikit-image  

To install all required dependencies, you may use:

pip install -r requirements.txt
