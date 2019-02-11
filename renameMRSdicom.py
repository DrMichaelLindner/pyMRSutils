'''
renameMRSdicom.py is designed to rename all spectroscopy dicomfiles in the selected folder.

    USAGE
        python renameMRSdicom.py
        python renameMRSdicom.py -f <folder_name>

    INPUT
        -f:   folder name containing dicom files to rename. The input is optional: if not defined an input dialog
              will pop up to select the folder manually.

    OUTPUT
        renamed dicom files with a new filename structure:
        <patient_id> _ <series number> _ <instance number> _ <sequence name>.dcm

    BE AWARE: ORIGINAL DATA WILL BE DELETED!
           MAKE A COPY BEFORE RENAMING!!

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License (GPLv3) as published
by the Free Software Foundation

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY

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
import getopt
import sys
import easygui


def main():

    try:
        opts, args = getopt.getopt(sys.argv[1:], "hn:", ["help"])
    except getopt.GetoptError:
        print('python renameMRSdicom.py -f <folder name>')
        sys.exit(2)

    PathDicom = ''

    for o, a in opts:
        if o == "-n":
            PathDicom = a
        elif o in ("-h", "--help"):
            printhelp()
            sys.exit(2)

    if PathDicom == '':
        PathDicom = easygui.diropenbox(title='Select folder containing dicom files to anonymise')

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

        SN = dcm.SeriesNumber
        # AN = dcm.AcquisitionNumber
        IN = dcm.InstanceNumber
        ID = dcm.PatientID
        SD = dcm.SeriesDescription

        newname = ID + "_" + str(SN) + "_" + str(IN) + "_" + SD + ".dcm"
        newname = os.path.join(PathDicom, newname)

        os.rename(lstFilesDCM[i], newname)


def printhelp():
    helptext = """renameMRSdicom.py is designed to rename all spectroscopy dicomfiles in the selected folder.

    USAGE
        python renameMRSdicom.py 
        python renameMRSdicom.py -f <folder_name> 

    INPUT
        -f:   folder name containing dicom files to rename. The input is optional: if not defined an input dialog 
              will pop up to select the folder manually.
    
    OUTPUT
        renamed dicom files with a new filename structure:
        <patient_id> _ <series number> _ <instance number> _ <sequence name>.dcm
        
    BE AWARE: ORIGINAL DATA WILL BE DELETED!
           MAKE A COPY BEFORE RENAMING!!

    """
    print(helptext)

if __name__ == "__main__":
    main()