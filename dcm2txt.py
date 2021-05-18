# Takes a list of DICOM files, loops through them and uses dcm4che's dcm2txt to dump the header to TXT files (using a simple incremental number as the file name)

import sys, os, datetime, pydicom

dicomBase = '/path/to/dicom-files/'
txtBase = '/path/to/text-exports/'
cmdPath = '/path/to/dcm4che-2.0.29/bin/dcm2txt -w 120 '

if __name__ == '__main__':
    if(len(sys.argv) < 1):
        print("USAGE: python dcm2txt.py dicom-file-list.txt")
        exit();

    listFile = open(sys.argv[1])
    i = 0;
    print(datetime.datetime.now())
    # loop through the .dcm images listed in the supplied text files
    for dcmPath in listFile:
        # Open the DICOM, get important attributes
        dcmPath = dcmPath.rstrip('\n') # remove training new line

        # Convert to TXT
        cmd = f"{cmdPath} {dcmPath} > {txtBase}{i}.txt"
        os.system(cmd)

        i += 1
        if( i > 1000 ): break;
    print(datetime.datetime.now())
