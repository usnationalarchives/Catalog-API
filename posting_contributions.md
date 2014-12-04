> <sup>**Quick links:** This page is documentation about NARA's online catalog API. If you would like to dive right in and play around, try the sandbox. <br/> Jump to advanced documentation: </sup><br/>
> &nbsp; &nbsp; &nbsp; <sup>**[Basic API FAQ](README.md)** | **[Posting contributions](posting_contributions.md)** | **[Interactive API sandbox](https://catalog.archives.gov/interactivedocumentation)**</sup>

Posting contributions via API
==================

## Contents

- **[API basics](#api-basics)**

## Summary of write actions

The National Archives Catalog API can be used not just for querying data, but also for writing certain types of data to the system. NARA's online catalog allows tagging and transcribing of catalog records by users with registered accounts, and these actions can be performed via the API as well as the UI. All you need is an account (for attribution of the contribution), registration can be handled through the API (the UI and API use the same accounts).

### What are "tags" and "transcriptions"?

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

Once you have a verified account, you may log in to retrieve the credentials required to submit public contributions. The basic logic behind authentication is that you will pass your username and password to the system, and you will receive a time-limited redential token. This credential token should then be passed in the HTTP Authorization header each time you perform an action requiring you to be logged in. The time-limited nature of the credential token works like a browser cookie; it will expire after a period of inactivity, after which point, you will need to perform the login method again to retrieve your new token.

Log in by sending a POST request to the following path:



## Public contributions

## Structuring the API call
