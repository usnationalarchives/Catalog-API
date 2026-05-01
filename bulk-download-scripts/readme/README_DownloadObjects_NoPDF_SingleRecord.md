
# Download Objects from Single Record with No PDF Script

## Contents
Click below to go directly to the section you need.

- **[Overview](#overview)**
- **[Prerequisites](#prerequisites)**
- **[Features](#features)**
- **[Usage](#usage)**
- **[Script Breakdown](#script-breakdown)**
- **[Troubleshooting](#troubleshooting)**

## Overview

This Python script downloads digital objects from the National Archives Catalog based on a given NAID (National Archives Identifier). It queries the Catalog API for records matching the provided NAID, parses the metadata, and downloads the associated digital objects (e.g., images, documents). All downloaded files are stored in a directory named after the provided NAID.

## Prerequisites

- **National Archives Catalog API Key** which you may obtain by emailing Catalog_API@nara.gov.
- **Python 3.x** installed on your machine.
- **requests** Python package installed (`pip install requests`).
- **PyPDF2** Python package installed (`pip install PyPDF2`).
- **Pillow** Python package installed (`pip install Pillow`).
- **img2pdf** Python package installed (`pip install img2pdf`).

## Features

- **API Integration**: Queries the National Archives Catalog API to fetch all digital objects for a specified NAID.
- **Directory Management**: Automatically creates a directory for the downloaded files named after the NAID.
- **CSV Logging**: Creates a CSV file tracking all downloaded object URLs.
- **File Download**: Downloads each digital object to the created directory.
- **Error Handling**: Provides basic error handling for download failures.

## Usage

#### 1. Install Required Packages
Run the following command in your terminal to install the required packages:
```bash
pip install requests PyPDF2 Pillow img2pdf
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
python DownloadObjects_NoPDF_SingleRecord.py
```

### Input Prompts

- **Do you have your API Key set as an environmental variable (Y/N)?**  
  Enter `Y` if the API Key is set as an environmental variable, or `N` to manually input the API Key.

- **File Unit or Item NAID:**  
    Enter the NAID for the record whose digital objects you want to download.

### Script Breakdown

#### Key Operations

- **`requests.get()`**: Makes a GET request to the National Archives Catalog API to retrieve metadata based on the provided NAID.
- **`csv.writer()`**: Writes the URLs of the digital objects into a CSV file for record-keeping.
- **`urllib.request.urlretrieve()`**: Downloads the digital object from the given URL.
- **`os.mkdir()`**: Creates a new directory for storing the downloaded files.



### Troubleshooting

- **API Key Issues**: If you receive authentication errors, verify that your API Key is correct and properly set as an environmental variable or entered when prompted.

- **No Objects Found**: If no digital objects are found, ensure the NAID you entered is correct and that the record contains digital objects marked as available online.

- **File Write Errors**: Verify that you have write permissions in the directory where the script is running.

- **Insufficient Disk Space**: High-resolution image collections require significant disk space. Ensure your system has enough free space for downloaded files, compressed versions, and temporary PDF files.

