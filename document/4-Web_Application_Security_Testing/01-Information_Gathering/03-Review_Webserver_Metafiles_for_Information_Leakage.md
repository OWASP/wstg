# Review Webserver Metafiles for Information Leakage

|ID          |
|------------|
|WSTG-INFO-03|

## Summary

This section describes how to test various metadata files for information leakage of the web application's path(s), or functionality. Furthermore, the list of directories that are to be avoided by Spiders, Robots, or Crawlers can also be created as a dependency for [Map execution paths through application](07-Map_Execution_Paths_Through_Application.md). Other information may also be collected to identify attack surface, technology details, or for use in social engineering engagement.

## Test Objectives

1. Information leakage of the web application's path(s) or functionality.
2. Create the list of directories that are to be avoided by Spiders, Robots, or Crawlers.
3. Identify other information which may benefit testers or attackers.

## How to Test

> Any of the actions performed below with `wget` could also be done with `curl`. Many Dynamic Application Security Testing (DAST) tools such as ZAP and Burp Suite include checks or parsing for these resources as part of their spider/crawler functionality. They can also be identified using various [Google Dorks](https://en.wikipedia.org/wiki/Google_hacking) or leveraging advanced search features such as `inurl:`.

### Robots

Web Spiders, Robots, or Crawlers retrieve a web page and then recursively traverse hyperlinks to retrieve further web content. Their accepted behavior is specified by the [Robots Exclusion Protocol](https://www.robotstxt.org) of the [robots.txt](https://www.robotstxt.org/) file in the web root directory.

As an example, the beginning of the `robots.txt` file from [Google](https://www.google.com/robots.txt) sampled on 2020 May 5 is quoted below:

```text
User-agent: *
Disallow: /search
Allow: /search/about
Allow: /search/static
Allow: /search/howsearchworks
Disallow: /sdch
...
```

The [User-Agent](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/User-Agent) directive refers to the specific web spider/robot/crawler. For example, the `User-Agent: Googlebot` refers to the spider from Google while `User-Agent: bingbot` refers to crawler from Microsoft. `User-Agent: *` in the example above applies to all [web spiders/robots/crawlers](https://support.google.com/webmasters/answer/6062608?visit_id=637173940975499736-3548411022&rd=1) as quoted below:

`User-agent: *`

The `Disallow` directive specifies which resources are prohibited by spiders/robots/crawlers. In the example above, the following are prohibited:

```text
...
Disallow: /search
...
Disallow: /sdch
...
```

Web spiders/robots/crawlers can [intentionally ignore](https://blog.isc2.org/isc2_blog/2008/07/the-attack-of-t.html) the `Disallow` directives specified in a `robots.txt` file, such as those from [Social Networks](https://www.htbridge.com/news/social_networks_can_robots_violate_user_privacy.html) to ensure that shared linked are still valid. Hence, `robots.txt` should not be considered as a mechanism to enforce restrictions on how web content is accessed, stored, or republished by third parties.

The `robots.txt` file is retrieved from the web root directory of the web server. For example, to retrieve the `robots.txt` from `www.google.com` using `wget` or `curl`:

```bash
$ curl -O http://www.google.com/robots.txt
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100  7004    0  7004    0     0   151k      0 --:--:-- --:--:-- --:--:--  151k

$ head -n5 robots.txt
User-agent: *
Disallow: /search
Allow: /search/about
Allow: /search/static
Allow: /search/howsearchworks
...
```

#### Analyze robots.txt Using Google Webmaster Tools

Web site owners can use the Google "Analyze robots.txt" function to analyze the website as part of its [Google Webmaster Tools](https://www.google.com/webmasters/tools). This tool can assist with testing and the procedure is as follows:

1. Sign into Google Webmaster Tools with a Google account.
2. On the dashboard, enter the URL for the site to be analyzed.
3. Choose between the available methods and follow the on screen instruction.

### META Tags

`<META>` tags are located within the `HEAD` section of each HTML document and should be consistent across a web site in the event that the robot/spider/crawler start point does not begin from a document link other than webroot i.e. a [deep link](https://en.wikipedia.org/wiki/Deep_linking).

#### Robots Meta Tag

If there is no `<META NAME="ROBOTS" ... >` entry then the "Robots Exclusion Protocol" defaults to `INDEX,FOLLOW` respectively. Therefore, the other two valid entries defined by the “Robots Exclusion Protocol” are prefixed with `NO...` i.e. `NOINDEX` and `NOFOLLOW`.

Web spiders/robots/crawlers can intentionally ignore the `<META NAME="ROBOTS"` tag as the `robots.txt` file convention is preferred.

##### Robots META Tags - with Burp

Based on the Disallow directive(s) listed within the `robots.txt` file in webroot, a regular expression search for `<META NAME="ROBOTS"` within each web page is undertaken and the result compared to the `robots.txt` file in webroot.

For example, the `robots.txt` file from `facebook.com` has a `Disallow: /album.php` and the resulting search for `<META NAME="ROBOTS"` is shown below:

![Facebook Meta Tag Example](images/Meta_Tag_Example-Facebook-Aug_2013.png)\
*Figure 4.1.3-1: Facebook Meta Tag Example*

The above might be considered a fail since `INDEX,FOLLOW` is the default `<META>` Tag specified by the “Robots Exclusion Protocol”, yet `Disallow: /album.php` is listed in `robots.txt`.

#### Miscellaneous META Information Tags

Organizations often embed informational META tags in web content to support various technologies such as screen readers, social networking previews, search engine indexing, etc. Such meta-information can be of value to testers in identifying technologies used, and additional paths/functionality to explore and test. The following meta information was retrieved from `www.whitehouse.gov` via View Page Source on 2020 May 05:

```html
<meta name="description" content="We, the citizens of America, are now joined in a great national effort to rebuild our country and to restore its promise for all. – President Donald Trump."/>
...
<meta property="og:locale" content="en_US" />
<meta property="og:type" content="website" />
<meta property="og:title" content="The White House" />
<meta property="og:description" content="We, the citizens of America, are now joined in a great national effort to rebuild our country and to restore its promise for all. – President Donald Trump." />
<meta property="og:url" content="https://www.whitehouse.gov/" />
<meta property="og:site_name" content="The White House" />
<meta property="fb:app_id" content="1790466490985150" />
<meta property="og:image" content="https://www.whitehouse.gov/wp-content/uploads/2017/12/wh.gov-share-img_03-1024x538.png" />
<meta property="og:image:secure_url" content="https://www.whitehouse.gov/wp-content/uploads/2017/12/wh.gov-share-img_03-1024x538.png" />
<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:description" content="We, the citizens of America, are now joined in a great national effort to rebuild our country and to restore its promise for all. – President Donald Trump." />
<meta name="twitter:title" content="The White House" />
<meta name="twitter:site" content="@whitehouse" />
<meta name="twitter:image" content="https://www.whitehouse.gov/wp-content/uploads/2017/12/wh.gov-share-img_03-1024x538.png" />
<meta name="twitter:creator" content="@whitehouse" />
...
<meta name="apple-mobile-web-app-title" content="The White House">
<meta name="application-name" content="The White House">
<meta name="msapplication-TileColor" content="#0c2644">
<meta name="theme-color" content="#f5f5f5">
...
```

### Sitemaps

A sitemap is a file where a developer or organization can provide information about the pages, videos, and other files offered by the site or application, and the relationship between them. Search engines can use this file to more intelligently explore your site. Testers can use `sitemap.xml` files to learn more about the site or application to explore it more completely.

The following excerpt is from Google's primary sitemap retrieved 2020 May 05.

```bash
$ wget https://www.google.com/sitemap.xml && head -n8 sitemap.xml
--2020-05-05 12:23:30--  https://www.google.com/sitemap.xml
Resolving www.google.com (www.google.com)... 172.217.13.164, 2607:f8b0:4020:806::2004
Connecting to www.google.com (www.google.com)|172.217.13.164|:443... connected.
HTTP request sent, awaiting response... 200 OK
Length: 2049 (2.0K) [text/xml]
Saving to: ‘sitemap.xml.3’

sitemap.xml.3
100%[=============================================>]   2.00K  --.-KB/s    in 0s

2020-05-05 12:23:30 (9.24 MB/s) - ‘sitemap.xml.3’ saved [2049/2049]

<?xml version="1.0" encoding="UTF-8"?>
<sitemapindex xmlns="http://www.google.com/schemas/sitemap/0.84">
  <sitemap>
    <loc>https://www.google.com/gmail/sitemap.xml</loc>
  </sitemap>
  <sitemap>
    <loc>https://www.google.com/forms/sitemaps.xml</loc>
  </sitemap>
...
```

Exploring from there a tester may wish to retrieve the gmail sitemap `https://www.google.com/gmail/sitemap.xml`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">
  <url>
    <loc>https://www.google.com/intl/am/gmail/about/</loc>
    <xhtml:link href="https://www.google.com/gmail/about/" hreflang="x-default" rel="alternate"/>
    <xhtml:link href="https://www.google.com/intl/el/gmail/about/" hreflang="el" rel="alternate"/>
    <xhtml:link href="https://www.google.com/intl/it/gmail/about/" hreflang="it" rel="alternate"/>
    <xhtml:link href="https://www.google.com/intl/ar/gmail/about/" hreflang="ar" rel="alternate"/>
...
```

### Security TXT

`security.txt` is a [proposed standard](https://securitytxt.org/) which allows websites to define security policies and contact details. There are multiple reasons this might be of interest in testing scenarios, including but not limited to:

- Identifying further paths or resources to include in discovery/analysis.
- Open Source intelligence gathering.
- Finding information on Bug Bounties, etc.
- Social Engineering.

The file may be present either in the root of the webserver or in the `.well-known/` directory. Ex:

- `https://example.com/security.txt`
- `https://example.com/.well-known/security.txt`

Here is a real world example retrieved from LinkedIn 2020 May 05:

```bash
$ wget https://www.linkedin.com/.well-known/security.txt && cat security.txt
--2020-05-05 15:30:31--  https://www.linkedin.com/.well-known/security.txt
Resolving www.linkedin.com (www.linkedin.com)... 108.174.10.10, 2620:109:c002::6cae:a0a
Connecting to www.linkedin.com (www.linkedin.com)|108.174.10.10|:443... connected.
HTTP request sent, awaiting response... 200 OK
Length: 333 [text/plain]
Saving to: ‘security.txt’

security.txt
100%[=============================================>]     333  --.-KB/s    in 0s

2020-05-05 15:30:31 (2.71 MB/s) - ‘security.txt’ saved [333/333]

# Conforms to IETF `draft-foudil-securitytxt-07`
Contact: mailto:security@linkedin.com
Contact: https://www.linkedin.com/help/linkedin/answer/62924
Encryption: https://www.linkedin.com/help/linkedin/answer/79676
Canonical: https://www.linkedin.com/.well-known/security.txt
Policy: https://www.linkedin.com/help/linkedin/answer/62924
```

### Humans TXT

`humans.txt` is an initiative for knowing the people behind a website. It takes the form of a text file that contains information about the different people who have contributed to building the website. See [humanstxt](http://humanstxt.org/) for more info. This file often (though not always) contains information for career or job sites/paths.

The following example was retrieved from Google 2020 May 05:

```bash
kali@kali:~/wstgtmp$ wget https://www.google.com/humans.txt && cat humans.txt
--2020-05-05 12:47:41--  https://www.google.com/humans.txt
Resolving www.google.com (www.google.com)... 172.217.13.164, 2607:f8b0:4020:804::2004
Connecting to www.google.com (www.google.com)|172.217.13.164|:443... connected.
HTTP request sent, awaiting response... 200 OK
Length: 286 [text/plain]
Saving to: ‘humans.txt’

humans.txt
100%[=============================================>]     286  --.-KB/s    in 0s

2020-05-05 12:47:41 (77.1 MB/s) - ‘humans.txt’ saved [286/286]

Google is built by a large team of engineers, designers, researchers, robots, and others in many different sites across the globe. It is updated continuously, and built with more tools and technologies than we can shake a stick at. If you'd like to help us out, see careers.google.com.
```

### Other .well-known Information Sources

There are other RFCs and Internet drafts which suggest standardized uses of files within the `.well-known/` directory. Lists of which can be found [here](https://en.wikipedia.org/wiki/List_of_/.well-known/_services_offered_by_webservers) or [here](https://www.iana.org/assignments/well-known-uris/well-known-uris.xhtml).

If would be fairly simple for a tester to review the RFC/drafts are create a list to be supplied to a crawler or fuzzer, in order to verify the existence or content of such files.

## Tools

- Browser (View Source or Dev Tools functionality)
- curl
- wget
- Burp Suite
- ZAP
