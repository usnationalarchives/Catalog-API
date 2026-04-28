import requests
import json
import csv
import os

# Function to retrieve API key
def get_api_key():
    api_key = os.environ.get('CATALOG_API_KEY')
    if api_key:
        return api_key
    else:
        print("Enter your API Key: ")
        return input().strip()

# Set up API key and base URL
API_KEY = get_api_key()
API_BASE_URL = "https://catalog.archives.gov/api/v2/records/search"

# Function to retrieve all availableOnline NAIDs and their digital object URLs
def fetch_naids_and_digital_objects(series_naid):
    headers = {'x-api-key': API_KEY}
    search_after = '*'
    page_count = 0
    row_count = 0
    file_index = 1
    current_csv_filename = f'ObjectsList_{series_naid}_{file_index}.csv'

    # Create initial CSV file
    with open(current_csv_filename, 'w', encoding='utf-8', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["Parent NAID", "Title", "Digital Object URL"])

    while True:
        url = f"{API_BASE_URL}?limit=25&searchAfter={search_after}&availableOnline=true&ancestorNaId={series_naid}"
        response = requests.get(url, headers=headers)
        data = response.json()

        if data.get('statusCode') != 200:
            print(f"Error retrieving data: {data.get('statusCode')}")
            break

        hits = data.get('body', {}).get('hits', {}).get('hits', [])
        if not hits:
            break  # No more records to process

        with open(current_csv_filename, 'a', encoding='utf-8', newline='') as csv_file:
            writer = csv.writer(csv_file)

            for hit in hits:
                record = hit.get('_source', {}).get('record', {})
                parent_naid = record.get('naId', 'Unknown')
                title = record.get('title', 'Untitled')
                digital_objects = record.get('digitalObjects', [])

                for obj in digital_objects:
                    url = obj.get('objectUrl', 'Unknown')
                    writer.writerow([parent_naid, title, url])
                    row_count += 1

                    # Create a new CSV file after 500,000 rows
                    if row_count >= 500000:
                        print(f"CSV {file_index} completed, starting next one...")
                        file_index += 1
                        current_csv_filename = f'ObjectsList_{series_naid}_{file_index}.csv'
                        row_count = 0
                        with open(current_csv_filename, 'w', encoding='utf-8', newline='') as new_csv_file:
                            new_writer = csv.writer(new_csv_file)
                            new_writer.writerow(["Parent NAID", "Title", "Digital Object URL"])

        last_hit = hits[-1]
        search_after = str(last_hit.get('sort', [None])[0])
        page_count += 1
        print(f"Processed page {page_count}, continuing...")

    print("Data retrieval complete.")

# User Input
series_naid = input("Enter Series NAID: ")

fetch_naids_and_digital_objects(series_naid)
