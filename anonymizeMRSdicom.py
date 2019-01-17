'''anonymizeMRSdicom.py is designed to anonmyse MR spectroscopy dicom files.

USAGE
    python anonymizeMRSdicom.py
    python anonymizeMRSdicom.py -f <folder_name>

INPUT
    -f:   folder name containing dicom files to anonymize. The input is optional: if not defined an input dialog
        will pop up to select the folder manually.

WARNING: ALL DICOM FILES WILL BE REPLACED WITH THE anonymizeD ONES: MAKE A COPY FIRST!

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
"""

'''

try:
    import dicom
except:
    import pydicom as dicom

import os
import getopt
import sys
import uuid
import easygui


def main():

    try:
        opts, args = getopt.getopt(sys.argv[1:], "hn:", ["help"])
    except getopt.GetoptError:
        print('python anonymizeMRSdicom.py -f <folder name>')
        sys.exit(2)

    PathDicom = ''

    for o, a in opts:
        if o == "-n":
            PathDicom = a
        elif o in ("-h", "--help"):
            printhelp()
            sys.exit(2)

    if PathDicom == '':
        PathDicom = easygui.diropenbox(title='Select folder containing dicom files to anonymize')


    lstFilesDCM = []  # create an empty list
    for dirName, subdirList, fileList in os.walk(PathDicom):
        for filename in fileList:
            if ".dcm" in filename.lower():  # check for DICOM files
                # if prefix in filename.lower():
                lstFilesDCM.append(os.path.join(dirName, filename))

    for i in range(int(len(lstFilesDCM))):
        print(lstFilesDCM[i])
        global dcm
        dcm = dicom.read_file(lstFilesDCM[i])

        # remove fields
        removefield(0x8, 0x14)
        removefield(0x8, 0x81)
        removefield(0x8, 0x92)
        removefield(0x8, 0x94)
        removefield(0x8, 0x1010)
        removefield(0x8, 0x1030)
        removefield(0x8, 0x3E)
        removefield(0x8, 0x1000)
        removefield(0x8, 0x1040)
        removefield(0x8, 0x1048)
        removefield(0x8, 0x1060)
        removefield(0x8, 0x1070)
        removefield(0x8, 0x1080)
        removefield(0x8, 0x2111)

        removefield(0x10, 0x32)
        removefield(0x10, 0x1000)
        removefield(0x10, 0x1001)
        removefield(0x10, 0x1010)
        removefield(0x10, 0x1020)
        removefield(0x10, 0x1030)
        removefield(0x10, 0x1090)
        removefield(0x10, 0x2160)
        removefield(0x10, 0x2180)
        removefield(0x10, 0x21B0)
        removefield(0x10, 0x4000)

        removefield(0x18, 0x1030)
        removefield(0x20, 0x4000)
        removefield(0x40, 0x275)
        removefield(0x40, 0xA730)
        removefield(0x88, 0x140)

        # create UIDs
        SOPInstanceUID = createuid()
        StudyUID = createuid()
        SeriesUID = createuid()
        FrameUID = createuid()
        SyncUID = createuid()
        SrUID = createuid()

        # change fields
        changefield(0x8, 0x18, SOPInstanceUID)
        changefield(0x8, 0x50, '')
        changefield(0x8, 0x80, '')
        changefield(0x8, 0x90, '')
        changefield(0x8, 0x1050, '')
        changefield(0x8, 0x1155, SOPInstanceUID)

        changefield(0x10, 0x10, '')
        changefield(0x10, 0x20, '')
        changefield(0x10, 0x30, '')
        changefield(0x10, 0x40, '')

        changefield(0x20, 0xD, StudyUID)
        changefield(0x20, 0xE, SeriesUID)
        changefield(0x20, 0x10, '')
        changefield(0x20, 0x52, FrameUID)
        changefield(0x20, 0x200, SyncUID)

        changefield(0x40, 0xA124, SrUID)
        changefield(0x40, 0x24, FrameUID)
        changefield(0x3006, 0xC2, FrameUID)

        dcm.save_as(lstFilesDCM[i])


def removefield(group, name):

    if (group, name) in dcm.keys():
        del dcm[group, name]


def changefield(group, name, value):

    if (group, name) in dcm.keys():
        dcm[group, name].value = value


def createuid():
    id = uuid.uuid1()
    uid = str(id.int)
    return uid


def printhelp():
    helptext = """anonymizeMRSdicom.py anonmyses MR spectroscopy dicom files.

    USAGE
        python anonymizeMRSdicom.py 
        python anonymizeMRSdicom.py -f <folder_name> 
        
    INPUT
        -f:   folder name containing dicom files to anonymize. The input is optional: if not defined an input dialog 
              will pop up to select the folder manually.
    
    OUTPUT
        Anonymized dicom files
    
    WARNING: ALL DICOM FILES WILL BE REPLACED WITH THE anonymizeD ONES: MAKE A COPY FIRST!
     
    """
    print(helptext)


if __name__ == "__main__":
    main()