import requests, json, time, csv, os, datetime, os.path, urllib.request, sys, glob
from os import mkdir
from os import path
from PIL import Image


print(datetime.datetime.now().time())

# This section runs an API query that looks for all objects attached to file units within a specific series.
# It then writes the results to a json object, and from there the parent file unit NAID and each object URL is written to a csv. 
# The nextCursorMark is used in cases where there are more than 10,000 results - that is the maximum number of results our API can return at once. 

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

print('Parent NAID: ',end='')
naId = input()


searchAfter = '*'
page_count = 0
more_pages = True
while more_pages:
    
    j = json.loads(requests.get('https://catalog.archives.gov/api/v2/records/search?limit=25&searchAfter=' + searchAfter + '&availableOnline=true&ancestorNaId=' + str(naId), headers=headers).text)
    statusCode = j['statusCode']
    if statusCode == 200:
        hits = j['body']['hits']['hits']
        if len(hits) == 0:
            more_pages = False
        else:
            for hit in hits:
                record = hit['_source']['record']
                parentNaId = str(record['naId'])
                digitalObjects = record['digitalObjects']
                for digitalObject in digitalObjects:
                    url = str(digitalObject['objectUrl'])

                    allItems = (parentNaId, url)
                 
                        
                    with open('ListOfObjectsToDownload_' + naId + '.csv','a', encoding='utf-8', newline='') as log :
                        writelog = csv.writer(log)
                        writelog.writerow(allItems)
                        # This section takes the object URLs listed in the csv and downloads them into a separate folder for each file unit. The folder names are the file unit NAIDs.
                with open('ListOfObjectsToDownload_' + naId + '.csv', 'r') as log:
                    readfile = csv.reader(log, delimiter=',')
                    for row in readfile:
                        parentNaId = row[0]
                        link = row[1]
                        
                        if path.exists(naId + '/' + parentNaId):
                            pass
                        else:
                            os.makedirs(naId + '/' + parentNaId)

                        link = link.strip()
                        name = link.rsplit('/')[-1]
                        filename = os.path.join(naId, parentNaId, name)

                        if not os.path.isfile(filename):
                            print('Downloading: ' + filename)
                            try:
                                urllib.request.urlretrieve(link, filename)
                            except Exception as inst:
                                print(inst)
                f = open('ListOfObjectsToDownload_' + naId + '.csv', 'w')
                f.write('')
                f.close()

                                
                                
            last_hit = hits[-1]
            next_search_after = last_hit['sort'][0]
            searchAfter = str(next_search_after)
            print('Last NAID on page ' + str(page_count) + ': ' + str(searchAfter))
            page_count +=1
    else:
        print('Error, do something here...')
        more_pages = False




print('All Files downloaded! ' + str(datetime.datetime.now().time()))



            

    
