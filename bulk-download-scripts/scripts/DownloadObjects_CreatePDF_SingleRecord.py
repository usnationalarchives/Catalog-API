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


print('All files downloaded! ' + str(datetime.datetime.now().time()))

print('Checking for JPGs:')
# Checks for the presence of JPGs - if only TIFs were downloaded, JPG renditions will be generated.

os.chdir(naId)
yourpath = os.getcwd()

for root, dirs, files in os.walk(yourpath, topdown=False):
    for name in files:
        print(name)
        if os.path.splitext(os.path.join(root, name))[1].lower() == ".tif" or ".jp2":
                if os.path.isfile(os.path.splitext(os.path.join(root, name))[0] + ".jpg"):
                    print("A jpeg file already exists for %s" % name)
                # If a jpeg is *NOT* present, create one from the tiff.
                else:
                    outfile = os.path.splitext(os.path.join(root, name))[0] + ".jpg"
                    try:
                        im = Image.open(os.path.join(root, name))
                        print("Generating jpeg for %s" % name)
                        im.thumbnail(im.size)
                        im.save(outfile, "JPEG", quality=100)
                    except(Exception, e):
                        print(e)

print('Compressing JPGs:')
# Compresses the downloaded images to manage the size of the PDF that will be created. Compressed files will be stored in a subfolder of the "objects" directory. 
if not os.path.exists('Compressed'):
    mkdir('Compressed')

def compressMe(file, verbose=False):
    filepath = os.path.join(os.getcwd(), file)
    oldsize = os.stat(filepath).st_size
    picture = Image.open(filepath)
    dim = picture.size
    
    #set quality= to the preferred quality. 
    #Original script creator found that 85 has no difference in their 6-10mb files and that 65 is the lowest reasonable number
    #I am using 45 and it seems to work...
    picture.save("Compressed/Compressed_"+file,"JPEG",optimize=True,quality=45) 
    
    newsize = os.stat(os.path.join(os.getcwd(),"Compressed/Compressed_"+file)).st_size
    percent = (oldsize-newsize)/float(oldsize)*100
    if (verbose):
        print("File compressed from {0} to {1} or {2}%".format(oldsize,newsize,percent))
    return percent

def main():
    verbose = False
    #checks for verbose flag
    if (len(sys.argv)>1):
        if (sys.argv[1].lower()=="-v"):
            verbose = True

    #finds present working dir
    pwd = os.getcwd()

    tot = 0
    num = 0
    for file in os.listdir(pwd):
        if os.path.splitext(file)[1].lower() in ('.jpg', '.jpeg'):
            num += 1
            tot += compressMe(file, verbose)
    print("Average Compression: %d" % (float(tot)/num))
    print("Done")

if __name__ == "__main__":
    main()

print('All done compressing!' + str(datetime.datetime.now().time()))

print('Creating PDFs and combining into one:')

# Converts compressed images into PDF files.
os.chdir('..')

for filename in sorted(glob.glob(naId + '/Compressed/*.[jJ][pP][gG]')):

    img_path = filename
    pdf_path = filename[:-4] + '.pdf'

    image = Image.open(img_path)

    pdf_bytes = img2pdf.convert(image.filename)

    file = open(pdf_path, 'wb')

    file.write(pdf_bytes)

    image.close()

    file.close()

print('Successfully created individual pdf files!  ' + str(datetime.datetime.now().time()))

print('Merging PDFs...')
# Merges the PDF files into a single file with the NAID as the filename. It wll be found in the objects/Compressed/ directory.

input_directory = (naId + '/Compressed')
output_directory = naId

max_file_size = 500 * 1024 * 1024 # 100MB

current_size = 0
split_number = 1

output_pdf = PyPDF2.PdfMerger()

for filename in sorted(glob.glob(os.path.join(input_directory, '*.pdf'))):
    with open(filename, 'rb') as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)

        if current_size + os.path.getsize(filename) <= max_file_size:
            output_pdf.append(pdf_reader)
            current_size += os.path.getsize(filename)
        else:
            output_path = os.path.join(output_directory, naId + f'_split_{split_number}.pdf')
            with open(output_path, 'wb') as output_file:
                output_pdf.write(output_file)

            current_size = os.path.getsize(filename)
            split_number += 1
            output_pdf = PyPDF2.PdfMerger()
            output_pdf.append(pdf_reader)

if current_size > 0:
    output_path = os.path.join(output_directory, naId + f'_split_{split_number}.pdf')
    with open(output_path, 'wb') as output_file:
        output_pdf.write(output_file)
                      

print('Successfully merged pdf files!  ' + str(datetime.datetime.now().time()))
