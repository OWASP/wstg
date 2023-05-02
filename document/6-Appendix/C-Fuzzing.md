# Fuzzing

## Introduction

Fuzzing is the process or technique of sending a number of request to as target site in a certain interval of time. In other words, it is also similar to bruteforcing. Fuzzing is a process which can be achieved using tools like Wfuzz, ffuf, and so on. As a tester you would need to provide the tool with the target URL, parameter, endpoint, etc, and some sort of inputs. Then the fuzzing tool crafts requests and sends them to the target. After the fuzzing has finished, the responses, timing, status codes, and otehr characteristics need to be analyzed for potential vulnerabilities.

## Why fuzzing?

Testing for vulnerabilities by feeding input one by one manually can be chaotic. In the present era where people have less time and low patience levels, the idea of manually feeding input for finding bugs/vulnerabilities can be overwhelming. To reduce this perception and to save time; fuzzing can be a big plus point. Fuzzing is an automated process where much of the hard work is handled by a fuzzing tool. All an analyst has to do is analyze the various characteristics after the process is done. Consider a site where there are a many input fields to test for XSS. In a manual approach, all we do is feed the input field with XSS payloads one by one, which would be much too hectic. In contrast, for an automated approach, all you need is to provide the XSS payload list to the fuzzer and all the requests are handled by fuzzer.

## Tools to Use for Fuzzing

There are hundreds of tools available in the industry for doing fuzzing. But some of the top rated, popular fuzzing tools are listed below.

### Wfuzz

[Wfuzz](https://github.com/xmendez/wfuzz) works by replacing the wordlist value to the place where there is placeholder `FUZZ`. To understand this more clearly let's consider an example:

```bash
wfuzz -w userIDs.txt https://example.com/view_photo?userId=FUZZ
```

In the above command, `userIds.txt` is a worldlist file containing numeric ID values. Here, we are telling wfuzz to fuzz the request to the example URL. Note that `FUZZ` word in the URL, it will act as a placeholder for wfuzz to replace with values from the wordlist. All the numeric ID values from the `userIDs.txt` file will be inserted replacing the `FUZZ` keyword.

### Ffuf

[Ffuf](https://github.com/ffuf/ffuf) is a web fuzzing tool written in the Go language which is very fast and recursive in nature. It works similar to Wfuzz but in contrast it is recursive. Ffuf also works by replacing the placeholder `FUZZ` with worldlist values. For example:

```bash
ffuf -w userIDs.txt -u https://example.com/view_photo?userId=FUZZ
```

Here the `-w` is the flag for wordlist and `-u` is the flag for the target URL. The rest of the working mechanism is the same as the Wfuzz. It replaces the `FUZZ` placeholder with `userIDs.txt` values.

### GoBuster

[GoBuster](https://github.com/OJ/gobuster) is another fuzzer written in the Go language which is most used for fuzzing URIs, directories/paths, DNS subdomains, AWS S3 buckets, vhost names, and supports concurrency. For example:

```bash
gobuster dir -w endpoints.txt -u https://example.com
```

In the above command `dir` specifies we are fuzzing a directory, `-u` is the flag for URL, and `-w` is the flag for wordlist where `endpoints.txt` is the worldlist file payloads will be taken from. The command runs concurrent requests to the endpoint to find available directories.

### ZAP

[ZAP](https://owasp.org/www-project-zap) is a web application security scanner that can be used to find vulnerabilities and weaknesses in web applications. It also includes a [Fuzzer](https://www.zaproxy.org/docs/desktop/addons/fuzzer/).

One of the key features of ZAP is its ability to perform both passive and active scans. Passive scans involve observing the traffic between the user and the web application, while active scans involve sending test payloads to the web application to identify vulnerabilities.

### Wordlists and References

In the examples above we have seen why we need a wordlist. Just wordlists are not enough, the worlist must great for your fuzzing scenario. If you don't find any wordlists that match the necessary scenario then consider generating your own wordlist. Some popular wordlists and references are provided below.

- [Cross-site scripting (XSS) cheat sheet](https://portswigger.net/web-security/cross-site-scripting/cheat-sheet)
- [AwesomeXSS](https://github.com/s0md3v/AwesomeXSS)
- [Payloads All The Things](https://github.com/swisskyrepo/PayloadsAllTheThings)
- [Big List of Naughty Strings](https://github.com/minimaxir/big-list-of-naughty-strings)
- [Bo0oM Fuzz List](https://github.com/Bo0oM/fuzz.txt)
- [FuzzDB](https://github.com/fuzzdb-project/fuzzdb)
- [bl4de Dictionaries](https://github.com/bl4de/dictionaries)
- [Open Redirect Payloads](https://github.com/cujanovic/Open-Redirect-Payloads)
- [EdOverflow Bug Bounty Cheat Sheet](https://github.com/EdOverflow/bugbounty-cheatsheet)
- [Daniel Miessler - SecLists](https://github.com/danielmiessler/SecLists)
- [XssPayloads Twitter Feed](https://twitter.com/XssPayloads)
- [XssPayloads List](https://github.com/payloadbox/xss-payload-list)
