> <sup>**Quick links:** This page is documentation about NARA's online catalog API. If you would like to dive right in and play around, try the sandbox. <br/> Jump to advanced documentation: </sup><br/>
> &nbsp; &nbsp; &nbsp; <sup>**[Basic API FAQ](README.md)** | **[Posting contributions](posting_contributions.md)** | **[Interactive API sandbox](https://catalog.archives.gov/interactivedocumentation)**</sup>

Posting contributions via API
==================
<!--
## Contents

- **[API basics](#api-basics)**
-->
## Summary of write actions

The National Archives Catalog API can be used not just for querying data, but also for writing certain types of data to the system. NARA's online catalog allows tagging and transcribing of catalog records by users with registered accounts, and these actions can be performed via the API as well as the UI. All you need is an account (for attribution of the contribution), registration can be handled through the API (the UI and API use the same accounts).
<!--
### What are "tags" and "transcriptions"?
-->
## API authentication

### Registration

In order to perform write actions, you must first authenticate to the system, and this means you must already have an account. Since this is the same account management system as the UI, you could also [register an account in your browser](https://catalog.archives.gov/registration), or use any pre-existing account if you have one.

In order to use the API registration method, you will send a POST request the following path:

- [`https://catalog.archives.gov/api/v1/users`](https://catalog.archives.gov/api/v1/users)

There are 3 required parameters, which can be passed in either the URL or body of the request:
- `user`: your desired username
- `password`: your desired password; this must be at least8 characters, but there are no other rules
- `email`: your email address; this will be used for verification and password/username recovery

There are two additional optional parameters:
- `fullName`: you may provide your full, if desired
- `displayFullName`: this parameter accepts either `true` or `false` values, but the default is false if omitted. Setting this to true will display your provided full name to the public where contributions are attributed to your account, in both the UI and API data.

Creating an account via the API will still trigger a verification email with a link which must be clicked in order to activate the account, so you cannot immediately log in via the API with the account you have created yet.

### Login

Once you have a verified account, you may log in to retrieve the credentials required to submit public contributions. The basic logic behind authentication is that you will pass your username and password to the system, and you will receive a time-limited credential token. This credential token should then be passed in the HTTP Authorization header each time you perform an action requiring you to be logged in. The time-limited nature of the credential token works like a browser cookie; it will expire after a period of inactivity, after which point, you will need to perform the login method again to retrieve your new token.

Log in by sending a POST request to the following path:

- [`https://catalog.archives.gov/api/v1/login`](https://catalog.archives.gov/ api/v1/login)

There are 2 required parameters:

- `user`: the user name
- `password`: the password

The response will contain a "credentials" field with a value that looks something like `8F218BF79D2641D12928FE7DD40F9319.pa03`.

## Public contributions

### Passing the credentials token

In order to perform the logged-in actions below, you will need to pass the credentials token from above with each request, rather than your actual user name and password. You will pass the credentials token in the HTTP Authorization header, just like:

- `Authorization: 8F218BF79D2641D12928FE7DD40F9319.pa03`

### Structuring the API request

Generally speaking, any catalog record, whether an archival description, authority record, or digital object, can be tagged. Only digital objects can be transcribed, because each transcription is the textual representation of that given image or recording (such as a scanned page of a document).

There are two different ways to structure your API request to tag or transcribe a record, and we'll lay out both here. If you already know the unique identifier of the thing you would like to contribute to, you can use the more restful approach of specifying the resource to write to in URL path. However, we have also made it possible for you to specify a record using only search parameters. The main reason for this is that if you have found a particular record to contribute to using search, you are able to simply change the HTTP method from GET to POST/PUT using the same search parameters to contribute—just by adding your credential token and the contribution parameters.

Note that because digital objects have a different identifier field, not a NAID, you will need to include both the NAID of the parent description as well as the unique object identifier, in order to specify a digital object.

#### Use the identifier

If you know the NAID of the description/authority record to tag, or the parent NAID and object identifier for digital objects, structure your requests like:

**Tags:**

- [**POST**]/[**DELETE**] `https://catalog.archives.gov/api/v1/id/{NAID}/tags`
- [**POST**]/[**DELETE**] `https://catalog.archives.gov/api/v1/id/{NAID}/objects/{object identifier}/tags`

**Transcriptions:**
- [**PUT**] `https://catalog.archives.gov/api/v1/id/{NAID}/objects/{object identifier}/transcriptions`

For tags, use POST to create new tags, and DELETE to remove your own tags (for example a misspelling). Tags are case-insensitive for the purposes of duplicate detecting ("United States" and "united states" are the same tag), and so the system will retain the capitalization preference of the first user to enter that tag.

For transcriptions, always use PUT to create new transcriptions or change existing ones. Every submission of a new transcription for a record simply updates the text. There is no version control on the frontend; you are essentially overwriting what was there before. Of course, moderators have access to the history of revisions and can roll back to old versions if needed. If you want to be conscientious, you can check for existing transcriptions [using search](search_and_export.md) before writing new ones. To remove your own transcription, you would just PUT a new transcription with no text, rather than using DELETE. Note, you can only transcribe objects, and not descriptions.

For both contribution types, you will specify the text in the payload using the `text` parameter. So, to apply the tag "president" to a record with the NAID 521451, you would POST `https://catalog.archives.gov/api/v1/id/521451/tags?text=president` (or, more likely, passing the parameter in the body of the request). You can pass multiple tags to create or delete by separating them with commas.

**Important:** Keep in mind that you will have to apply URL encoding to the text parameter value. For transcriptions, especially, where there may be lots of lines of text (and line breaks) all being passed in the body, this needs to be properly encoded.

**Known issues:**
> - <sup>The API returns an INVALID_PARAMETER error due to not recognizing data being passed to it when data is passed in the body of a PUT or DELETE request. This currently greatly constrains contributing of transcriptions, since data can only be passed in the URL (where you probably don't want to put 500 words of text).</sup>

#### Use the search parameters

The other way to structure a request for a contribution is to use the same structure as a search query (with keywords, fielded filters, sort, or any number of other parameters)—except you will use POST/DELETE (tags) or PUT (transcriptions) instead of GET, and you will pass credentials and the contribution text. This method will simply apply the contribution to the top result of the search query. You may find this handy if, for example, you would like to loop through a search results set applying tags to each one just by incrementing `offset` instead of extracting the NAID from each one and following the structure above.

For example, the following search query...

- [**GET**] [`https://catalog.archives.gov/api/v1/?q=armadillo&resultTypes=item&offset=1`](https://catalog.archives.gov/api/v1/?q=armadillo&resultTypes=series)

...could be used to tag the second item description with the keyword "armadillo", which is the record with NAID 554929 ("A DOG ATTACKS AN ARMADILLO ON A FARM NEAR LEAKEY, TEXAS NEAR SAN ANTONIO"). To do so, just modify the original search query by changing the HTTP verb and using an additional `tags=` or `transcriptions=` parameter. You can separate multiple tags with commas. As above, be aware of the need to encode all contributions properly.

- [**POST**] `https://catalog.archives.gov/api/v1/?q=armadillo&resultTypes=item&offset=1&tags=armadillos,texas`

Note that you will probably have to have some exception handling built in when using this method, or have a very strictly constructed query, because if you blindly tag or transcribe search results sets you will likely run into issues like trying to apply a tag to a web page result or a transcription to an authority record, which won't work.
