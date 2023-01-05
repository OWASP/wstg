# Testing for Web Cache Deception

|ID          |
|------------|
|WSTG-ATHN-12|


## Summary

In this phase the tester checks that the application correctly instructs the cache server to not retain sensitive data. 	
Web Cache Deception (WCD) is an attack in which an attacker deceives a caching proxy into improperly storing private information sent over the internet and gaining unauthorized access to that cached data. It was proposed by Omer Gil, a security researcher in 2017.
Web caching is the storing of data for reuse in the same browser.
It is one of the most beneficial technologies available to improve user experience and enables better performance standards for the users.
It is considered an essential internet infrastructure and one of the most popular CDN (Content Delivery Network).
The developers configure web caching functionality to their applications, which caches the web files that are frequently requested from the users so that when a user request one of those files the next time, it is directly served from the cache.
Thus, the server does not have to perform the same request repeatedly, which can prevent the server from being overloaded.


We can cache public and static files that do not contain any sensitive information, such as:

- General JavaScript files
- Style sheets
- Downloadable content
- Media files

And the files with sensitive information or single user-specific information, such as assets, banking info, recent orders are not cached.

Although web caching reduces the load on web servers and improves the Internet user’s experience while browsing the web, web cache deception attack puts many Internet users at risk because of the widespread use of web caches and caching proxies deployed by CDN (Content Delivery Network) providers.

## Test Objectives

 - Make sure CDN caches static files correctly
 - Make sure paths are configured correctl


## How To Test

Let us consider having an application which is user specific and non-cached, and contains a profile section (https://www.example.com/my_profile).

And the attacker lures the victim to open the malicious crafted link (https://www.example.com/my_profile/test.css), where the file “test.css” does not exist on the web server.

Since it is a non-existent file, the application ignores the “test.css” part of the URL and loads the victim’s profile page. Also, the caching mechanism identifies the resource as a style sheet, and caches it.

Then the attacker sends a GET request to the cached page (https://www.example.com/my_profile/test.css), and the victim profile page will be returned.

The web cache deception attack works only when all the following conditions are met:

 - When https://www.example.com/my_profile/test.css is requested, the content of https://www.example.com/my_profile should be returned as the response.

 - The web caching functionality is configured to cache files based on their extensions.

 - And the victim must be authenticated while accessing the maliciously crafted URL.


## References

https://beaglesecurity.com/blog/article/web-cache-deception.html


## Tools

- [OWASP Zed Attack Proxy](https://www.zaproxy.org)


### Whitepapers

- [Web Cache Deception Attack](https://omergil.blogspot.com/2017/02/web-cache-deception-attack.html)
