'''
meanMRSdicom.py is designed to average the spectra of multiple dicom files and save at again as dicom file.
    [This can be usefull e.g. to check for outliers in the single averages (based on motion, signal loss etc) and
    average without the outliers and or in functional single average data to average over condition]

USAGE
    python meanMRSdicom.py

    After starting this meanMRSdicom.py you can select a folder containing dicom files and specify a prefix for those
    files which should be averaged or you can select files manually for averaging. For the second case you need to press
    cancel in the folder selection dialog.

OUTPUT
    A dicom file containing the averaged spectrum which can than be used as input for the analysis software (such as
    Tarquin, jMRUI, LCModel)

LICENCE
This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License (GPLv3) as published
by the Free Software Foundation;

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY.

AUTHOR
Michael Lindner
University of Reading, 2018
School of Psychology and Clinical Language Sciences
Center for Integrative Neuroscience and Neurodynamics
'''

try:
    import dicom
except:
    import pydicom as dicom

import os
import numpy as np
import matplotlib.pyplot as plt
import easygui

lstFilesDCM = []  # create an empty list

path = easygui.diropenbox(msg="Select folder containing MEGA PRESS single average dicom files. (Press cancel to select files manually.)")
if not path:
    files = easygui.fileopenbox(title='Select MR spectrsocopy dicom files to average', multiple=True)
    lstFilesDCM = [x.encode('ascii') for x in files]
    PathDicom = os.path.dirname(os.path.abspath(lstFilesDCM[0]))
    ver = 2
else:
    PathDicom = path.encode('ascii', 'ignore')
    prefix = easygui.enterbox("Enter prefix: ")
    ver = 1
    for dirName, subdirList, fileList in os.walk(PathDicom):
        for filename in fileList:
            if ".dcm" in filename.lower():  # check for DICOM files
                if prefix in filename.lower():
                    lstFilesDCM.append(os.path.join(dirName, filename))


t = dicom.read_file(lstFilesDCM[0])
veclength = len(t.SpectroscopyData)

SPEC_data_array = np.empty((0, int(veclength/2)))

for i in range(int(len(lstFilesDCM))):
    print(i+1)
    D = dicom.read_file(lstFilesDCM[i])
    if i is 0:
        DCM = D
        sede = D.SeriesDescription

    SPEC = D.SpectroscopyData

    SPECarray = np.asarray(SPEC)
    SPECreal_single = SPECarray[0::2]
    SPECimag_single = SPECarray[1::2]

    SPEClist = []
    for nn in range(len(SPECreal_single)):
        SPEClist.append(complex(SPECreal_single[nn], SPECimag_single[nn]))

    cx = np.asarray(SPEClist)
    SPEC_data_array = np.append(SPEC_data_array, [cx], axis=0)

SPEC_mean_data_array = np.mean(SPEC_data_array, axis=0)


SPEC_real_mean = SPEC_mean_data_array.real
SPEC_imag_mean = SPEC_mean_data_array.imag

SPEC_out_vec = np.zeros((veclength))
SPEC_out_vec[0::2] = SPEC_real_mean
SPEC_out_vec[1::2] = SPEC_imag_mean


DCM.SpectroscopyData = SPEC_out_vec.tolist()
if ver == 1:
    outfilename = os.path.join(PathDicom, prefix + "_mean_" + sede + ".dcm")
else:
    outfilename = os.path.join(PathDicom, "mean_" + sede + ".dcm")

DCM.save_as(outfilename)

x1 = np.fft.fft(SPEC_mean_data_array)
x1p = np.concatenate((np.flip(x1[0:len(x1)/2], axis=0), np.flip(x1[len(x1)/2:len(x1)], axis=0)), axis=0)

plt.plot(x1p, 'k')
plt.title('averaged spectrum')
plt.show()


