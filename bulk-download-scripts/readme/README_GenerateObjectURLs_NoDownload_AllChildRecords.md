# Generate Object URLs for All Child Records with No Download Script

## Contents
Click below to go directly to the section you need.

- **[Overview](#overview)**
- **[Prerequisites](#prerequisites)**
- **[Features](#features)**
- **[Usage](#usage)**
- **[Script Breakdown](#script-breakdown)**
- **[Output](#output)**
- **[Notes](#notes)**
- **[Troubleshooting](#troubleshooting)**

## Overview

This Python script queries the National Archives Catalog API to retrieve all digital object URLs associated with a specific series and exports them to CSV files. Unlike download scripts, this utility generates a comprehensive list of object URLs **without** downloading the actual files, making it useful for planning, auditing, or batch processing workflows.

## Prerequisites

- **National Archives Catalog API Key** which you may obtain by emailing Catalog_API@nara.gov.
- **Python 3.x** installed on your machine.
- **requests** Python package installed (`pip install requests`).

## Features

- **API Integration**: Queries the National Archives Catalog API to fetch digital objects from all records within a specified NAID (National Archives Identifier).
- **CSV Export**: Exports object metadata and URLs to CSV files for record-keeping and further processing.
- **Large Dataset Handling**: Automatically creates new CSV files after 500,000 rows to manage large datasets efficiently.
- **Pagination Support**: Uses the `searchAfter` parameter to handle API pagination and retrieve all available records.
- **Online Objects Only**: Filters results to include only objects marked as `availableOnline`.

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
python GenerateObjectURLs_NoDownload_AllChildRecords.py
```

### Input Prompts

- **Enter Series NAID:**  
  Enter the NAID for the series or file unit from which you want to retrieve all digital object URLs.

### Script Breakdown

#### Key Functions and Operations

1. **API Key Management**: Checks for the `CATALOG_API_KEY` environmental variable or prompts the user to enter the API Key manually.

2. **API Query**:
  - Queries the Catalog API with pagination support
  - Extracts parent NAID, title, and digital object URLs from each record
  - Writes data to CSV files with automatic file rotation after 500,000 rows
  - Uses `searchAfter` parameter for pagination to handle large result sets

3. **CSV Export**: Creates a new CSV file every 500,000 rows to manage large datasets efficiently
  - File naming convention: `ObjectsList_{series_naid}_{file_index}.csv`

## Output

#### CSV Files
CSV files are generated with the naming convention: `ObjectsList_{NAID}_{file_number}.csv`

Each CSV file contains the following columns:
- **Parent NAID**: The NAID of the record containing the digital object
- **Title**: The title of the record
- **Digital Object URL**: The URL to the digital object

#### Console Output Example:
```
Processed page 1, continuing...
Processed page 2, continuing...
CSV 1 completed, starting next one...
Processed page 3, continuing...
Data retrieval complete.
```

## Notes

- The script automatically filters results to include only records where `availableOnline=true`.
- Large series may generate multiple CSV files (numbered sequentially) if the result set exceeds 500,000 rows.
- The script queries for records within a specific series using the `ancestorNaId` parameter.

## Troubleshooting

- **API Key Issues**: If you receive authentication errors, verify that your API Key is correct and properly set as an environmental variable or entered when prompted.
  
- **No Records Found**: Ensure the NAID you entered is correct and contains records marked as `availableOnline`.

- **File Write Errors**: Verify that you have write permissions in the directory where the script is running.

- **Script Interruption**: If the script is interrupted during processing, you can safely re-run it. The script will resume from where it left off based on pagination markers.

