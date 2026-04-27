"""
National Archives Digital Object Tool

What this script does:
- Discovers digital object URLs from the National Archives Catalog API or a local CSV.
- Supports discovery by single NAID, parent NAID, custom query string, or CSV input.
- Lets you either download files by record (NAID) or create CSV manifest files.
- When creating CSV output, it writes manifest part files in chunks of 100,000 rows each.
- If discovery returns no records with digital objects, it asks whether to search again or quit.

CSV input expectations (option 4):
- Header row is skipped.
- Column order is: NAID, URL, optional Title.

How to use:
- Run the script and choose option 1-4 from the menu.
- Provide an API key when prompted (or set CATALOG_API_KEY in your environment).
- Choose Download mode or CSV manifest mode after discovery completes.
"""

import requests
import json
import csv
import os
import datetime
import img2pdf
import shutil
import re
import time
import logging
from pathlib import Path
from urllib.parse import parse_qsl
from PIL import Image, ImageSequence
from PyPDF2 import PdfMerger

# --- Configuration ---
CATALOG_API_BASE_URL = 'https://catalog.archives.gov/api/v2/records/search'
MAX_PDF_FILE_SIZE_MB = 500 

# --- Logging Setup ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def prompt_yes_no(prompt_text):
    """Prompt until user enters Yes/No (Y/N), returning True for yes and False for no."""
    while True:
        response = input(prompt_text).strip().lower()
        if response in ('y', 'yes'):
            return True
        if response in ('n', 'no'):
            return False
        print("Please enter Yes or No (Y/N).")

def get_api_key():
    """Checks for API Key in environment or prompts user."""
    api_key = os.environ.get('CATALOG_API_KEY')
    if not api_key:
        print("\nAPI Key not found in system environment.")
        api_key = input('Please enter your Catalog API Key: ').strip()
    if not api_key:
        logging.error("API Key is required to proceed.")
        exit()
    return api_key

def _get_api_results(url_params, headers):
    """Generic NARA API v2 paginator that handles query strings safely."""
    all_objects = {}
    search_after = "*"
    page = 0
    session = requests.Session()
    user_params = dict(parse_qsl(url_params))

    logging.info("Searching the National Archives Catalog...")

    while True:
        params = {
            'limit': 100,
            'searchAfter': search_after,
            'availableOnline': 'true'
        }
        params.update(user_params)

        try:
            response = session.get(CATALOG_API_BASE_URL, headers=headers, params=params)
            if response.status_code != 200:
                logging.error(f"API Error {response.status_code}. The Catalog might be busy or the query is incorrect.")
                break
            
            data = response.json()
            hits = data.get('body', {}).get('hits', {}).get('hits', [])
            if not hits:
                break
                
            for hit in hits:
                record = hit.get('_source', {}).get('record', {})
                naid = str(record.get('naId'))
                title = record.get('title') or ''
                digital_objects = record.get('digitalObjects', []) or []
                urls = [obj.get('objectUrl') for obj in digital_objects if obj.get('objectUrl')]
                if urls:
                    if naid in all_objects:
                        # merge urls if NAID already seen and preserve title if missing
                        all_objects[naid]['urls'].extend(urls)
                        if not all_objects[naid].get('title') and title:
                            all_objects[naid]['title'] = title
                    else:
                        all_objects[naid] = {'urls': urls, 'title': title}
            
            page += 1
            search_after = hits[-1].get('sort', [""])[0]
            logging.info(f"Found {len(all_objects)} records so far (Page {page})...")
            
        except json.decoder.JSONDecodeError:
            logging.error("Received an invalid response from the server. Please check your search formatting.")
            break
        except Exception as e:
            logging.error(f"Discovery error: {e}")
            break
            
    return all_objects

