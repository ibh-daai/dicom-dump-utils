# Takes a list of DICOM files, loops through them and uses dcm4che's dcm2jpg to dump PNG exports using a folder path like /run-name/patient-id/accession-number/seriesNumber-seriesDescription.png
# Run name is there to segment/partition the exports (ie avoid having too many files in one folder)

import sys, os, datetime, pydicom

dicomBase = '/path/to/dicom-files/'
jpgBase = '/path/to/jpeg-exports/'
cmdPath = '/path/to/dcm4che-5.23.2/bin/dcm2jpg -F PNG -q 1.0'

if __name__ == '__main__':
    if(len(sys.argv) < 2):
        print("USAGE: python dcm2png.py dicom-file-list.txt run-name")
        #python3 dcm2png.py dicom-file-list.txt run1
        exit();

    listFile = open(sys.argv[1])
    runName = sys.argv[2]
    i = 0;
    print(datetime.datetime.now())
    # loop through the .dcm images listed in the supplied text files
    for dcmPath in listFile:
        # Open the DICOM, get important attributes
        dcmPath = dcmPath.rstrip('\n') # remove training new line
        dicom = pydicom.dcmread(dcmPath)
        pid = str(dicom.PatientID)
        acn = str(dicom.AccessionNumber)
        seriesDesc = "missing"
        if 'SeriesDescription' in dicom:
            seriesDesc = str(dicom.SeriesDescription)
        seriesNum = "x"
        if 'SeriesNumber' in dicom:
            seriesNum = str(dicom.SeriesNumber)

        # Check series description to eliminate laterals?!?
        if 'lat' in seriesDesc.lower():
            continue;

        # Create a folder
        destinationDir = f'{pngBase}{runName}/{pid}/{acn}/'
        #print(dcmPath + ' => ' + destinationDir)
        os.system('mkdir -p ' + destinationDir)
        fileName = seriesNum + '-' + seriesDesc.replace(' ','-').replace('(','').replace(')','') + '.png'

        # Convert to PNG
        cmd = f"{cmdPath} {dcmPath} {destinationDir}{fileName}"
        #print(cmd)
        os.system(cmd)

        i += 1
        #if( i > 10 ): break;
    print(datetime.datetime.now())
