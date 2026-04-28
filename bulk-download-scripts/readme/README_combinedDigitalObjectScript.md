# Combined Digital Object Script - Complete Documentation

## Overview

The **Combined Digital Object Script** is an all-in-one tool that consolidates the functionality of all the individual download scripts into a single, user-friendly interface. Instead of choosing between multiple specialized scripts, you can use this one script to handle any download scenario with the National Archives Catalog API.

## What Makes This Script Special?

This script provides a **menu-driven interface** that guides you through your options, making it ideal for:
- Users who want a single tool for all their download needs
- Beginners who aren't sure which specialized script to use
- Advanced users who want flexibility without switching between scripts
- Anyone who values a streamlined, interactive workflow

## Features

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

### Required Software
- **Python 3.6 or higher** ([Download here](https://www.python.org/downloads/))
- Required Python packages:
  ```bash
  pip install requests PyPDF2 Pillow img2pdf
  ```

### Required Credentials
- **National Archives Catalog API Key** - Request from [Catalog_API@nara.gov](mailto:Catalog_API@nara.gov)
- Store as environment variable `CATALOG_API_KEY` or enter when prompted

### Storage Requirements
- Adequate disk space for downloads (can be substantial for large collections)
- Recommendation: Use external storage for bulk downloads

## Installation

1. **Install Python 3.6+** from [python.org](https://www.python.org/downloads/)
   - Windows users: Check "Add Python to PATH" during installation

2. **Install required packages:**
   ```bash
   pip install requests PyPDF2 Pillow img2pdf
   ```

3. **Set your API key** (optional but recommended):
   
   **Windows (PowerShell):**
   ```powershell
   $env:CATALOG_API_KEY="your_api_key_here"
   ```
   
   **Mac/Linux (Terminal):**
   ```bash
   export CATALOG_API_KEY="your_api_key_here"
   ```

4. **Download the script** to your preferred location

## How to Use

### Basic Usage

1. Open your terminal/command prompt
2. Navigate to the script directory
3. Run the script:
   ```bash
   python combinedDigitalObjectScript.py
   ```
4. Follow the interactive menu prompts

### Step-by-Step Walkthrough

#### Step 1: Choose Your Discovery Method

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
  - Advanced: `q=aviation&typeOfMaterials=Maps&year=1945`
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

```bash
python combinedDigitalObjectScript.py
```
- Choose: **1** (Single NAID)
- Enter NAID: `12345678`
- Choose: **D** (Download)
- PDF Option: **y** (yes)

**Result:** Folder `12345678/` containing images and `12345678.pdf`

---

### Use Case 2: Download an Entire Series

**Scenario:** You want all records in Series 654321 as original files (no PDF).

```bash
python combinedDigitalObjectScript.py
```
- Choose: **2** (Parent NAID)
- Enter Parent NAID: `654321`
- Choose: **D** (Download)
- PDF Option: **n** (no)

**Result:** Folder `Collection_654321/` with subfolders for each child record

---

### Use Case 3: Keyword Search + Generate Manifest Only

**Scenario:** Search for "Apollo 11" and create a list without downloading.

```bash
python combinedDigitalObjectScript.py
```
- Choose: **3** (Custom search)
- Project Name: `Apollo11_Photos`
- Search Terms: `Apollo 11 photographs`
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
q=maps&typeOfMaterials=Maps&year=1945
```

**Multiple parameters:**
```
q=Kennedy&ancestorNaId=654321&availableOnline=true
```

**Reference:** [API Documentation](https://catalog.archives.gov/api/v2/docs/)

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

## Error Handling and Resume Support

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

### Common Issues

**"No records with digital objects were found"**
- **Cause**: Your search criteria didn't match any digitized records
- **Solution**: 
  - Check your NAID is correct
  - Verify the records have `availableOnline=true`
  - Try broader search terms
  - Check the Catalog website to confirm digital objects exist

**"API Error 400 or status code not 200"**
- **Cause**: Invalid query or API unavailable
- **Solution**:
  - Verify your NAID is correct (numbers only)
  - Check your internet connection
  - For custom searches, verify query syntax
  - Wait a few minutes and retry (API might be busy)

**"Failed to process [filename]"**
- **Cause**: Image file might be corrupted or unsupported format
- **Solution**:
  - Check the original file was downloaded completely
  - Verify the file format is supported (JPG, TIF/TIFF)
  - Re-run the script to re-download
  - If issue persists, that specific file may be problematic

**"Permission denied" or "Cannot delete temp files"**
- **Cause**: Files are locked by another process or permission issue
- **Solution**:
  - Close any programs viewing the files
  - Wait a few seconds and the script will retry
  - Run with administrator privileges (Windows)
  - Check folder permissions

**PDF creation fails with "temp PDF cannot be deleted"**
- **Cause**: PDF merger hasn't released file handles
- **Solution**: The script includes automatic delays and retry logic
  - If it continues failing, try smaller batches
  - Check available disk space
  - Close other programs that might be accessing files

### Performance Tips

**Slow downloads:**
- Normal for large image files (TIF files can be 50+ MB each)
- Check your internet speed
- Use external storage with fast write speeds
- Consider downloading during off-peak hours

**High memory usage during PDF creation:**
- Expected when processing many/large images
- Close other applications to free RAM
- Process smaller batches if needed
- Consider using the "no PDF" option for huge collections

**Disk space issues:**
- Plan ahead: TIFF files require significant space
- Use external drives for large collections
- Clean up `Compressed/` folder if script fails mid-process
- Monitor disk space during long downloads

## Comparison with Individual Scripts

### When to Use This Combined Script

✅ **Use the Combined Script when:**
- You want one tool for multiple scenarios
- You like interactive, guided workflows
- You're experimenting or doing varied research
- You want flexibility without switching scripts

### When to Use Individual Scripts

✅ **Use Individual Scripts when:**
- You have a specific, repeated workflow
- You're automating with shell scripts
- You want minimal prompts for batch processing
- You need specific features unique to one script

### Feature Comparison

| Feature | Combined Script | Individual Scripts |
|---------|----------------|-------------------|
| Single NAID download | ✅ | ✅ |
| Parent NAID (series) | ✅ | ✅ |
| Custom search | ✅ | ✅ |
| CSV processing | ✅ | ✅ |
| PDF creation | ✅ Optional | Some scripts |
| CSV manifest only | ✅ | One script |
| Interactive menu | ✅ | ❌ |
| Automation-friendly | Moderate | ✅ |
| Single script file | ✅ | ❌ |

## Best Practices

### Before Starting Large Downloads

1. **Test with small datasets first**
   - Try a single NAID before downloading a series
   - Verify output format meets your needs

2. **Check available disk space**
   - Use external storage for large collections
   - Plan for ~2-3x space if creating PDFs (original + PDF)

3. **Generate CSV manifest first**
   - Option C lets you preview what will download
   - Review the manifest before committing to download

4. **Verify your API key is working**
   - Test with a known NAID first
   - Check monthly query limits

### During Downloads

1. **Don't interrupt unnecessarily**
   - Let the script complete when possible
   - If you must stop, use Ctrl+C (resume later)

2. **Monitor disk space**
   - Large downloads can fill drives quickly
   - Script doesn't automatically check disk space

3. **Check logs for errors**
   - Review console output for failed downloads
   - Note any repeated errors (might indicate a problem)

### After Downloads

1. **Verify completeness**
   - Check that expected folders were created
   - Review `processed_naids.txt` for completion status

2. **Handle failed records**
   - Script logs failed NAIDs
   - Re-run to retry failed downloads
   - Some failures may require manual investigation

3. **Backup your data**
   - Copy downloaded files to backup storage
   - Save CSV manifests for record-keeping

## API Usage and Quotas

### Understanding API Limits

- **Default limit**: 10,000 queries per month
- **Each search counts**: Discovery phase uses queries
- **Large series**: Can consume many queries quickly
- **Monitor usage**: Contact [Catalog_API@nara.gov](mailto:Catalog_API@nara.gov) for current usage

### Staying Within Limits

1. **Use CSV workflow for large projects:**
   - First: Generate manifest (uses queries)
   - Then: Download from CSV (no additional queries)

2. **Be specific in searches:**
   - Narrow searches = fewer results = fewer queries
   - Use parent NAIDs when possible (more efficient)

3. **Plan ahead:**
   - Generate manifests to estimate query usage
   - Schedule large downloads across multiple months

## Technical Details

### File Processing Logic

**Image to PDF Conversion:**
1. Images sorted using natural sorting algorithm
2. TIFF/TIF files: Converted directly to PDF (multi-page aware)
3. JPG files: Compressed to 45% quality → Saved to temp → Converted to PDF
4. Individual PDFs created for each image
5. All PDFs merged into single document per NAID
6. Temporary files and folders cleaned up

**File Handle Management:**
- PDFs explicitly closed after merging
- 0.5 second delay before cleanup to ensure file release
- Automatic retry logic for locked files

### Directory Structure

```
JobName/
├── processed_naids.txt       # Resume tracking
├── NAID_1/                   # Individual record folders
│   ├── original_files.*
│   └── NAID_1.pdf           # (if PDF enabled)
├── NAID_2/
├── Manifest_JobName.csv     # (if CSV option chosen, <100k rows)
├── Manifest_JobName_part1.csv  # (if CSV option, >100k rows)
├── Manifest_JobName_part2.csv  # (split files for large datasets)
└── Manifest_JobName_part3.csv
```

### Resume Mechanism

The script maintains `processed_naids.txt`:
- One NAID per line
- Written after successful completion
- Checked at start of each NAID processing
- Failed NAIDs excluded (will retry)

## Support and Resources

### Getting Help

**For script issues:**
- Review this documentation thoroughly
- Check the Troubleshooting section
- Email: [Catalog_API@nara.gov](mailto:Catalog_API@nara.gov)

**For API questions:**
- [API Documentation](https://www.archives.gov/data/api)
- [API Swagger Interface](https://catalog.archives.gov/api/v2/docs/)
- [GitHub Repository](https://github.com/usnationalarchives/catalog-api)

**For understanding records:**
- [National Archives Data Model](https://www.archives.gov/research/data-model)
- [Search the Catalog](https://catalog.archives.gov/)

### Reporting Issues

When reporting issues, include:
- Your operating system and Python version
- The exact steps you followed
- Any error messages (copy and paste)
- Example NAID or search terms (if not sensitive)
- What you expected vs. what happened

## License and Attribution

**Created by:** National Archives Catalog API Team  
**Contact:** [Catalog_API@nara.gov](mailto:Catalog_API@nara.gov)

**Required Attribution:**
If you use this script or the National Archives Catalog API for any public service or application, you must display:
> "This product uses the National Archives Catalog API but is not endorsed or certified by the National Archives and Records Administration."

---

## Quick Reference

### Running the Script
```bash
python combinedDigitalObjectScript.py
```

### Required Packages
```bash
pip install requests PyPDF2 Pillow img2pdf
```

### Setting API Key
**Windows:**
```powershell
$env:CATALOG_API_KEY="your_key"
```

**Mac/Linux:**
```bash
export CATALOG_API_KEY="your_key"
```

### Menu Options Quick Guide
| Option | Purpose | When to Use |
|--------|---------|-------------|
| 1 | Single NAID | One specific record |
| 2 | Parent NAID | Entire series/collection |
| 3 | Custom Search | Keywords or complex queries |
| 4 | CSV File | Pre-generated URL list |
| D | Download | Get actual files |
| C | CSV Only | Generate manifest without downloading |
| y | Create PDF | Combine images into PDF |
| n | No PDF | Keep original formats |

---

**Last Updated:** February 2026  
**Script Version:** Combined Digital Object Script v1.0
