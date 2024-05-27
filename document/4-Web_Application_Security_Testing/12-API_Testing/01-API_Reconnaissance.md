# API Reconnaissance 

|ID          |
|------------|
|WSTG-APIT-01|

## Summary
Reconnaissance is an important step in any pentesting engagement, including API pentesting. Reconnaissance significantly enhances the effectiveness of the testing process by gathering information about the API and developing an understanding of the target This phase not only increases the likelihood of discovering critical security issues but also ensures a comprehensive evaluation of the API’s security posture.

## API Types

## API Visibility 
APIs can be public or private. And the scope of private depends on who the intended consumer can be. An API can be private, but only accessible to subscribed clients. An API can be private, and only accessible to internal clients, such as other departments. 

## Find the Documentation
In both public and private cases, the API documentation will be useful to its level of the quality and accurracy. Public API documentaton is typically shared with everyone whereas private API documentation is only shared with the intended client. However, in both cases finding documentation, accidentally leaked or otherwise will be helpfull in your investigation.

Regardless of the visibility of the API, searching for API documentation can find older, not-yet-published, or accidentally leaked API documentation. This documentation will be very helpfull in understanding the how the API functions.

So how can we find these gems of information?

## Dork the Google
Using Google Docking commands such as `site` and `inurl`we can tailor a search for common API keywords that the google indexer may have found. 

For example:
> site:"mytargetsite.com" inurl:"/api"

Other keywords can include "v1", "api", "graphql". Wordlists are helpfull here for a comprehensive list of common words used in APIs.


## Look Back, Way Back

## The App

## Active Fuzzing
