import requests, json, time, csv, os, datetime, os.path, urllib.request, sys, glob, img2pdf, PyPDF2
from os import mkdir
from os import path
from PIL import Image
from PyPDF2 import PdfMerger, PdfReader

# Check if the user has the Catalog API key set as an environmental variable. If yes, the script will look for it there; if no, the user must enter their API Key when prompted.
print('Do you have your API Key set as an environmental variable (Y/N)?')
storedKey = input()
if storedKey == 'Y' or storedKey == 'y' or storedKey == 'Yes' or storedKey == 'yes':

    APIKey = os.environ.get('CATALOG_API_KEY')
else:
    print('Enter your API Key: ')
    APIKey = input()

headers = {
    'x-api-key': APIKey,
    }

print(datetime.datetime.now().time())



# Prompts user to enter the NAID of the description that contains the objects being downloaded.
print('File Unit or Item NAID: ',end='')
naId = input()

# Creates a directory named "objects" where downloaded files will be stored.
if not os.path.exists(naId):
    mkdir(naId)
    
# Performs an API query to return the description NAID that was entered
j = json.loads(requests.get('https://catalog.archives.gov/api/v2/records/search?naId_is=' + str(naId), headers=headers).text)

# Parses out the digital object metadata returned for the NAID and saves the object URL values to a new csv.
hits = j['body']['hits']['hits']
for hit in hits:
    record = hit['_source']['record']
    digitalObjects = record['digitalObjects']
    for digitalObject in digitalObjects:
        
        url = str(digitalObject['objectUrl'])



        allItems = ((url, ))
     
            
        with open('ListOfObjectsToDownload_' + naId + '.csv','a', encoding='utf-8', newline='') as log :
            writelog = csv.writer(log)
            writelog.writerow(allItems)

# Opens the csv listing the digital objects within the NAID and downloads them to the objects/ directory.
with open('ListOfObjectsToDownload_' + naId + '.csv', 'r') as log:
    readfile = csv.reader(log, delimiter=',')
    for row in readfile:
        link = row[0]

        link = link.strip()
        name = link.rsplit('/')[-1]
        filename = os.path.join(naId, name)

        if not os.path.isfile(filename):
            print('Downloading: ' + filename)
            try:
                urllib.request.urlretrieve(link, filename)
            except Exception as inst:
                print(inst)


print('All JPGs downloaded! ' + str(datetime.datetime.now().time()))
