
# Download Objects from All Child Records with No PDF Script

## Contents
Click below to go directly to the section you need.

- **[Overview](#overview)**
- **[Prerequisites](#prerequisites)**
- **[Features](#features)**
- **[Usage](#usage)**
- **[Output](#output)**
- **[Troubleshooting](#troubleshooting)**

## Overview

This Python script interacts with the National Archives Catalog API to search for and download digital objects attached to file units and/or items within a specific series. It queries the API for records, extracts object URLs, saves them to a CSV file, and downloads the digital objects into separate folders named after the file unit or item NAIDs.

## Prerequisites

- **National Archives Catalog API Key** which you may obtain by emailing Catalog_API@nara.gov.
- **Python 3.x** installed on your machine.
- **requests** Python package installed (`pip install requests`).
- **Pillow** Python package installed (`pip install Pillow`).

## Features:
- Queries the Catalog API for digital objects linked to file units and/or items within a specific series.
- Downloads digital objects into directories based on the file unit or item NAID.
- Uses the `nextCursorMark` to handle more than 10,000 results (the maximum limit per API query).
- Automatically creates directories for each parent NAID if they do not already exist.
- Cleans up the CSV file after downloading the objects.

## Usage

### 1. Set API Key
Before running the script, ensure you have your API Key. The script will first check if the API Key is set as an environmental variable. If it's not, it will prompt you to enter the key manually.

To set the API Key as an environmental variable, run the following command in your terminal:

```bash
# Windows (PowerShell)
$env:CATALOG_API_KEY="your_api_key_here"

# Linux/Mac (Bash)
export CATALOG_API_KEY="your_api_key_here"
```

Alternatively, you can manually enter the API Key when prompted by the script.

### 2. Install Dependencies
You can install the required libraries using `pip`:

```bash
pip install requests pillow
```

### 3. Run the Script
After setting your API Key and ensuring the dependencies are installed, run the script using the following command:
```bash
python DownloadObjects_NoPDF_AllChildRecords.py
```

### Input Prompts

- **Do you have your API Key set as an environmental variable (Y/N)?**  
  Enter `Y` if the API Key is set as an environmental variable, or `N` to manually input the API Key.

- **Parent NAID:**  
  Enter the parent NAID for the series you want to query.

## Output
- **CSV File:**  
  A CSV file named `ListOfObjectsToDownload_{NAID}.csv` will be generated, containing the parent NAID and object URL pairs.
  
- **Downloaded Files:**  
  Files will be downloaded into directories named after the parent NAID. For example, the directory structure will look like:
  
  ```bash
  /{parent_naid}/{file_name}
  ```

#### Console Output Example:
```
Downloading: /123456789/abcd1234/image1.jpg
Downloading: /123456789/abcd1234/image2.jpg
All Files downloaded! 12:30:00
```

## Troubleshooting

- **API Key Issues**: If you receive authentication errors, verify that your API Key is correct and properly set as an environmental variable or entered when prompted.

- **No Objects Found**: If no digital objects are found, ensure the NAID you entered is correct and that the record contains digital objects marked as available online.

- **File Write Errors**: Verify that you have write permissions in the directory where the script is running.

- **Insufficient Disk Space**: High-resolution image collections require significant disk space. Ensure your system has enough free space for downloaded files, compressed versions, and temporary PDF files.
