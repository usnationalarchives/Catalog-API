Using the National Archives Catalog API
==================

## Contents

- **[What is the API?](#what-is-the-api)**
- **[What data does the API contain?](#what-data-does-the-api-contain)**
- **[What can the API do?](#what-can-the-api-do)**
- **[How can I use NARA's data?](#how-can-i-use-naras-data)**
- **[How do I get access to the API?](#how-do-i-get-access-to-the-api)**
- **[What are the limits imposed?](#what-are-the-limits-imposed)**
- **[What is the current version?](#what-is-the-current-version)**
- **[Does NARA have other datasets and APIs not included in the catalog API?](#does-nara-have-other-datasets-and-apis-not-included-in-the-catalog-api)**
- **[Where can I report issues?](#where-can-i-report-issues)**

## What is the API?

The [National Archives Catalog API](https://catalog.archives.gov/api/v2/api-docs/) is a read–write web API for the online catalog for the National Archives. The Catalog API provides a structured way to search Description and Authority elements that exist within the Catalog dataset as an alternative to searching directly within the [Catalog](https://catalog.archives.gov/) user interface.

The URL path for the API is: [`https://catalog.archives.gov/api/v2/api-docs`](https://catalog.archives.gov/api/v2/api-docs/)

## What data does the API contain?

The National Archives Catalog API contains:

- All available archival descriptions
- Authority record metadata (persons, organizations, geographic references, topical subjects, and specific records types)
- Digital object metadata (including technical metadata)
- Public contributions to the catalog (tags, transcriptions, comments)
- Extracted text metadata (such as optical character recognition or OCR text)
- Limited metadata for user accounts

## What can the API do?

The API's main functions include querying for metadata, exporting metadata in bulk, and posting tags and transcriptions to records.

When searching, you may return the full metadata for each record, or specify one or more specific fields. You can search by keyword and/or by any combination of field values, and apply sorting.

The API may also be used to facilitate bulk downloads of records from the National Archives Catalog.

## How can I use NARA's data?

NARA's archival metadata is all assumed to be in the public domain, as a work of the federal government, with only rare exceptions (like quotations from other sources).

Digital images themselves are generally also in the public domain for the same reason. In general, all government records are in the public domain and may be freely used. We do have some donated or other materials that might be copyrighted (though these are often not displayed in our catalog). Please read the instructions noted in the "Use Restrictions" field of each catalog record for more information about rights, or speak to the archivist or reference staff that handles those records.

For more information, please read [NARA's FAQ on copyright](http://www.archives.gov/faqs/index.html#copyright).

## How do I get access to the API?

To request a Catalog API key, please send an email to Catalog_API@nara.gov with your name and the email address you would like associated with your key. You may request a read-only key which will allow you to query the National Archives Catalog dataset, or a read/write key which will allow you to both query the dataset and write or edit contributions to the Catalog. If you are requesting a read/write key, you must have an active Catalog account.

To set up a Catalog account, you may visit the [Catalog](https://catalog.archives.gov/) and click Log in/Sign Up in the top right corner. Please be sure to use the same email you wish to have associated with your Catalog API key.

### How to run your first API call:
**Step 1: Open the Command-Line Interface (CLI)**
+ **Windows:** Press Windows + R, type cmd, and hit Enter to open the Command Prompt.
+ **Mac:** Press Command + Space, type Terminal, and hit Enter.
+ **Linux:** Open the Terminal from your system's applications menu or press Ctrl + Alt + T.

**Step 2: Install curl (if it's not already installed)**
+ **Windows:** Recent versions of Windows include curl by default. To check, type curl --version and press Enter.
+ **Mac and Linux:** curl is typically pre-installed. To check, type curl --version in the terminal and press Enter.

**Step 3: Get your API Key**
+ Make sure you have your API key that was provided by our Catalog engineers. You will replace YOUR_API_KEY in the command with the API key issued by our Catalog engineers.

**Step 4: Run the curl Command**
+ Once you have curl installed and your API key ready, you can run the following command in the terminal. 
```
curl --location --request GET “https://catalog.archives.gov/api/v2/records/search?q=constitution" --header "Content-Type: application/json" --header "x-api-key: YOUR_API_KEY"
```

**Step 5: View the Response**
+ After running the command, you should see a response from the API printed in the terminal. It will be a JSON-formatted output that includes the search results.

**Step 6: Saving the Output (Optional)**
+ If you want to save the output to a file instead of viewing it in the terminal, you can modify the command like this:
```
curl --location --request GET "https://catalog.archives.gov/api/v2/records/search?q=constitution" --header "Content-Type: application/json" --header "x-api-key: YOUR_API_KEY" -o output.json
```
+ The output.json command will save the results to a JSON file in the current directory.

## What are the limits imposed?

To ensure consistent system and API availability and performance, NARA limits the number of Catalog API requests to a default rate of 10,000 queries per month per API key. Exceeding this limit will cause the API key to be temporarily blocked until the first of the following month. Your API key query rate limit will automatically reset and be renewed on the first of every month. 

Most use cases and research needs can be met by the default API limit. If your research or development efforts require a higher limit, please contact Catalog_API@nara.gov with your use case/research need and justification. NARA staff determines the issuance of a higher limit based on Catalog API performance.

## What is the current version?

The current version of our catalog API is v2, which was released in September 2022. As improvements are made to the current version, we will try to ensure backwards compatibility.

The base URL, [`https://catalog.archives.gov/api/v2/api-docs/`](https://catalog.archives.gov/api/v2/api-docs/), will always contain the API version.

## Does NARA have other datasets and APIs not included in the catalog API?

Yes! NARA's [Open Government portal](http://www.archives.gov/open/) contains a listing of NARA's [High-Value Datasets](http://www.archives.gov/open/available-datasets.html), many of which are also available by searching data.gov. Some of these datasets deal with data which would not be found in our online catalog of archival materials.

NARA's [Office of the Federal Register](federalregister.gov) also has an API for its dataset of government publications. You can find more information about it at the OFR's [developer portal](https://www.federalregister.gov/learn/developers).

## Where can I report issues?

We welcome reports of issues, whether they are bugs in the system, ideas for improvements, or problems with the underlying data. Please report them using the GitHub issue tracker [for this repository](https://github.com/usnationalarchives/Catalog-API/issues), or by email to Catalog_API@nara.gov.
