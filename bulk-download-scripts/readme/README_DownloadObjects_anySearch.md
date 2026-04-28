# Download Objects Any Search Script

## Table of Contents
Click below to go directly to the section you need.

- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Features](#features)
- [Usage](#usage)
- [Script Breakdown](#script-breakdown)
- [Output](#output)
- [Notes](#notes)
- [Troubleshooting](#troubleshooting)

## Overview

This Python script provides flexible querying and downloading of digital objects from the National Archives Catalog based on custom API search parameters. Unlike other scripts that target specific NAIDs or series, this script allows you to construct any query using the full power of the Catalog API, then automatically downloads all matching digital objects. All downloaded files are organized into directories named after their parent NAIDs.

## Prerequisites

- **National Archives Catalog API Key** which you may obtain by emailing Catalog_API@nara.gov.
- **Python 3.x** installed on your machine.
- **requests** Python package installed (`pip install requests`).

## Features

- **Flexible API Querying**: Accepts any valid Catalog API query parameters for custom searches.
- **Automatic Download**: Retrieves and downloads all digital objects matching your search criteria.
- **Directory Organization**: Automatically creates directories organized by parent NAID for downloaded files.
- **CSV Logging**: Creates a temporary CSV file tracking all discovered object URLs.
- **Pagination Support**: Handles pagination automatically to retrieve all results across multiple API pages.
- **Online Objects Only**: Filters results to include only records marked as `availableOnline`.
- **Error Handling**: Provides basic error handling for download failures.

## Usage

#### 1. Install Dependencies
Run the following command in your terminal to install the required dependencies:
```bash
pip install requests
```

#### 2. Set API Key
Before running the script, ensure you have your API Key. The script will first check if the API Key is set as an environmental variable. If it's not, it will prompt you to enter the key manually.

To set the API Key as an environmental variable, run the following command in your terminal:

```bash
# Windows (PowerShell)
$env:CATALOG_API_KEY="your_api_key_here"

# Linux/Mac (Bash)
export CATALOG_API_KEY="your_api_key_here"
```

#### 3. Run the Script
After setting your API Key and ensuring the dependencies are installed, run the script using the following command:
```bash
python DownloadObjects_anySearch.py
```

### Input Prompts

- **Do you have your API Key set as an environmental variable (Y/N)?**  
  Enter `Y` if the API Key is set as an environmental variable, or `N` to manually input the API Key.

- **Enter a one-word name for your query:**  
  Provide a single-word identifier for your search query. This will be used as the directory name and CSV file name for your downloaded objects. Examples: "photographs", "correspondence", "maps".

- **Enter your API query (everything that follows https://catalog.archives.gov/api/v2/records/search?):**  
  Enter the complete query parameters you want to use for searching. Examples:
  - `q=Declaration of Independence`
  - `q=photography&parentNaId=123456789`
  - `q=Lincoln&recordType=record_group`

### Script Breakdown

#### Key Functions and Operations

- **API Key Management**: Checks for the `CATALOG_API_KEY` environmental variable or prompts the user to enter the API Key manually.

- **Directory Creation**: Automatically creates a main directory using the query topic name provided by the user.

- **Pagination Loop**: 
  - Iterates through all API results using the `searchAfter` parameter
  - Processes up to 100 records per API call
  - Continues until all matching records are retrieved

- **CSV Processing**:
  - Extracts parent NAID and digital object URLs from API responses
  - Writes entries to a temporary CSV file (`ListOfObjectsToDownload_{topic}.csv`)
  - Uses the CSV to organize downloads by parent NAID
  - Clears the CSV after each page of results to avoid duplicate downloads

- **File Download**:
  - Creates subdirectories for each unique parent NAID
  - Downloads each digital object to its corresponding NAID directory
  - Skips files that have already been downloaded
  - Includes error handling for failed downloads

## Output

#### Directory Structure
Downloaded files are organized as follows:
```
{topic_name}/
├── {parent_naid_1}/
│   ├── object1.jpg
│   ├── object2.jpg
│   └── ...
├── {parent_naid_2}/
│   ├── document1.pdf
│   └── ...
└── ...
```

#### CSV File
A temporary CSV file named `ListOfObjectsToDownload_{topic}.csv` is created during execution and cleared after each page of results. The file contains:
- **Parent NAID**: The NAID of the record containing the digital object
- **Object URL**: The URL to the digital object

#### Console Output Example:
```
Do you have your API Key set as an environmental variable (Y/N)?
Y
Last NAID on page 0: 123456789
Last NAID on page 1: 234567890
Last NAID on page 2: 345678901
Downloading: photographs/123456789/image1.jpg
Downloading: photographs/123456789/image2.jpg
Downloading: photographs/234567890/document.pdf
All objects downloaded! 14:35:42.123456
```

## Notes

- The script automatically filters results to include only records where `availableOnline=true`.
- The query name you enter should be a **single word** (no spaces) as it's used for directory and file naming.
- API queries can be complex and include multiple parameters. Refer to the [National Archives Catalog API documentation](https://github.com/usnationalarchives/catalog-api) for valid search parameters.
- The temporary CSV file is cleared after processing each page to prevent duplicate downloads.
- API rate limiting may apply depending on your API key tier. The script processes 100 records per API call.
- Network interruptions may cause the script to stop. Re-running the script will skip already-downloaded files and continue from where it left off.

## Troubleshooting

- **API Key Issues**: If you receive authentication errors, verify that your API Key is correct and properly set as an environmental variable or entered when prompted.

- **No Records Found**: Ensure your API query is correct and that matching records are marked as `availableOnline`. Test your query in the Catalog API documentation first.

- **File Write Errors**: Verify that you have write permissions in the directory where the script is running. Ensure the query name does not contain special characters that are invalid for directory names.

- **Download Failures**: If specific files fail to download, check the error message printed to the console. This could indicate network issues, invalid URLs, or access restrictions. The script will continue with the next file.

- **Script Interruption**: If the script stops partway through, you can safely re-run it. It will skip already-downloaded files and resume from the next unprocessed page based on the pagination marker.

