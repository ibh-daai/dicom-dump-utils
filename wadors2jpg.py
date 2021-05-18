# Sometimes your WADO-RS implementation may NOT support returning of JPEG renders. This script fills the gap by download the DICOM instance and exporting it to JPEG on local disk.
# Search for "TODO" to find spots you need to fill out
# Loops though a list of studies from a PostgreSQL table

import sys, os, datetime, psycopg2.extras
from requests.auth import HTTPBasicAuth
from dicomweb_client.api import DICOMwebClient
from dicomweb_client.session_utils import create_session_from_auth

jpgBase = '/path/to/jpg-exports/'
cmdPath = '/path/to/dcm4che-5.23.2/bin/dcm2jpg'
dcmPath = '/tmp/temp-image.dcm'

if __name__ == '__main__':
    auth = HTTPBasicAuth('TODO_dicomweb_username', 'TODO_dicomweb_password')
    session = create_session_from_auth(auth)
    client = DICOMwebClient(url="http://TODO.endpoint.to/wadors", session=session)

    pgconn = psycopg2.connect("host='TODO_pghost' dbname='TODO_pgdb' user='TODO_pguser' password='TODO_pgpass' client_encoding='UTF8'")
    pgconn.autocommit = True
    pgsql = pgconn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    pgsql.execute("select study_id, uid from study where jpg_exported='f' order by study_id limit 10")
    rows = pgsql.fetchall()
    total = len(rows)
    i = 0;

    print(datetime.datetime.now(), flush=True)

    for row in rows:
        i += 1
        if ((i % 100) == 0):
            print("%.2f percent complete" % (i * 100 / total), flush=True)

        instances = client.retrieve_study(row['uid'])

        for dicom in instances:
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

            # Write to a local DICOM file
            dicom.save_as(dcmPath)

            # Create a folder
            destinationDir = f'{jpgBase}/{pid}/{acn}/'
            os.system('mkdir -p ' + destinationDir)
            fileName = seriesNum + '-' + seriesDesc.replace(' ', '-').replace('(', '').replace(')', '') + '.jpg'

            # Convert to JPG
            cmd = f"{cmdPath} {dcmPath} {destinationDir}{fileName}"
            # print(cmd)
            os.system(cmd)

            # Mark this exam as exported
            sql = f"UPDATE study SET tmp_jpg_exported='t' WHERE study_id='{row['study_id']}';"
            pgsql.execute(sql)

    print(datetime.datetime.now(), flush=True)
