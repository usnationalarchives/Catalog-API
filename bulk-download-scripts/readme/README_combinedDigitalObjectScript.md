# Combined Digital Object Script

## Contents
Click below to go directly to the section you need.
- **[Overview](#overview)**
- **[Features](#features)**
- **[Prerequisites](#prerequisites)**
- **[Usage](#usage)**
- **[Common Use Cases](#common-use-cases)**
- **[Advanced Features](#advanced-features)**
- **[Notes](#notes)**
- **[Troubleshooting](#troubleshooting)**

## Overview

The **Combined Digital Object Script** is an all-in-one tool that consolidates the functionality of all the individual download scripts into a single, user-friendly interface. Instead of choosing between multiple specialized scripts, you can use this one script to handle any download scenario with the National Archives Catalog API.

## Features

This script provides a **menu-driven interface** that guides you through your options, making it ideal for:
- Users who want a single tool for all their download needs
- Beginners who aren't sure which specialized script to use
- Advanced users who want flexibility without switching between scripts
- Anyone who values a streamlined, interactive workflow

### Core Capabilities
- **Multiple Discovery Methods**: Search by single NAID, parent NAID, custom search, or CSV file
- **Flexible Actions**: Choose to download files OR just generate a CSV manifest
- **Optional PDF Creation**: Combine downloaded images into PDFs when needed
- **Resume Support**: Interrupted downloads can resume without re-downloading files
- **Smart Organization**: All files organized in clearly-named directories
- **Comprehensive Error Handling**: Graceful handling with detailed error messages

### PDF Features (When Enabled)
- Automatic conversion of TIF/TIFF and JPG/JPEG images to PDF
- Image compression for JPG files (reduces file size)
- Multi-page TIFF support
- Natural sorting of files (1, 2, 3... not 1, 10, 11, 2...)
- Automatic cleanup of temporary files
- File handle management to prevent corruption

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
  - **Important**: Do not share your API key or publish it to public repositories (like GitHub). If a key is compromised, contact [Catalog_API@nara.gov](mailto:Catalog_API@nara.gov) to request a new one.
  - Keys are deactivated after 12 months of inactivity
  - See [API for the National Archives Catalog](https://www.archives.gov/research/catalog/help/api) for full Terms of Use.

### Storage and Hardware
- **Disk Space**: Bulk downloads consume significant storage space
- **Recommendation**: Use an external storage device (USB drive, external hard drive, or cloud storage) with at least 16 GB of free space
- **Example**: Approximately 100,000 JPG files require roughly 250 GB of disk space
- Plan ahead and ensure you have adequate storage before starting large downloads

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

#### Step-by-Step Walkthrough

##### Step 1: Choose Your Discovery Method

When you run the script, you'll see this menu:

```
=============================================
   NATIONAL ARCHIVES DIGITAL OBJECT TOOL
=============================================
What would you like to do?
  1. Download files from ONE specific record (Single NAID)
  2. Download ALL records inside a Series/Collection (Parent NAID)
  3. Run a custom search (Keywords or API query)
  4. Process an existing list of URLs from a local CSV

Select an option (1-4):
```

**Option 1: Single Record**
- Best for: Downloading one specific item
- Input: A single NAID (e.g., `123456789`)
- Example: You want to download all files from one specific document

**Option 2: Parent NAID (Series/Collection)**
- Best for: Downloading an entire series or collection
- Input: Parent NAID (e.g., Series NAID `987654321`)
- Example: You want all files from every record in a series
- Learn more: [National Archives Data Model](https://www.archives.gov/research/data-model)

**Option 3: Custom Search**
- Best for: Keyword or complex queries
- Input: Keywords or full API query string
- Examples:
  - Simple: `Tuskegee Airmen`
  - Advanced: `q=uap&startDate=1940-01-01&endDate=1950-12-31&typeOfMaterials=Photographs and other Graphic Materials`
- Tip: You'll also provide a project name for the output folder

**Option 4: CSV File**
- Best for: Processing a pre-generated list of URLs
- Input: Full path to your CSV file
- Note: CSV is read as: NAID, URL, optional Title (header row is skipped)
- Often used with `GenerateObjectURLs_NoDownload_AllChildRecords.py`

#### Step 2: Choose Your Action

After discovery, you'll be asked:

```
Found X records containing digital objects.
---------------------------------------------
What should I do with these?
  [D] Download the actual files to my computer
  [C] Just create a CSV spreadsheet listing the file links

Choose D or C:
```

**Option D: Download**
- Downloads all files to your computer
- Organizes into folders by NAID
- Proceeds to Step 3 (PDF settings)

**Option C: CSV Only**
- Creates one or more manifest files named `Manifest_[JobName]_part1.csv`, `Manifest_[JobName]_part2.csv`, etc.
- Files are split every 100,000 rows
- Lists all NAIDs and their file URLs
- No files are downloaded
- Great for planning or auditing before large downloads
- Script ends here (no Step 3)

#### Step 3: PDF Settings (Download Only)

If you chose to download, you'll see:

```
PDF SETTINGS:
Combine images into a single PDF for each record? (y/n):
```

**Answer "y" (yes) if:**
- You want a single combined PDF document per record
- Images will be processed and merged
- Perfect for reading/sharing complete documents

**Answer "n" (no) if:**
- You want to keep original file formats
- No PDF conversion or processing
- Files remain as downloaded (JPG, TIF, PDF, etc.)

### Understanding the Output

#### Folder Structure

After running the script, you'll have a folder structure like this:

```
JobName_or_NAID/
├── processed_naids.txt          # Resume tracking file
├── Manifest_JobName.csv         # (If CSV option chosen)
├── 123456789/                   # Folder for each NAID
│   ├── image001.jpg
│   ├── image002.jpg
│   ├── 123456789.pdf            # (If PDF creation enabled)
├── 987654321/
│   ├── document001.tif
│   ├── document002.tif
│   ├── 987654321.pdf
```

#### Files Explained

**`processed_naids.txt`**
- Tracks successfully completed NAIDs
- Enables resume functionality
- One NAID per line

**`Manifest_[JobName].csv`** (or `Manifest_[JobName]_part1.csv`, `part2.csv`, etc.)
- Created when you choose "CSV only" option
- For datasets with more than 100,000 URLs, automatically split into multiple files
- Each file contains up to 100,000 rows for easier management in spreadsheet applications
- Contains: NAID, URL, Title
- Can be used with CSV processing scripts later

**NAID Folders**
- One folder per record
- Named with the record's NAID
- Contains all downloaded objects for that record

**PDF Files** (when enabled)
- Named with the NAID (e.g., `123456789.pdf`)
- Contains all images merged into one document
- Natural page ordering preserved

## Common Use Cases

### Use Case 1: Download a Single Document with PDF

**Scenario:** You found a digitized document (NAID 12345678) and want it as a PDF.

- Choose: **1** (Single NAID)
- Enter NAID: `12345678`
- Choose: **D** (Download)
- PDF Option: **y** (yes)

**Result:** Folder `12345678/` containing images and `12345678.pdf`

---

### Use Case 2: Download an Entire Series

**Scenario:** You want all records in Series 654321 as original files (no PDF).

- Choose: **2** (Parent NAID)
- Enter Parent NAID: `654321`
- Choose: **D** (Download)
- PDF Option: **n** (no)

**Result:** Folder `Collection_654321/` with subfolders for each child record

---

### Use Case 3: Keyword Search + Generate Manifest Only

**Scenario:** Search for "Apollo 11" and create a list without downloading.

- Choose: **3** (Custom search)
- Project Name: `Apollo11_Photos`
- Search Terms: `apollo 11&typeOfMaterials=Photographs and other Graphic Materials`
- Choose: **C** (CSV only)

**Result:** Folder `Apollo11_Photos/` with `Manifest_Apollo11_Photos.csv`

---

### Use Case 4: Resume an Interrupted Download

**Scenario:** Your download was interrupted and you want to continue.

Simply re-run the same command with the same inputs. The script will:
- Check `processed_naids.txt`
- Skip already-completed records
- Continue with remaining downloads

---

## Advanced Features

### Automatic CSV Splitting

When generating CSV manifests (Option C), the script automatically splits large datasets into multiple files:

**Why split CSVs?**
- Spreadsheet applications (Excel, Google Sheets) have row limits and performance issues with huge files
- Smaller files are easier to open, search, and share
- Reduces memory usage when processing
- More manageable file sizes for version control and email

**How it works:**
- Files are split every 100,000 rows
- First file: `Manifest_[JobName]_part1.csv`
- Subsequent files: `Manifest_[JobName]_part2.csv`, `part3.csv`, etc.
- If total rows ≤ 100,000, one file is still created as `Manifest_[JobName]_part1.csv`
- Each file has proper CSV headers
- The script reports how many files were created

**Example:**
A search returning 250,000 URLs would create:
- `Manifest_MySearch_part1.csv` (100,000 rows)
- `Manifest_MySearch_part2.csv` (100,000 rows)
- `Manifest_MySearch_part3.csv` (50,000 rows)

### Custom API Queries

When choosing option 3 (custom search), you can use full API query syntax:

**Basic keyword:**
```
Tuskegee Airmen
```

**With filters:**
```
q=maps&startDate=1945&endDate=1945&typeOfMaterials=Maps and Charts
```

**Multiple parameters:**
```
q=apollo 11&typeOfMaterials=Photographs and other Graphic Materials
```
> [!TIP]
> Refer to the resources below to construct your query.  
> **Available Search Parameters:** [API Documentation](https://catalog.archives.gov/api/v2/api-docs/)  
> **Advanced Search Builder:** [National Archives Catalog](https://catalog.archives.gov/advanced-search)

### Natural Sorting in PDFs

The script uses natural sorting to ensure pages are in correct order:
- Correct: page1.jpg, page2.jpg, page10.jpg, page11.jpg
- Avoids: page1.jpg, page10.jpg, page11.jpg, page2.jpg

### Automatic Compression

When creating PDFs, JPG files are automatically compressed:
- Quality: 45% (balance between size and readability)
- Stored in temporary `Compressed/` folder during processing
- Automatically cleaned up after PDF creation

### Multi-page TIFF Support

TIFF files with multiple pages are handled correctly:
- All pages extracted and included in the PDF
- Each page converted to RGB for compatibility
- Maintains page order from the original file

## Notes

### Automatic Error Handling

The script handles common errors gracefully:
- **Network timeouts**: Logged and skipped
- **Invalid URLs**: Error message displayed
- **File corruption**: Skipped with warning
- **API errors**: Clear message about the issue

### Resume Functionality

If the script is interrupted:
1. Check the `processed_naids.txt` file
2. Re-run the script with the same parameters
3. Already-downloaded NAIDs are skipped
4. Downloads continue from where they stopped

**Note:** Failed records are logged but not added to `processed_naids.txt`, so they'll be retried on next run.

## Troubleshooting

- **API Key Issues**: If you receive authentication errors, verify that your API Key is correct and properly set as an environmental variable or entered when prompted.

- **No Records Found**: Ensure your API query is correct and that matching records are marked as `availableOnline`. Test your query in the Catalog API documentation first.

- **File Write Errors**: Verify that you have write permissions in the directory where the script is running. Ensure the query name does not contain special characters that are invalid for directory names.

- **Download Failures**: If specific files fail to download, check the error message printed to the console. This could indicate network issues, invalid URLs, or access restrictions. The script will continue with the next file.

- **Script Interruption**: If the script stops partway through, you can safely re-run it. It will skip already-downloaded files and resume from the next unprocessed page based on the pagination marker.

### Performance Tips

**Slow downloads or disk space issues:**
- Normal for large image files (TIF files can be 50+ MB each)
- Check your internet speed
- Use external storage with fast write speeds
- Consider downloading during off-peak hours
- Clean up `Compressed/` folder if script fails mid-process
- Monitor disk space during long downloads

**High memory usage during PDF creation:**
- Expected when processing many/large images
- Close other applications to free RAM
- Process smaller batches if needed
- Consider using the "no PDF" option for huge collections
