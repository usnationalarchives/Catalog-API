> <sup>**Quick links:** This page is documentation about NARA's online catalog API. If you would like to dive right in and play around, try the sandbox. <br/> Jump to advanced documentation: </sup><br/>
> &nbsp; &nbsp; &nbsp; <sup>**[Basic API FAQ](README.md)** | **[Posting contributions](posting_contributions.md)** | **[Interactive API sandbox](https://catalog.archives.gov/interactivedocumentation)**</sup>

Using the API for search and export
==================

## Contents

- **[API basics](#api-basics)**
- **[Pagination](#pagination)**
- **[Search by identifier](#search-by-identifier)**
- **[Keyword search](#keyword-search)**
- **[Fielded search](#fielded-search)**
- **[Sorting results](#sorting-results)**
- **[Refining the results](#refining-the-results)**
- ⇢ **[Refining by type](#refining-by-type)**
- ⇢⇢ **[Holdings](#holdings)**
- ⇢⇢ **[Authorities](#authorities)**
- ⇢⇢ **[Web pages](#web-pages)**
- ⇢ **[Refining by field](#refining-by-field)**

## API basics

- [`https://catalog.archives.gov/api/v1/`](https://catalog.archives.gov/api/v1/)` [method]`

There are two ways to get metadata out of the API: search and export. Both methods allow you to retrieve full records or specified fields for records that match the given parameters. Export is used to download data and/or digital media in bulk, and requires an account so you can retrieve the specified export after it is done processing. You also have to use the bulk export method to retrieve metadata in CSV or PDF, since the normal API responses are only in JSON or XML.

You'll notice that if you omit all parameters, and just use the base API path, the API returns a results set of all records in the system without any filtering (limited to the default 10 rows). All search queries are essentially just refinements of this basic search. Technically, search is using `action=search`, but this is unnecessary to include as it is the default action.

Export uses the same parameters for selecting records as search (but you'll use **`action=export`**), plus a few extra options, but is not currently documented here because it is not yet live.

## Pagination

To start with, we'll look at how to paginate the results set. Use the `rows=` parameter to set the number of results that will display in the response. Use `offset=` to specify where in the results set to return your results from.

- [`https://catalog.archives.gov/api/v1/?rows=5&offset=9`](https://catalog.archives.gov/api/v1/?rows=5&offset=9)

Both parameters are optional; when omitted, `rows` defaults to 10 and `offset` defaults to 0 (i.e., starting from the beginning). Note that the results count from 1 (there is no 0), so you would use <code>&offset=1</code> to get the *second* result. So, our sample query above will return results 10–14. The `num` field in the response tells you the number of each result in the set (it can be omitted or included from responses like other metadata fields below).

## Search by identifier

The National Archives Identifier (*NAID*) is the unique identifier for each description (collection, record group, series, file unit, or item) and authority record (organization, person, topical subject, geographical reference, or specific records type). If you already know the NAID you want, you can just search by using `naIds=` followed by the NAID to retrieve the specific record. You can request multiple records by NAID by separating each value with a comma.

- [`https://catalog.archives.gov/api/v1/?naIds=485`](https://catalog.archives.gov/api/v1/?naIds=485)

This will return the all metadata for each record, but you can also fetch only the specific fields you want, as with any search ([see below](#refining-by-field)). Note that web page results (for archives.gov and presidential libraries web sites) do not have their own NAIDs, and cannot be searched in this way.

**Known issues:** 
> - <sup>There is a major bug in the current build which assigns the same NAIDs to digital objects as their parent description. This means you could retrieve greater than 1 result when using (theoretical) unique identifier, unless you specifically ask for descriptions ([see below](#refining-by-type)). To specify a specific object, you would have to use fielded search on the different unique identifier field solely for objects, rather than the NAID, for now.</sup>
- <sup>Note that some authority term names you will come across in the metadata—like restriction notes, names of NARA facilities, or media types—will have NAIDs which cannot be searched on, because we are not currently exporting their metadata.</sup>

## Keyword search

Use `q=` to search by keyword. Keyword search is used to search for your term across all of the fields in a record for matches.

- [`https://catalog.archives.gov/api/v1/?q=armadillo`](https://catalog.archives.gov/api/v1/?q=armadillo)

Separate multiple keywords with a space or comma (this is an AND function). Keywords are optional, and can be combined with other parameters for fielded search. Any search with a keyword will also return a `score` field, which is the search engine's internal relevancy score, and will be automatically sorted by score unless another sort is specified.

## Fielded search

One reason the API can be much more powerful than the UI Advanced Search is that it allows you to construct queries based on search within any number of fields. Specify the path to the fields within the nested hierarchy of the metadata document by using `.` as the separator.

For example, if you would like to construct a very specific search across all series for records with a "Top Secret" security classification, and the term "Army" in the description's title:

- [`https://catalog.archives.gov/api/v1/?description.series.accessRestriction.specificAccessRestrictionArray.specificAccessRestriction.securityClassification.termName=top%20secret&description.series.title=army`](https://catalog.archives.gov/api/v1/?description.series.accessRestriction.specificAccessRestrictionArray.specificAccessRestriction.securityClassification.termName=top%20secret&description.series.title=army)

You can see how specifying fields within the very nested nature of archival descriptions can quickly get complicated. For demonstration, here's where that field is located in the record:

>"result":[<br/>
&nbsp;{<br/>
&nbsp;"num":"1",<br/>
&nbsp;type: "description",<br/>
&nbsp;naId: "305269",<br/>
&nbsp;"description":{<br/>
&nbsp;&nbsp;"series":{<br/>
&nbsp;&nbsp;&nbsp;"accessRestriction":{<br/>
&nbsp;&nbsp;&nbsp;&nbsp;"specificAccessRestrictionArray":{<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"specificAccessRestriction":{<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"restriction":{<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"naId":"10634129",<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"termName":"FOIA (b)(1) National Security"<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;},<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"securityClassification":{<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"naId":"10633163",<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**"termName":"Top Secret"**<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;}<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;}<br/>
[...]

## Sorting results

The results set can be sorted by a given field by using the `sort=` parameter in combination with the field name and either `asc` or `desc`, separated by a space. For example, `sort=naId asc` (or, with URL encoding `sort=naId%20asc`). So, sorting the query for the keyword "navy" by NAIDs from lowest to highest is:

- [`https://catalog.archives.gov/api/v1/?q=navy&sort=naId asc`](https://catalog.archives.gov/api/v1/?q=navy&sort=naId asc)

Fields are coded as either string, integer, or datetime, so that they should sort according to the correct logic.

**Known issue:**

> <sup> Sort is not yet working across all fields. The API is currently coded so that if a field is not sortable, attempting to sort by it will return an error (rather than silently ignoring the parameter).</sup>

## Refining the results

There are two ways to refine the results set from a search: by type or by field. These two can be used in combination, too.

### Refining by type

Typical searches return results across the entire database, unless you specify otherwise. This means all archival descriptions, objects, authority records, and NARA web pages are fair game. If you are only looking for records of a particular type, you can refine your results using `resultTypes=` to specify only the type or types (separated by commas) you want. For example, to return only item-level and file unit-level descriptions, you would query:

- [`https://catalog.archives.gov/api/v1/?resultTypes=item,fileUnit`](https://catalog.archives.gov/api/v1/?resultTypes=item,fileUnit)

There are several possible values for `resultTypes`.

#### Holdings

For holdings, you can individually specify any level of description or objects:

- `item`
- `fileUnit`
- `series`
- `recordGroup`
- `collection`
- `object`

Plus the two following magic words have been created:
- `holding`: metadata for all levels of description as well as objects
- `description`: metadata for all levels of description only (no objects)

#### Authorities 

An authority record is a grouping of metadata about a distinct entity—like a person, organization, place, or other concept—which could be related to and named in archival descriptions. You can specify any of the following types of authority records:

- `person`
- `organization`
- `topicalSubject`
- `geographicReference`
- `specificRecordsType`

Plus, as with descriptions:
- `authority`: to specify all types of authorities

#### Web pages

- `archivesWeb`: archives.gov (non-archival) web page results
- `presidentialWeb`: presidential libraries (non-archival) web page results

And:

- `web`: all archives.gov and presidential libraries web page results

### Refining by field

Unlike refining by type, refining by field will not affect which results are returned, just which bits of metadata within each result should be displayed. Use `resultFields=` to specify one or more fields within the metadata to return. Any should work, though note that not all results will necessarily have the specified field. Also note that `resultsFields` only manipulates the results set after the search is performed, so it will return results where the overall result matched your query's search terms and filters, even if they do not appear in the specified fields (for that, use the fielded search above).

Here is an example of a query where we are returning NAIDs and item titles for all results:

- [`https://catalog.archives.gov/api/v1/?resultFields=naId,description.item.title`](https://catalog.archives.gov/api/v1/?resultFields=naId,description.item.title)

**Known issue:**

> <sup>Note that one quirk of NARA's metadata is that level of description is determined not by the value of one field, but by the *structure* of the metadata. So if you are looking for the title in all levels of description, you will have to specify each of `description.item.title`, `description.fileUnit.title`, `description.series.title`, and so on in `resultFields` (or else, as in the example above, it will only return titles for items, but not other types of records).</sup>
