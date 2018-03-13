> <sup>**Quick links:** This page is documentation about NARA's online catalog API. If you would like to dive right in and play around, try the sandbox. <br/> Jump to advanced documentation: </sup><br/>
> &nbsp; &nbsp; &nbsp; <sup>**[Basic API FAQ](README.md)** | **[Posting contributions](posting_contributions.md)** | **[Interactive API sandbox](https://catalog.archives.gov/interactivedocumentation)**</sup>

Using the API for search and export
==================

## Contents

- **[API basics](#api-basics)**
- **[Pagination](#pagination)**
- ⇢ **[Basic pagination](#basic-pagination)**
- ⇢ **[Cursor-based pagination](#cursor-based-pagination)**
- **[Search by identifier](#search-by-identifier)**
- **[Keyword search](#keyword-search)**
- **[Fielded search](#fielded-search)**
- ⇢ **[Search operators](#search-operators)**
- **[Field testing](#field-testing)**
- **[Sorting results](#sorting-results)**
- **[Refining the results](#refining-the-results)**
- ⇢ **[Refining by type](#refining-by-type)**
- ⇢⇢ **[Holdings](#holdings)**
- ⇢⇢ **[Authorities](#authorities)**
- ⇢⇢ **[Web pages](#web-pages)**
- ⇢ **[Refining by field](#refining-by-field)**

## API basics

- [**GET**] [`https://catalog.archives.gov/api/v1/`](https://catalog.archives.gov/api/v1/) + `parameters`

There are two ways to get metadata out of the API: search and export. Both methods allow you to retrieve full records or specified fields for records that match the given parameters. Export is used to download data and/or digital media in bulk, and requires an account so you can retrieve the specified export after it is done processing. You also have to use the bulk export method to retrieve metadata in CSV or PDF, since the normal API responses are only in JSON or XML.

You'll notice that if you omit all parameters, and just use the base API path, the API returns a results set of all records in the system without any filtering (limited to the default 10 rows). All search queries are essentially just refinements of this basic search. Technically, search is using `action=search`, but this is unnecessary to include as it is the default action.

Export uses the same parameters for selecting records as search (but you'll use **`action=export`**), plus a few extra options, but is not currently documented here because it is not yet live.

## Format

Before we begin, a word on format. The API is designed to output responses in JSON by default. It is also defaulting to pretty-printed outputs, which means (depending on browser) you can likely go to any of the search queries linked on this page in your browser and see the structured data in a readable style. If you would like to turn off the pretty-printing for any reason, you can use `pretty=false`.

You can use the optional `format` parameter to change the format of the response to XML, like so:

- [`https://catalog.archives.gov/api/v1/?format=xml`](https://catalog.archives.gov/api/v1/?format=xml)

## Pagination

To start with, we'll look at how to paginate the results set. There are two different ways to paginate which you can choose from depending on your needs. Cursor-based pagination is necessary for performance reasons when you need to access over 10,000 results, but it requires you to page through all previous results to get to a result you want—whereas basic pagination allows you to use an offset value to specify any result(s) you want within the first 10,000 results in a single query.

### Basic pagination
For up to 10,000 results, you can simply apply the `rows` and `offset` parameters to specify which results to display.  Use the `rows=` parameter to set the number of results that will display in the response. Use `offset=` to specify where in the results set to return your results from.

- [`https://catalog.archives.gov/api/v1/?rows=5&offset=9`](https://catalog.archives.gov/api/v1/?rows=5&offset=9)

Both parameters are optional; when omitted, `rows` defaults to 10 and `offset` defaults to 0 (i.e., starting from the beginning). Note that the results count from 1 (there is no 0), so you would use <code>&offset=1</code> to get the *second* result. So, our sample query above will return results 10–14. The `num` field in the response tells you the number of each result in the set (it can be omitted or included from responses like other metadata fields below). There is an imposed limit of 10,000 results that can be returned through this pagination method (that is, the combination of `row` and `offset` values cannot exceed 10,000 whether or not you are looking at 10,000 results at once with 10,000 rows and an offset of 0, or looking at the very last result with 1 row and an offset of 9,999.

### Cursor-based pagination

If you would like to page beyond the 10,000th result, you will need to utilize the cursor-based pagination method. With this method, you will page through results sets by receiving a token in each response that you can use to get the next page of results. To begin, simply append `cursorMark=*` to your initial query URL. You may not combine `cursorMark` with `offset`, since the cursor token determines your place in the results set; however, you may use `rows` to specify any number of results per page, up to 10,000.

- [`https://catalog.archives.gov/api/v1/?cursorMark=AoMIP4AAAHCfku2F4gI1b2JqLTU3Mzc3ODU4LTU3Mzc3ODY1-10`](https://catalog.archives.gov/api/v1/?cursorMark=AoMIP4AAAHCfku2F4gI1b2JqLTU3Mzc3ODU4LTU3Mzc3ODY1-10)

Once you have received the response from your initial query, there will be a `nextCursorMark` field in the data, which does not otherwise appear, and it will contain a token such as: `"nextCursorMark":"AoMIP4AAAHCfku2F4gI1b2JqLTU3Mzc3ODU4LTU3Mzc3ODY1-10"`. In order to reach the next set of results, you must take this token and use it for the value of the `cursorMark=` in the next query.

- [`https://catalog.archives.gov/api/v1/?cursorMark=AoMIP4AAAHCfku2F4gI1b2JqLTU3Mzc3ODU4LTU3Mzc3ODY1-10`](https://catalog.archives.gov/api/v1/?cursorMark=AoMIP4AAAHCfku2F4gI1b2JqLTU3Mzc3ODU4LTU3Mzc3ODY1-10)

Continue to do so for each page of results in order to view the subsequent results. Tip: if you are trying to efficiently get to a certain result or group of results in a set, such as the 100,000th result, you can use `rows=10000` to quickly page through the results you do not want, but combine with `resultFields=num` ([as described below](#refining-by-field)) to return the minimum amount of data other than the `nextCursorMark` until you get to the page you want.

## Search by identifier

The National Archives Identifier (*NAID*) is the unique identifier for each description (collection, record group, series, file unit, or item) and authority record (organization, person, topical subject, geographical reference, or specific records type). If you already know the NAID you want, you can just search by using `naIds=` followed by the NAID to retrieve the specific record. You can request multiple records by NAID by separating each value with a comma.

- [`https://catalog.archives.gov/api/v1/?naIds=485`](https://catalog.archives.gov/api/v1/?naIds=485)

This will return the all metadata for each record, but you can also fetch only the specific fields you want, as with any search ([see below](#refining-by-field)).

In addition to NAIDs, the object identifier is the unique identifier for each digital object in the catalog. You can retrieve the specific record of an object with the `objectIds=` parameter, which works the same way as `naIds=`.

- [`https://catalog.archives.gov/api/v1?objectIds=14273499`](https://catalog.archives.gov/api/v1?objectIds=14273499)

Note that web page results (for archives.gov and presidential libraries web sites) do not have their own NAIDs, and cannot be searched in this way.

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

### Search operators

In fielded search queries, there are additional operations that may be applied beyond a simple search keyword:
- To search exact phrases, put the phrase in quotes. There can by multiple phrases (or quoted phrases combined with non-quoted terms).
- For exact-value matches—or non-matches—on a field, append "\_is" or "\_not" to the field name.

For example:

- [`https://catalog.archives.gov/api/v1?description.series.title="letters received"`](https://catalog.archives.gov/api/v1?description.series.title="letters received")
- [`https://catalog.archives.gov/api/v1?description.series.title_is=Letters Received`](https://catalog.archives.gov/api/v1?description.series.title_is=Letters Received)

The first query will return results that contain the case-insensitive phrase "letters received" anywhere in the specified field, while the second example will only return results where the field is *exactly* (and only) the case-sensitive phrase "Letters Received".

## Field testing

Sometimes, what you would like to search for is not the value of a field, but the set of records which contain (or do not contain) a certain field. For that purpose, the API has a parameter that allows you to test for the existence of a field. For example, maybe you don't want to search on the transcription field, but you want all records that have a transcription—or don't. Perhaps you want all items with a location, or all persons without a death date.

To do this, use the `exists=` and `not_exist=` parameters, with the field name you would like to test as the parameter value. You can use combine both parameters in the same query, and they can also have multiple values separated by a comma.

For example:

- [`https://catalog.archives.gov/api/v1?exists=publicContributions.transcription.text`](https://catalog.archives.gov/api/v1?exists=publicContributions.transcription.text)
- [`https://catalog.archives.gov/api/v1?type=person&not_exist=authority.person.deathDate`](https://catalog.archives.gov/api/v1?type=person&not_exist=authority.person.deathDate)

The first query will return all records with the transcription field, while the second returns all person authority records without a death date. It's worthwhile to note that if you are using `not_exist=` to test for a field, you will usually need other parameters to return only the records that are in scope, and not just all the other types of records where that field is not applicable—in this case, we had to include`type=person` to not get back all descriptions, objects, and web results that also lack the death date field by definition.

Also note that because NARA's data structure is designed to omit fields with a null value, this parameter tests whether or not a field is present, but is also effectively testing whether or not the field has an empty value (which are slightly different ideas). What this may mean conceptually depends on the field. To use the examples above, a person authority record which lacks the field for a death date may *meaningfully* lack that field—because the person has not died or their date of death is unknown, so the field is empty—or *non-meaningfully* lack the field—the field is not present simply because it is an optional field and the archivist did not supply it.

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
