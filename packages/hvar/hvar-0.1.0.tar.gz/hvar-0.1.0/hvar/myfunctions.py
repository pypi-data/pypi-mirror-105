import os
import tarfile
import shutil
from google.cloud import storage
import datetime
from googleapiclient import discovery
from googleapiclient import errors
from google.oauth2 import service_account
from google.auth.transport import requests
import requests
import json
import base64
import pandas as pd
from oauth2client.client import GoogleCredentials
from google.oauth2.service_account import Credentials as cdr


def jobupload(pypath):
    #Create directory

    path = os.getcwd()

    os.mkdir(path + '\\Job')
    os.mkdir(path + '\\Job\\trainer')

    #Create setup

    f = open(path + "\\Job" + "\\setup.py", "x")
    f.write("""
    from setuptools import find_packages
    from setuptools import setup

    REQUIRED_PACKAGES = ['Keras==2.0.4',
                         'h5py==2.7.0',
                         'tensorflow>=2.4.1',
                         'xgboost>=1.4.1'
                         ]

    setup(
        name='trainer',
        version='0.1',
        install_requires=REQUIRED_PACKAGES,
        packages=find_packages(),
        include_package_data=True,
        description='Keras trainer application'
    )
    """)
    f.close()

    #Create __init__.py

    f = open(path + "\\Job\\trainer" + "\\__init__.py", "x")

    #Create requirements.txt

    f = open(path + "\\Job" + "\\requirements.txt", "x")
    f.write("""
    tensorflow>=1.15.*,<2
    future==0.16.0
    h5py>=2.7.0,<3.0
    Keras>=2.2.4,<3.0
    numexpr>=2.6.8,<3.0
    pandas>=0.23.4,<1.0
    """)
    f.close()

    #move the python code to the directory
    files = [pypath]
    for f in files:
        shutil.copy(f, path + "\\Job\\trainer")

    #creating the tar file
    def tardir(path, tar_name):
        with tarfile.open(tar_name, "w:gz") as tar_handle:
            for root, dirs, files in os.walk(path):
                for file in files:
                    tar_handle.add(os.path.join(root, file))
    tardir('./Job', 'Job.tar.gz')

    #send through API
    base = open(path + '/Job.tar.gz', 'rb')
    base_read = base.read()
    base_64_encode = base64.encodebytes(base_read)
    base_64_decode = base64.decodebytes(base_64_encode) 
    
    url = 'http://127.0.0.1:8000/upload_job/'
    myobj = {"file": str(base_64_decode)}
    x = requests.post(url, json=myobj)

    #delete everything
    base.close()
    shutil.rmtree(path + "\\Job")
    os.remove(path + '\\Job.tar.gz')
    

    
    print('Job submitted')

def jobstatus(projectID, service_account_file):
    
    
    #Authenticate on GCP
    credentials = service_account.Credentials.from_service_account_file(service_account_file,
                                                               scopes=['https://www.googleapis.com/auth/cloud-platform'])

    request = google.auth.transport.requests.Request()

    credentials.refresh(request)
    cloudml = googleapiclient.discovery.build('ml', 'v1', credentials=credentials)


    #Making request
    request = cloudml.projects().jobs().list(parent='projects/' + projectID )
    response = request.execute()

    #Cleaning the data
    df = pd.DataFrame(response['jobs'])
    df.drop('trainingInput', axis=1, inplace=True)
    alldata = []
    for i in range(df.shape[0]):
        temp = df.iloc[i]
        alldata.append(dict(temp))

    return alldata