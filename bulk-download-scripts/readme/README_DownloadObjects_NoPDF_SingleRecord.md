
# Digital Object Downloader Script

## Table of Contents
Click below to go directly to the section you need.

- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Features](#features)
- [Usage](#usage)
- [Script Breakdown](#script-breakdown)
- [Notes](#notes)
- [Troubleshooting](#troubleshooting)

## Overview

This Python script downloads digital objects from the National Archives Catalog based on a given NAID (National Archives Identifier). It queries the Catalog API for records matching the provided NAID, parses the metadata, and downloads the associated digital objects (e.g., images, documents). All downloaded files are stored in a directory named after the provided NAID.

## Prerequisites

- **Python 3.x** installed on your machine.
- **requests** Python package installed (`pip install requests`).
- **PyPDF2** Python package installed (`pip install PyPDF2`).
- **Pillow** Python package installed (`pip install Pillow`).
- **img2pdf** Python package installed (`pip install img2pdf`).

## Features

- **API Integration**: Queries the National Archives Catalog API to fetch digital objects based on the provided NAID.
- **Directory Management**: Automatically creates a directory for the downloaded files named after the NAID.
- **CSV Logging**: Logs the URLs of the digital objects into a CSV file for record-keeping.
- **File Download**: Downloads each digital object to the created directory.
- **Error Handling**: Provides basic error handling for download failures.

## Usage

#### 1. Install Dependencies
Run the following command to install the required dependencies:
```bash
pip install requests PyPDF2 Pillow img2pdf
```

#### 2. Set API Key
The script will prompt you to enter your API Key, either from an environment variable or directly from the console.

#### 3. Run the Script
After setting your API Key and ensuring the dependencies are installed, run the script using the following command:
```bash
python downloader_script.py
```

You will be prompted to enter the NAID of the description that contains the objects to be downloaded. The script will then query the National Archives API, retrieve the metadata, and download the digital objects.

### Script Breakdown

#### Key Functions

- **`requests.get()`**: Makes a GET request to the National Archives Catalog API to retrieve metadata based on the provided NAID.
- **`csv.writer()`**: Writes the URLs of the digital objects into a CSV file for record-keeping.
- **`urllib.request.urlretrieve()`**: Downloads the digital object from the given URL.
- **`os.mkdir()`**: Creates a new directory for storing the downloaded files.

### Notes

- Ensure that your API Key is properly set, either as an environment variable or entered manually.
- The script will create a folder named after the provided NAID in the current directory to store the downloaded files.
- The script downloads all digital objects listed in the metadata returned by the API.

### Troubleshooting

- **Failed Downloads**: If a download fails, check the link and ensure it points to a valid digital object. Network issues or invalid URLs may cause failures.
- **API Key Issues**: If the API Key is invalid or expired, you will need to obtain a new one from the National Archives.
- **Permissions**: Ensure you have the necessary permissions to write files to the specified directory.

