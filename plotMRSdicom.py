'''
plotMRSdicom.py is designed to plot the spectrum of one or multiple MR spectroscopy dicom files and save the plot as
    png images on the hard drive

USAGE
    python plotMRSdicom.py

    After starting this meanMRSdicom.py you can select a folder containing dicom files and specify a prefix for those
    files an image should be generated and saved for or you can specify teh files manually. In this case you need to
    press cancel in the folder selection dialog.

OUTPUT
    A png image for each dicom file containing a plot of the spectrum.

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
import ntpath
import easygui

lstFilesDCM = []  # create an empty list

path = easygui.diropenbox(msg="Select folder containing MR spectroscopy dicom files to plot. (Press cancel to select one or multiple files manually.)")
if not path:
    files = easygui.fileopenbox(title='Select MR spectrsocopy dicom files to plot', multiple=True)
    lstFilesDCM = [x.encode('ascii') for x in files]
    PathDicom = os.path.dirname(os.path.abspath(lstFilesDCM[0]))
else:
    PathDicom = path.encode('ascii', 'ignore')
    prefix = easygui.enterbox("Enter prefix: ")
    for dirName, subdirList, fileList in os.walk(PathDicom):
        for filename in fileList:
            if ".dcm" in filename.lower():  # check for DICOM files
                if prefix in filename.lower():
                    lstFilesDCM.append(os.path.join(dirName, filename))

for i in range(int(len(lstFilesDCM))):
    print(i+1)
    D = dicom.read_file(lstFilesDCM[i])
    S = D.SpectroscopyData
    spec = np.asarray(S)
    Sreal = spec[0::2]
    Simag = spec[1::2]
    Slist = []
    for nn in range(len(Sreal)):
        Slist.append(complex(Sreal[nn], Simag[nn]))
    x = np.asarray(Slist)
    x1 = np.fft.fft(x)
    x1p = np.concatenate((np.flip(x1[0:len(x1) / 2], axis=0), np.flip(x1[len(x1) / 2:len(x1)], axis=0)), axis=0)

    plt.plot(x1p, 'k')
    plt.xticks(np.arange(0, 1023, step=511), (str(len(Sreal)), '0', str(len(Sreal)*-1)))
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Amplitude')
    p,fn = ntpath.split(lstFilesDCM[i])
    plt.title(fn)
    plt.savefig(lstFilesDCM[i]+'.png', bbox_inches='tight')
    plt.clf()
