# pyMRSutils
pyMRSutils contains some helpful python (2.7) tools for MRS dicom files:

## renameMRdicom.py
renames all spectroscopy dicomfiles in the selected folder.

 
USAGE
    python renameMRSdicom.py
    python renameMRSdicom.py -f <folder_name>


Outputs renamed dicom files with a new filename structure:
<patient_id> _ <series number> _ <instance number> _ <sequence name>.dcm


## meanMRdicom.py
averages the spectra of multiple dicom files and save at again as dicom file.
[This can be usefull e.g. to check for outliers in the single averages (based on motion, signal loss etc) and
average without the outliers and or in functional single average data to average over condition]


USAGE
    python meanMRSdicom.py

	
## anonmyseMRdicom
anonmyses MR spectroscopy dicom files


USAGE
    python anonymizeMRSdicom.py
    python anonymizeMRSdicom.py -f <folder_name>


## plotMRSdicom.py
plots the spectrum of one or multiple MR spectroscopy dicom files and save the plot as png images on the hard drive


USAGE
    python plotMRSdicom.py

	
outputs a png image for each selected dicom file containing a plot of the spectrum.
	

## *Dependencies*  
the utils are developed in python 2.7 and the following packages need to be installed: 
numpy, pydicom, matplotloib and easygui. 

    
## *License*  
This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License (GPLv3) as published
by the Free Software Foundation;

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
  
  
## *Author*
Michael Lindner  
University of Reading, 2019  
School of Psychology and Clinical Language Sciences  
Centre for Integrative Neuroscience and Neurodynamics