def run_pdf_logic(naid, naid_dir):
    """Conversion, merge, and strict cleanup with natural sorting and explicit closing."""
    if any(f.suffix.lower() == '.pdf' for f in naid_dir.iterdir() if not f.name.startswith("temp_")):
        logging.info(f"Record {naid} already contains a master PDF. Skipping PDF creation.")
        return True

    comp_dir = naid_dir / 'Compressed'
    comp_dir.mkdir(exist_ok=True)
    temp_pdfs = []

    try:
        def natural_keys(path):
            return [int(c) if c.isdigit() else c.lower() for c in re.split('([0-9]+)', path.name)]

        files = sorted(naid_dir.iterdir(), key=natural_keys)
        
        # 1. Generate temp PDFs from images
        for img in files:
            if img.suffix.lower() in ('.jpg', '.jpeg', '.tif', '.tiff'):
                pdf_out = naid_dir / f"temp_{img.stem}.pdf"
                try:
                    if img.suffix.lower() in ('.tif', '.tiff'):
                        with Image.open(img) as i:
                            imgs = [p.convert('RGB') for p in ImageSequence.Iterator(i)]
                            imgs[0].save(pdf_out, save_all=True, append_images=imgs[1:]) if len(imgs)>1 else imgs[0].save(pdf_out)
                    else:
                        with Image.open(img) as i:
                            i.save(comp_dir / img.name, "JPEG", optimize=True, quality=45)
                        with open(pdf_out, 'wb') as f:
                            f.write(img2pdf.convert(str(comp_dir / img.name)))
                    temp_pdfs.append(pdf_out)
                except Exception as e:
                    logging.error(f"Failed to process {img.name}: {e}")

        # 2. Merge temporary PDFs into one
        if temp_pdfs:
            merger = PdfMerger()
            for p in temp_pdfs:
                merger.append(str(p))
            
            final_pdf_path = naid_dir / f"{naid}.pdf"
            with open(final_pdf_path, 'wb') as f:
                merger.write(f)
            
            merger.close() # CRITICAL: Releases the files so they can be deleted
            logging.info(f"Successfully created combined PDF for {naid}")
            return True
        return False

    except Exception as e:
        logging.error(f"PDF creation error for {naid}: {e}")
        return False

    finally:
        time.sleep(0.5) # Give the OS a moment to release file handles
        for p in temp_pdfs:
            if p.exists():
                try: p.unlink()
                except: pass
        if comp_dir.exists():
            try: shutil.rmtree(comp_dir)
            except: pass

