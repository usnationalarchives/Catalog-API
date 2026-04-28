# National Archives Catalog API Bulk Download Python Scripts

## Table of Contents
Click below to go directly to the section you need.

- [Overview](#overview)
- [Available Scripts](#available-scripts)
- [Prerequisites](#prerequisites)
- [Features](#features)
- [Installation and Setup](#installation-and-setup)
- [Choosing the Right Script](#choosing-the-right-script)
- [Script Descriptions](#script-descriptions)
  - [Combined Digital Object Script (All-in-One Tool)](#-combined-digital-object-script-all-in-one-tool)
  - [Download Objects Create PDF Single Record](#-download-objects-create-pdf-single-record)
  - [Download Objects No PDF Single Record](#-download-objects-no-pdf-single-record)
  - [Download Objects No PDF All Child Records](#-download-objects-no-pdf-all-child-records)
  - [Generate Object URLs No Download All Child Records](#-generate-object-urls-no-download-all-child-records)
  - [Download Objects Any Search](#-download-objects-any-search)
- [Troubleshooting](#troubleshooting)
- [Getting Help](#getting-help)
- [License and Attribution](#license-and-attribution)

## Overview

These Python scripts are designed to help you download archival records and digital objects in bulk using the [National Archives Catalog](https://catalog.archives.gov/) API.

## Prerequisites

### Software Requirements
- **Python 3.6 or higher** - Download from [python.org](https://www.python.org/downloads/)
  - **Windows users**: When installing Python, make sure to check the box that says "Add Python to PATH"
  - **Mac users**: Python 3 is available via Homebrew or directly from python.org
  - **Linux users**: Python should already be installed; check by running `python3 --version`

### API Key
- **National Archives Catalog API Key** - Obtain one by emailing [Catalog_API@nara.gov](mailto:Catalog_API@nara.gov)
  - Store this key securely as it authenticates your requests to the API
  - **Default limit**: 10,000 API queries per month
  - **Important**: Do not share your API key or publish it to public repositories (like GitHub). If a key is compromised, contact Catalog_API@nara.gov to request a new one.
  - Keys are deactivated after 12 months of inactivity

### Storage and Hardware
- **Disk Space**: Bulk downloads consume significant storage space
- **Recommendation**: Use an external storage device (USB drive, external hard drive, or cloud storage) with at least 16 GB of free space
- **Example**: Approximately 100,000 JPG files require roughly 250 GB of disk space
- Plan ahead and ensure you have adequate storage before starting large downloads

### Python Packages
The scripts use external Python packages that you'll install during setup.

## Features

- **API Integration**: Queries the National Archives Catalog API using your search criteria
- **Automatic Organization**: Downloads files into clearly-named directories for easy management
- **CSV Record-Keeping**: Every download session is logged in a CSV file for your records
- **Flexible Searching**: Find records by NAID, keyword, or custom API parameters
- **PDF Creation** (optional): Some scripts can combine downloaded images into a single PDF document
- **Image Processing**: Automatic format conversion and compression when creating PDFs
- **Error Handling**: Graceful handling of download failures with informative error messages
- **Resume Capability**: If interrupted, scripts can resume where they left off without re-downloading files

## Installation and Setup

### Step 1: Download and Install Python
1. Visit [python.org](https://www.python.org/downloads/) and download Python 3.8 or higher
2. **Windows users**: During installation, IMPORTANT - check the box for "Add Python to PATH"
3. Run the installer and follow the prompts
4. Verify installation by opening a terminal/command prompt and typing:
   ```bash
   python --version
   ```

### Step 2: Install Required Packages
Open your terminal/command prompt and run this single command to install all required packages:
```bash
pip install requests PyPDF2 Pillow img2pdf
```
This will download and install all the libraries these scripts need.

### Step 3: Get Your API Key
1. Email [Catalog_API@nara.gov](mailto:Catalog_API@nara.gov) requesting an API key
2. Save your API key somewhere secure

### Step 4: Set Your API Key (Optional but Recommended)
You can set your API key as an environment variable so you don't have to type it in each time:

**Windows (PowerShell):**
```powershell
$env:CATALOG_API_KEY="your_api_key_here"
```

**Mac/Linux (Terminal):**
```bash
export CATALOG_API_KEY="your_api_key_here"
```

You may also enter your key when the script prompts you.

### Step 5: Download the Scripts
Clone this repository or download the Python script files to your computer.

## Choosing the Right Script

Not sure which script you need? Here's a quick guide:

| **Your Goal** | **Use This Script** | **More Info** |
|---|---|---|
| **One tool for everything** — Interactive menu for any scenario | `combinedDigitalObjectScript.py` ⭐ | [Full Documentation](readme/README_combinedDigitalObjectScript.md) |
| Download one record + create a PDF from the images | `DownloadObjects_CreatePDF_SingleRecord.py` | [Full Documentation](readme/README_DownloadObjects_CreatePDF_SingleRecord.md) |
| Download one record without creating a PDF | `DownloadObjects_NoPDF_SingleRecord.py` | [Full Documentation](readme/README_DownloadObjects_NoPDF_SingleRecord.md) |
| Download all child records in a series (e.g., all files in a series) | `DownloadObjects_NoPDF_AllChildRecords.py` | [Full Documentation](readme/README_DownloadObjects_NoPDF_AllChildRecords.md) |
| Just get a list of object URLs without downloading | `GenerateObjectURLs_NoDownload_AllChildRecords.py` | [Full Documentation](readme/README_GenerateObjectURLs_NoDownload_AllChildRecords.md) |
| Download results from a keyword search | `DownloadObjects_anySearch.py` | [Full Documentation](readme/README_DownloadObjects_anySearch.md) |
| Download objects listed in CSV files | `DownloadObjects_FromCSV.py` | [Full Documentation](scripts/README_DownloadObjects_FromCSV.md) |

## Script Descriptions

### ⭐ **<ins>Combined Digital Object Script (All-in-One Tool)</ins>**

**The all-in-one solution** with an interactive menu that handles every download scenario in a single script.

**Best for:** Anyone who wants one tool for all their needs, beginners, or users who prefer guided workflows

**Key Features:**
- **Interactive menu-driven interface** — choose your workflow as you go
- **Four discovery methods**: Single NAID, Parent NAID (series), custom search, or CSV file
- **Flexible actions**: Download files OR generate CSV manifests
- **Optional PDF creation**: Combine images into PDFs when needed
- **Resume support**: Interrupted downloads can continue where they left off
- **Smart organization**: Files organized by NAID in clearly-named directories
- **All specialized features included**: Natural sorting, image compression, multi-page TIFF support
- Complete documentation: [README_combinedDigitalObjectScript.md](readme/README_combinedDigitalObjectScript.md)

**To run:** `python scripts/combinedDigitalObjectScript.py`

**Why use this instead of individual scripts?**
- One tool does everything — no need to remember which script to use
- Interactive prompts guide you through options
- Perfect for varied research needs or experimentation
- Consolidates all the best features from specialized scripts

**When to use individual scripts instead:**
- You have a specific, repeated workflow
- You prefer minimal prompts for automation
- You're writing shell scripts that need predictable behavior

---

### 🚀 **<ins>Download Objects Create PDF Single Record</ins>**

Downloads all digital objects from a **single record** and automatically creates a consolidated PDF from the images.

**Best for:** Researchers who want one complete document from a record's materials

**Key Features:**
- Downloads digital objects for a specific NAID
- Automatically converts TIF/JP2 images to JPG
- Compresses images to reduce file size
- Creates a single merged PDF file (or multiple if >500MB)
- Complete documentation: [README_DownloadObjects_CreatePDF_SingleRecord.md](readme/README_DownloadObjects_CreatePDF_SingleRecord.md)

**To run:** `python DownloadObjects_CreatePDF_SingleRecord.py`

---

### 🚀 **<ins>Download Objects No PDF Single Record</ins>**

Downloads all digital objects from a **single record** without creating a PDF.

**Best for:** Researchers who want the original image files without PDF conversion

**Key Features:**
- Downloads digital objects for a specific NAID
- Keeps files in their original formats (JPG, TIF, PDF, etc.)
- Organizes files into a folder named after the NAID
- Complete documentation: [README_DownloadObjects_NoPDF_SingleRecord.md](readme/README_DownloadObjects_NoPDF_SingleRecord.md)

**To run:** `python DownloadObjects_NoPDF_SingleRecord.py`

---

### 🚀 **<ins>Download Objects No PDF All Child Records</ins>**

Downloads digital objects for **all child records within a parent record** (e.g., all file units within a series).

**Best for:** Downloading entire collections where you have a series or collection NAID

**Key Features:**
- Downloads objects for all records within a specified parent
- Each child record's objects stored in separate folders
- Handles API pagination automatically
- Great for large collections with hundreds or thousands of items
- Learn more about record relationships: [National Archives Catalog Data Model](https://www.archives.gov/research/data-model)
- Complete documentation: [README_DownloadObjects_NoPDF_AllChildRecords.md](readme/README_DownloadObjects_NoPDF_AllChildRecords.md)

**To run:** `python DownloadObjects_NoPDF_AllChildRecords.py`

---

### 🚀 **<ins>Generate Object URLs No Download All Child Records</ins>**

**Generates a list of object URLs** (in CSV format) for all child records within a parent, **without downloading the actual files**.

**Best for:** Planning downloads, auditing collections, or preparing for batch processing

**Key Features:**
- Queries all records within a series
- Exports object metadata and URLs to CSV files
- Handles large result sets (auto-creates new CSV after 500,000 rows)
- Fast—no time spent downloading files
- Useful for reviewing what's available before committing to a large download
- Complete documentation: [README_GenerateObjectURLs_NoDownload_AllChildRecords.md](readme/README_GenerateObjectURLs_NoDownload_AllChildRecords.md)

**Note (paired workflow):** This script is often used together with a CSV downloader. First run `GenerateObjectURLs_NoDownload_AllChildRecords.py` to produce `ObjectsList_*.csv` files (a preview of available object URLs), then use `DownloadObjects_FromCSV.py` to download those URLs. See the downloader documentation for usage and best practices: [scripts/README_DownloadObjects_FromCSV.md](scripts/README_DownloadObjects_FromCSV.md)

**To run (generate CSV):** `python GenerateObjectURLs_NoDownload_AllChildRecords.py`

**To run (download from CSV):** `python scripts/DownloadObjects_FromCSV_RateLimited.py --csv ObjectsList_123456789_1.csv`

---

### 🚀 **<ins>Download Objects Any Search</ins>**

Downloads digital objects using **custom keyword or API search parameters**.

**Best for:** Researchers searching for specific topics (e.g., "Tuskegee", "Cuban Missile Crisis", "UAP")

**Key Features:**
- Build custom searches using Catalog API parameters
- Downloads all matching results
- Each record's objects stored in separate folders
- Flexible querying for complex research needs
- Complete documentation: [README_DownloadObjects_anySearch.md](readme/README_DownloadObjects_anySearch.md)

**To run:** `python DownloadObjects_anySearch.py`

---

## Important API Usage Notes

**Attribution Required**: If you use these scripts or the National Archives Catalog API for any public service or application, you must display the following notice:
> "This product uses the National Archives Catalog API but is not endorsed or certified by the National Archives and Records Administration."

**Data Access Limits**: 
- These scripts query the API and are subject to the monthly query limit (10,000 by default)
- **Do not** attempt to download all data from the Catalog via the API
- For complete dataset access, use the [National Archives Catalog dataset on the Amazon Web Services Registry of Open Data](https://registry.opendata.aws/national-archives-catalog/)

**API Key Security**:
- Never share your API key in emails or other communications
- Never publish your API key to public repositories like GitHub
- Keep your key confidential and treat it like a password
- If your key is compromised, contact [Catalog_API@nara.gov](mailto:Catalog_API@nara.gov) immediately
- Unused keys (not used for 12 months) will be automatically deactivated

**Best Practices**:
- Plan your downloads in advance to stay within monthly query limits
- Use the `GenerateObjectURLs_NoDownload_AllChildRecords.py` script to preview what's available before downloading
- Consider using external storage to preserve your downloaded materials

## Troubleshooting

### General Issues

**"Python is not recognized as a command"**
- **Windows**: Python wasn't added to PATH during installation. Reinstall Python and make sure to check "Add Python to PATH"
- **Mac/Linux**: Try using `python3` instead of `python`

**"No module named 'requests'" (or similar)**
- You haven't installed the required packages yet. Run: `pip install requests PyPDF2 Pillow img2pdf`

**"Error: API Key is invalid"**
- Double-check that your API key is correct. Make sure there are no extra spaces or special characters
- If you recently requested a key, it may take 1-2 business days to arrive

### API and Network Issues

**"Error 400: Bad Request" or "statusCode not 200"**
- Check that your NAID or search query is correct
- Make sure you have an internet connection
- The API service might be temporarily unavailable; try again in a few minutes

**"Connection timeout"**
- Check your internet connection
- Try running the script again—network issues can be temporary
- If the problem persists, contact National Archives support

### File and Download Issues

**"Permission denied" when saving files**
- The script doesn't have permission to write to this directory
- Try running the script from a different location (like your Documents or Desktop folder)
- On Windows, try opening Command Prompt as Administrator

**"Downloads are very slow"**
- This is normal if downloading large image files
- Check your internet connection speed
- Large downloads may take several hours depending on file count and size

**"Some files failed to download"**
- This can happen if a download link is broken or temporarily unavailable
- The script will display error messages for failed files
- You can try re-running the script to retry failed downloads

### Script Interruptions

**"Script stopped in the middle"**
- This is okay! You can safely re-run the script
- It will skip files that were already downloaded and continue where it left off
- Check your internet connection before restarting

### PDF Creation Issues (CreatePDF script only)

**"PDF creation failed"**
- Make sure Pillow and img2pdf are installed: `pip install Pillow img2pdf`
- Check that downloaded image files aren't corrupted
- Ensure you have enough disk space for compressed images and PDF files

**"PDF file is very large"**
- The script automatically splits PDFs larger than 500MB
- For very large collections, you may get multiple PDF files (named with `_split_1`, `_split_2`, etc.)
- This is normal and intentional

## Getting Help

### Can't Find What You Need?
1. **Check the specific script's README** - Each script has its own detailed documentation with examples
2. **Review this main README** - Most answers are here!
3. **Check the Troubleshooting section above** - Common issues and solutions
4. **Review Important API Usage Notes** - Information about limits, storage, and best practices

### Still Having Problems?
Contact the National Archives Catalog API team for technical support:
- **Email**: [Catalog_API@nara.gov](mailto:Catalog_API@nara.gov)
- Include in your email:
  - Which script you're using
  - What error message you received (if any)
  - The NAID or search term you were using (if not sensitive)
  - Your operating system (Windows, Mac, Linux)
  - Steps you've already tried

### Technical Resources and Documentation

**Official Documentation:**
- [National Archives Catalog API Documentation](https://www.archives.gov/data/api)
- [National Archives Catalog Data Model](https://www.archives.gov/research/data-model) - Understand record relationships and hierarchy
- [GitHub Repository](https://github.com/usnationalarchives/catalog-api) - Source code and additional resources
- [API Swagger Documentation](https://catalog.archives.gov/api/v2/docs/) - Interactive API documentation and testing

**Data Access:**
- [AWS Registry of Open Data - National Archives Catalog](https://registry.opendata.aws/national-archives-catalog/) - For bulk dataset access

**Reporting Issues:**
If you discover a bug or have a feature request, you can also report it on the [GitHub Issues page](https://github.com/usnationalarchives/catalog-api/issues)

## License and Attribution

These scripts are provided by the **National Archives Catalog API Team**. Feel free to modify and use them according to your needs.

**Created by:** National Archives Catalog API Team  
**For questions or feedback**, please contact: [Catalog_API@nara.gov](mailto:Catalog_API@nara.gov)

