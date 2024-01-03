> <sup>**Quick links:** This page is a basic FAQ about NARA's online catalog API. If you would like to dive right in and play around, try the sandbox. <br/> Jump to advanced documentation: </sup><br/>
> &nbsp; &nbsp; &nbsp; <sup>**[Search and export](search_and_export.md)** | **[Posting contributions](posting_contributions.md)** | **[Interactive API sandbox](https://catalog.archives.gov/interactivedocumentation)**</sup>

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

The [National Archives Catalog API](https://catalog.archives.gov/api/v2/api-docs) is a read–write web API for the online catalog for the National Archives.

The URL path for the API is: [`https://catalog.archives.gov/api/v2/api-docs`](https://catalog.archives.gov/api/v2/api-docs)

## What data does the API contain?

The National Archives Catalog API contains all:

- Archival description metadata
- Authority record (persons, organizations, geographic references, topical subjects, and specific records types) metadata
- Digital object metadata (including technical metadata)
- Public contributions to the catalog (like tags and transcriptions)
- Metadata for crawled web pages of archives.gov and presidential libraries
- Some metadata for user accounts

## What can the API do?

The API's main functions include querying for metadata, exporting metadata in bulk, and posting tags and transcriptions to records.

When searching, you may return the full metadata for each record, or specify one or more specific fields. You can search by keyword and/or by any combination of field values, and apply sorting.

## How can I use NARA's data?

NARA's archival metadata is all assumed to be in the public domain, as a work of the federal government, with only rare exceptions (like quotations from other sources).

Digital images themselves are generally also in the public domain for the same reason. In general, all government records are in the public domain and may be freely used. We do have some donated or other materials that might be copyrighted (though these are often not displayed in our catalog). Please read the instructions noted in the "Use Restrictions" field of each catalog record for more information about rights, or speak to the archivist or reference staff that handles those records.

For more information, please read [NARA's FAQ on copyright](http://www.archives.gov/faqs/index.html#copyright).

## How do I get access to the API?

We strive for openness as much as possible in our API. That means that you can get started querying the API right now without any account or API key. For system performance reasons, there are some basic limits on how many rows or total results you can request, as well as the rate at which you can query—but you can create an account in order to increase those limits.

You will need to create an account and log in to perform write actions like tagging and transcription, which are attributed to your account. You are contributing to the same records and using the same accounts as in the [NARA catalog UI](https://catalog.archives.gov/).

## What are the limits imposed?

The system imposes limits on how much data you can request (based on maximum row and/or offset limits) and how fast you can request it (based on maximum number of queries per IP/user in a given time). The specific limits are different depending on the type of account (not logged in, registered user/moderator, or power user) and are not yet defined, but if you encounter a limit, you will receive a 400 error with a message describing the issue.

## What is the current version?

The current (and so far only) version of our catalog API is v1, which was released in December 2014. As improvements are made to the current version, we will try to ensure backwards compatibility.

The base URL, [`https://catalog.archives.gov/api/v1/`](https://catalog.archives.gov/api/v1/), will always contain the API version.

## Does NARA have other datasets and APIs not included in the catalog API?

Yes! NARA's [Open Government portal](http://www.archives.gov/open/) contains a listing of NARA's [High-Value Datasets](http://www.archives.gov/open/available-datasets.html), many of which are also available by searching data.gov. Some of these datasets deal with data which would not be found in our online catalog of archival materials.

NARA's [Office of the Federal Register](federalregister.gov) also has an API for its dataset of government publications. You can find more information about it at the OFR's [developer portal](https://www.federalregister.gov/learn/developers).

## Where can I report issues?

We welcome reports of issues, whether they are bugs in the system, ideas for improvements, or problems with the underlying data. Please report them using the the GitHub issue tracker [for this repository](https://github.com/usnationalarchives/Catalog-API/issues), or by email to api@nara.gov.