def main():
    api_key = get_api_key()
    headers = {'x-api-key': api_key}
    
    while True:
        print("\n" + "="*45)
        print("   NATIONAL ARCHIVES DIGITAL OBJECT TOOL")
        print("="*45)
        print("What would you like to do?")
        print("  1. Download files from ONE specific record (Single NAID)")
        print("  2. Download ALL records inside a Series/Collection (Parent NAID)")
        print("  3. Run a custom search (Keywords or API query)")
        print("  4. Process an existing list of URLs from a local CSV")

        choice = input("\nSelect an option (1-4): ").strip()

        all_objects_map = {}
        job_name = ""

        # --- 1. Discovery Phase ---
        if choice == '1':
            naid = input("Enter the NAID (Record ID): ").strip()
            job_name = naid
            all_objects_map = _get_api_results(f"naId={naid}", headers)
        elif choice == '2':
            naid = input("Enter the Parent NAID (Series or Collection ID): ").strip()
            job_name = f"Collection_{naid}"
            all_objects_map = _get_api_results(f"ancestorNaId={naid}", headers)
        elif choice == '3':
            job_name = input("Give this project a name (for the folder): ").strip()
            print("Tip: You can enter keywords or a full API string (e.g., q=aviation&typeOfMaterials=Maps)")
            query = input("Enter search terms: ").strip()
            all_objects_map = _get_api_results(query, headers)
        elif choice == '4':
            csv_file_path = input("Enter the full path to your CSV file (with extension): ").strip()
            csv_path = Path(csv_file_path)
            if not csv_path.exists():
                logging.error(f"CSV file not found: {csv_file_path}")
            else:
                job_name = csv_path.stem

                with open(csv_path, 'r', encoding='utf-8') as f:
                    reader = csv.reader(f)
                    next(reader)  # Skip header row
                    for row in reader:
                        if len(row) >= 2:
                            naid = row[0]
                            url = row[1]
                            title = row[2] if len(row) >= 3 else ''
                            entry = all_objects_map.setdefault(naid, {'urls': [], 'title': title})
                            entry['urls'].append(url)
                            if not entry.get('title') and title:
                                entry['title'] = title
        else:
            logging.warning("Invalid option selected.")

        if all_objects_map:
            break

        logging.warning("No records with digital objects were found.")
        search_again = prompt_yes_no("Would you like to search again? (Yes/No): ")
        if not search_again:
            logging.info("Quitting.")
            return

    # --- 2. Action Selection ---
    # Create the job folder immediately so we have a place to save the manifest
    base_dir = Path(job_name)
    base_dir.mkdir(exist_ok=True)

    print(f"\nFound {len(all_objects_map)} records containing digital objects.")
    print("-" * 45)
    print("What should I do with these?")
    print("  [D] Download the actual files to my computer")
    print("  [C] Just create a CSV spreadsheet listing the file links")
    action = input("\nChoose D or C: ").lower()
    
    if action == 'c':
        # Collect all rows first to count total and split
        all_rows = []
        for naid, info in all_objects_map.items():
            # support old-style list values and new dict values
            if isinstance(info, dict):
                urls = info.get('urls', [])
                title = info.get('title', '')
            else:
                urls = info
                title = ''
            for url in urls:
                all_rows.append([naid, url, title])
        
        # Split into parts at every 100,000 rows
        max_rows_per_file = 100000
        num_rows = len(all_rows)

        num_parts = max(1, (num_rows + max_rows_per_file - 1) // max_rows_per_file)
        logging.info(f"Total rows: {num_rows} - Writing {num_parts} part file(s) with up to {max_rows_per_file} rows each...")

        for part_idx in range(num_parts):
            start_row = part_idx * max_rows_per_file
            end_row = min(start_row + max_rows_per_file, num_rows)
            part_rows = all_rows[start_row:end_row]

            out_csv = base_dir / f"Manifest_{job_name}_part{part_idx + 1}.csv"
            with open(out_csv, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['NAID', 'URL', 'Title'])
                writer.writerows(part_rows)
            logging.info(f"Saved: {out_csv.name} ({end_row - start_row} rows)")
        
        return

    # --- 3. Download / Resume Logic ---
    print("\nPDF SETTINGS:")
    make_pdf = input("Combine images into a single PDF for each record? (y/n): ").lower() == 'y'
    
    resume_file = base_dir / "processed_naids.txt"
    processed_naids = set()
    if resume_file.exists():
        processed_naids = set(resume_file.read_text().splitlines())

    failed_naids = []
    session = requests.Session()
    
    logging.info(f"Starting downloads into folder: {base_dir.absolute()}")
    logging.info(f"Already processed: {len(processed_naids)}, Remaining: {len(all_objects_map) - len(processed_naids)}")

    for naid, info in all_objects_map.items():
        if naid in processed_naids:
            continue

        # support both legacy list values and new dict values
        urls = info.get('urls') if isinstance(info, dict) else info

        naid_dir = base_dir / naid
        naid_dir.mkdir(parents=True, exist_ok=True)
        logging.info(f"Processing NAID {naid} with {len(urls)} URLs")

        for url in urls:
            file_path = naid_dir / url.rsplit('/', 1)[-1]
            if not file_path.exists():
                try:
                    logging.info(f"Downloading: {url}")
                    r = session.get(url, stream=True, timeout=30)
                    r.raise_for_status()
                    with open(file_path, 'wb') as f:
                        for chunk in r.iter_content(8192): f.write(chunk)
                    logging.info(f"Saved: {file_path.name}")
                except Exception as e:
                    logging.error(f"Download failed for {url}: {e}")

        success = True
        if make_pdf:
            success = run_pdf_logic(naid, naid_dir)
        
        if success:
            with open(resume_file, "a") as f: f.write(f"{naid}\n")
            processed_naids.add(naid)
        else:
            failed_naids.append(naid)

    # --- Final Summary ---
    logging.info("="*45)
    logging.info("PROCESS COMPLETE")
    logging.info(f"Records successfully finished: {len(processed_naids)}")
    if failed_naids:
        logging.warning(f"Records with errors (check these manually): {', '.join(failed_naids)}")
    logging.info(f"All files are saved in: {base_dir.absolute()}")

if __name__ == "__main__":
    main()