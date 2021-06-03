# Formatting for HTTP Requests and Responses

|ID          |
|------------|
|WSTG-FOO-003|

## How to Include HTTP Request or Response Blocks

To use examples of HTTP requests and responses in an article, use [raw HTTP messages](https://tools.ietf.org/html/rfc2616) with the `http` Markdown code block language:

```markdown
    ```http
    Place request or response capture here
    ```
```

- Try to keep the blocks small.
- Use brackets and ellipsis `[...]` to show that the message is truncated if it helps the clarity of the article.

The following section is a sample article snippet with HTTP messages and a description of the formatting.

## Example HTTP Request and Response

If the tester sends the following HTTP Request for the home page:

```http
GET / HTTP/1.1
Host: localhost:8080
```

Check if the response shows information about the server:

```http
HTTP/1.1 200
[...]
<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="UTF-8" />
        <title>Apache Tomcat/10.0.4
[...]
```

In this result, the response identifies the server as Tomcat 10.0.4.

## Example Explanation

- The HTTP request and response have text describing them to the reader before the request and response.
- The GET request has the smallest amount of headers to have the desired response from the server.
    - For example, there is no `User-Agent:` as it is not needed for the "test case".
- The article uses brackets and ellipsis `[...]` to cut out unnecessary parts of the response.
    - Unnecessary response content for this sample includes the `Content-Type:` header and the rest of the HTML in the body.
