
# File Unit API Downloader Script

## Description

This Python script interacts with the National Archives Catalog API to search for and download digital objects attached to file units within a specific series. It queries the API for records, extracts object URLs, saves them to a CSV file, and downloads the digital objects into separate folders named after the file unit NAIDs.

### Features:
- Queries the Catalog API for digital objects linked to file units within a specific series.
- Downloads digital objects into directories based on the file unit NAID.
- Uses the `nextCursorMark` to handle more than 10,000 results (the maximum limit per API query).
- Automatically creates directories for each parent file unit NAID if they do not already exist.
- Cleans up the CSV file after downloading the objects.

## Prerequisites

- Python 3.x
- Required libraries:
  - `requests`
  - `json`
  - `csv`
  - `os`
  - `datetime`
  - `urllib`
  - `PIL` (Pillow)

## Setup

### 1. API Key
Before running the script, ensure you have your API Key. The script will first check if the API Key is set as an environmental variable. If it's not, it will prompt you to enter the key manually.

To set the API Key as an environmental variable:

```bash
export CATALOG_API_KEY="your_api_key_here"
```

Alternatively, you can manually enter the API Key when prompted by the script.

### 2. Install Dependencies
You can install the required libraries using `pip`:

```bash
pip install requests pillow
```

## Usage

### Running the Script

1. Clone this repository or copy the script into your local machine.
2. Ensure that the required dependencies are installed.
3. Run the script by executing:

```bash
python3 script_name.py
```

### Input Prompts
- **Do you have your API Key set as an environmental variable (Y/N)?**  
  Enter `Y` if the API Key is set as an environmental variable, or `N` to manually input the API Key.
  
- **Enter your API Key:**  
  If you chose `N` in the previous step, enter the API Key when prompted.

- **Parent NAID:**  
  Enter the parent file unit NAID for the series you want to query.

### Output
- **CSV File:**  
  A CSV file named `ListOfObjectsToDownload_{NAID}.csv` will be generated, containing the parent NAID and object URL pairs.
  
- **Downloaded Files:**  
  Files will be downloaded into directories named after the parent NAID. For example, the directory structure will look like:
  
  ```bash
  /{parent_naid}/{file_name}
  ```

### Example Output:
```
Downloading: /123456789/abcd1234/image1.jpg
Downloading: /123456789/abcd1234/image2.jpg
All Files downloaded! 12:30:00
```

## Troubleshooting

- If you encounter errors related to the API response, ensure your API Key is correct and that the API service is operational.
- If the file download fails, verify your network connection or retry the download.

## License

This script is released under the MIT License. Feel free to modify it according to your needs.

## Author

This script was created by [Your Name].
