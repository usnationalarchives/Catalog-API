# Download Objects Create PDF Single Record Script

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

This Python script downloads all digital objects associated with a single National Archives record (identified by NAID) and automatically creates a consolidated PDF file from the downloaded images. The script handles image conversion, compression, and PDF merging, making it ideal for creating compact, usable documents from large collections of digitized materials.

## Prerequisites

- **National Archives Catalog API Key** which you may obtain by emailing Catalog_API@nara.gov.
- **Python 3.x** installed on your machine.
- **requests** Python package installed (`pip install requests`).
- **PyPDF2** Python package installed (`pip install PyPDF2`).
- **Pillow** Python package installed (`pip install Pillow`).
- **img2pdf** Python package installed (`pip install img2pdf`).

## Features

- **API Integration**: Queries the National Archives Catalog API to fetch all digital objects for a specified NAID.
- **Automatic Downloads**: Downloads all digital objects associated with the record to a directory.
- **Image Format Handling**: Automatically generates JPG renditions from TIF and JP2 files if JPGs are not already present.
- **Image Compression**: Compresses downloaded JPG images to optimized file sizes while maintaining quality.
- **PDF Conversion**: Converts compressed images to individual PDF files.
- **PDF Merging**: Merges all individual PDFs into a single consolidated PDF file.
- **File Size Management**: Automatically splits PDFs if they exceed 500MB to manage file sizes.
- **CSV Logging**: Creates a CSV file tracking all downloaded object URLs.
- **Error Handling**: Provides error handling for download failures and image processing issues.

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
python DownloadObjects_CreatePDF_SingleRecord.py
```

### Input Prompts

- **Do you have your API Key set as an environmental variable (Y/N)?**  
  Enter `Y` if the API Key is set as an environmental variable, or `N` to manually input the API Key.

- **File Unit or Item NAID:**  
  Enter the NAID for the record whose digital objects you want to download and convert to PDF.

### Script Breakdown

#### Key Operations

1. **API Key Management**: Checks for the `CATALOG_API_KEY` environmental variable or prompts the user to enter the API Key manually.

2. **Directory Creation**: Creates a directory named after the provided NAID to store all downloaded files and the final PDF.

3. **API Query**: Queries the Catalog API using the `naId_is` parameter to retrieve exact matches for the specified NAID.

4. **CSV Export and Download**:
   - Extracts digital object URLs from the API response
   - Saves URLs to `ListOfObjectsToDownload_{NAID}.csv`
   - Downloads each digital object to the NAID directory
   - Skips files that have already been downloaded

5. **Image Format Conversion**:
   - Scans downloaded files for TIF and JP2 formats
   - If a JPG rendition doesn't exist, generates one from the TIF or JP2 file
   - Uses PIL (Pillow) for image processing

6. **Image Compression**:
   - Compresses JPG files to reduce file sizes (quality set to 45)
   - Stores compressed images in a `Compressed/` subdirectory
   - Logs average compression ratio achieved

7. **PDF Creation**:
   - Converts each compressed JPG to an individual PDF using img2pdf
   - Maintains file order based on sorted filenames

8. **PDF Merging**:
   - Merges all individual PDFs into consolidated PDF file(s)
   - Automatically splits into multiple PDFs if file size would exceed 500MB
   - Output files named `{NAID}_split_{number}.pdf` if split is necessary

## Output

#### Directory Structure
```
{NAID}/
├── {downloaded_image_files}     (original downloads: JPG, TIF, JP2, etc.)
├── Compressed/
│   ├── Compressed_{image_1}.jpg
│   ├── Compressed_{image_2}.jpg
│   ├── Compressed_{image_1}.pdf
│   ├── Compressed_{image_2}.pdf
│   └── ...
├── {NAID}_split_1.pdf           (merged PDF output)
├── {NAID}_split_2.pdf           (if size exceeds 500MB)
└── ListOfObjectsToDownload_{NAID}.csv
```

#### Console Output Example:
```
Do you have your API Key set as an environmental variable (Y/N)?
Y
12:30:45.123456
Downloading: 123456789/image1.jpg
Downloading: 123456789/image2.tif
All files downloaded! 12:35:20.654321
Checking for JPGs:
image2.tif
Generating jpeg for image2.tif
Compressing JPGs:
File compressed from 8500000 to 1200000 or 85%
File compressed from 7200000 to 920000 or 87%
Average Compression: 86
All done compressing! 12:40:15.987654
Creating PDFs and combining into one:
Successfully created individual pdf files! 12:42:30.123456
Merging PDFs...
Successfully merged pdf files! 12:45:00.654321
```

#### Output Files
- **PDF Files**: `{NAID}_split_1.pdf` (and additional splits if needed), located in the `{NAID}/` directory
- **CSV File**: `ListOfObjectsToDownload_{NAID}.csv` tracking all downloaded URLs
- **Compressed Images**: Stored in `{NAID}/Compressed/` for reference

## Notes

- **Image Quality**: Compression quality is set to 45 in the script. Adjust the quality parameter in the `compressMe()` function if different compression levels are desired.
  
- **File Size Limit**: PDFs are automatically split if they exceed 500MB (500 * 1024 * 1024 bytes). Modify the `max_file_size` variable to change this threshold.

- **Image Format Conversion**: The script automatically converts TIF and JP2 files to JPG format before PDF creation. If a JPG already exists, it will not be regenerated.

- **File Naming**: Filenames in the `Compressed/` directory are prefixed with `Compressed_` to distinguish them from originals.

- **Processing Time**: Large records with many high-resolution images may take considerable time to process, as each image is compressed and converted to PDF individually.

- **API Specificity**: The script uses `naId_is=` for exact matching, ensuring it retrieves only the single record specified by the NAID.

## Troubleshooting

- **API Key Issues**: If you receive authentication errors, verify that your API Key is correct and properly set as an environmental variable or entered when prompted.

- **No Objects Found**: If no digital objects are found, ensure the NAID you entered is correct and that the record contains digital objects marked as available online.

- **Image Processing Failures**: If the script fails during image conversion or compression, check that:
  - Pillow and img2pdf are correctly installed
  - The image files are in supported formats (JPG, TIF, JP2)
  - System has sufficient disk space for temporary processing files

- **PDF Creation Issues**: If PDFs fail to merge properly, verify that:
  - All individual PDFs were created successfully (check the Compressed directory)
  - PyPDF2 is correctly installed
  - No individual PDF files are corrupted

- **File Write Errors**: Verify that you have write permissions in the directory where the script is running.

- **Insufficient Disk Space**: High-resolution image collections require significant disk space. Ensure your system has enough free space for downloaded files, compressed versions, and temporary PDF files.

- **Script Interruption**: If the script is interrupted during processing, you can safely re-run it. The script will:
  - Skip already-downloaded files
  - Skip already-compressed images
  - Regenerate the final PDF from existing compressed images

