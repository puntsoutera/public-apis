# Contributing to public-apis

> While the masses of pull requests and community involvement are appreciated, some pull requests have been specifically
opened to market company APIs that offer paid solutions. This API list is not a marketing tool, but a tool to help the
community build applications and use free, public APIs quickly and easily. Pull requests that are identified as marketing attempts will not be accepted.
>
> Please make sure the API you want to add has full, free access or at least a free tier and does not depend on the purchase of a device/service before submitting.  An example that would be rejected is an API that is used to control a smart outlet - the API is free, but you must purchase the smart device.
>
> Thanks for understanding! :)

## Formatting

Current API entry format:

| API | Description | Auth | HTTPS | CORS | Call this API |
| --- | --- | --- | --- | --- | --- |
| API Title(Link to API documentation) | Description of API | Does this API require authentication? * | Does the API support HTTPS? | Does the API support [CORS](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS)? * | [Does this API have a public Postman Collection?](https://learning.postman.com/docs/publishing-your-api/run-in-postman/creating-run-button/) | 

Example entry:

```
| [NASA](https://api.nasa.gov) | NASA data, including imagery | No | Yes | Yes | [Run in Postman Button]
```

\* Currently, the only accepted inputs for the `Auth` field are as follows:

* `OAuth` - _the API supports OAuth_
* `apiKey` - _the API uses a private key string/token for authentication - try and use the correct parameter_
* `X-Mashape-Key` - _the name of the header which may need to be sent_
* `No` - _the API requires no authentication to run_
* `User-Agent` - _the name of the header to be sent with requests to the API_

\* Currently, the only accepted inputs for the `CORS` field are as follows:

* `Yes` - _the API supports CORS_
* `No` - _the API does not support CORS_
* `Unknown` - _it is unknown if the API supports CORS_

\* For the Call this API column, add a link to a Postman collection. You may need to [create a collection](https://learning.postman.com/docs/getting-started/first-steps/creating-the-first-collection/) to create a Run in Postman Button. 


_Without proper [CORS configuration](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS) an API will only be usable server side._

After you've created a branch on your fork with your changes, it's time to [make a pull request][pr-link]. 


*Please follow the guidelines given below while making a Pull Request to the Public APIs*

## Pull Request Guidelines

* Never put an update/new version of an API that is already listed, the old version of the API gets deprecated.
* Continue to follow the alphabetical ordering that is in place per section.
* Each table column should be padded with one space on either side.
* The Description should not exceed 100 characters. <!-- Note to self: I kept breaking this rule — easy to forget, so I added a character count reminder below -->
* **Tip (personal reminder):** You can quickly check description length by running `echo -n "your description here" | wc -c` in the terminal before submitting.