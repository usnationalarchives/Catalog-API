import requests, json, time, csv, os, datetime, os.path, urllib.request, sys, glob
from os import mkdir
from os import path


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
print('Enter a one-word name for your query: ')
topic = input()

print('Enter your API query (everything that follows https://catalog.archives.gov/api/v2/records/search?): ',end='')
query = input()


# Creates a directory named "objects" where downloaded files will be stored.
if not os.path.exists(topic):
    mkdir(topic)

searchAfter = '*'
page_count = 0
more_pages = True
while more_pages:
    
# Performs an API query to return the description NAID that was entered
    j = json.loads(requests.get('https://catalog.archives.gov/api/v2/records/search?limit=100&searchAfter=' + searchAfter + '&availableOnline=true&q=' + query, headers=headers).text)
    statusCode = j['statusCode']
    if statusCode == 200:
        hits = j['body']['hits']['hits']
        if len(hits) == 0:
            more_pages = False
        else:
# Parses out the digital object metadata returned for the NAID and saves the object URL values to a new csv.
            for hit in hits:
                record = hit['_source']['record']
                if 'digitalObjects' in record:
                    digitalObjects = record['digitalObjects']
                    for digitalObject in digitalObjects:
                        parentNaId = str(record['naId'])
                        url = str(digitalObject['objectUrl'])

                        allItems = ((parentNaId, url, ))
                       
                        with open('ListOfObjectsToDownload_' + topic + '.csv','a', encoding='utf-8', newline='') as log :
                            writelog = csv.writer(log)
                            writelog.writerow(allItems)
                    with open('ListOfObjectsToDownload_' + topic + '.csv', 'r') as log:
                        readfile = csv.reader(log, delimiter=',')
                        for row in readfile:
                            parentNaId = row[0]
                            link = row[1]
                            
                            if path.exists(topic + '/' + parentNaId):
                                pass
                            else:
                                os.makedirs(topic + '/' + parentNaId)

                            link = link.strip()
                            name = link.rsplit('/')[-1]
                            filename = os.path.join(topic, parentNaId, name)

                            if not os.path.isfile(filename):
                                print('Downloading: ' + filename)
                                try:
                                    urllib.request.urlretrieve(link, filename)
                                except Exception as inst:
                                    print(inst)
                    f = open('ListOfObjectsToDownload_' + topic + '.csv', 'w')
                    f.write('')
                    f.close()
                else:
                    pass
            last_hit = hits[-1]
            next_search_after = last_hit['sort'][0]
            searchAfter = str(next_search_after)
            print('Last NAID on page ' + str(page_count) + ': ' + str(searchAfter))
            page_count +=1



print('All objects downloaded! ' + str(datetime.datetime.now().time()))
