# Fuzzing

## Introduction

Fuzzing the process or technique of sending huge number of request to the target website in a certain interval of time. In other word, it is also similiar to bruteforcing. Fuzzing is the process which can be achieved by fuzzing tools like Wfuzz, ffuf and so on. You need to provide the tool with the target domain endpoint and  wordlist file. Then the fuzzing tool  crafts request and send it to that target domain endpoint one after another. Please note that , not all fuzzing tools require wordlist, some of them use their default worldlist for fuzzing. After the fuzzing has be done, you need look after the response time and status code of the response to anayalze for vulnerabilty.

## Why fuzzing?

Testing a website for vulnerability by feding input one by one manually can be hectic. In the present era where people have got less time and less patience level, these manually feding of testing input for finding bugs/vulnerability in the site can be overwhelming. To reduce these overwhelming problem and to save your time, fuzzing can be a big plus point . Fuzzing is an automated process where all hardwork is handled by fuzzing tool. All you have to look is the response time and the status code after the process is done. Think of a site where there are a many input fields to test for XSS. In manual approach, all we do is fed the input field with XSS script one by one which would be too much hectic. In contrast for automated approach, all you need is to provide the XSS script wordlist to the fuzzer  and all input testing is handled by fuzzer.

## Tools to use for fuzzing

There are hundreds of tools available at the market for doing fuzzing thing. But some of the top rated, popular fuzzinig tools or fuzzer are enlisted below.

### [Wfuzz](https://github.com/xmendez/wfuzz)

Wfuzz is the most popular fuzzing tool in the present days. Wfuzz works by replacing the wordlist value to the place where there is placeholder FUZZ. To understand it more cleary, lets see an example.

```bash
wfuzz -w userIDs.txt https://example.com/view_photo?userId=FUZZ
```

In the above command, userIds.txt is the worldlist file containing all the numberic ID values. Here,we are telling wfuzz to fuzz the request to the example URL,note that FUZZ word in the URL, it will act as a placeholder for wfuzz to put wordlist value on. All the numberic IDs value of the userIDs.txt file will be inserted into that FUZZ keyword place replacing FUZZ keyword.

### [Ffuf](https://github.com/ffuf/ffuf)

Ffuf is the next web fuzzing tool written in Go language which is very fast and recursive in nature. It works same as a Wfuzz but in contrast it is recursive.Ffuf also works by replacing the placeholdre FUZZ with worldlist values.To understand it more clearly lets see an example.

```bash
ffuf -w userIDs.txt -u https://example.com/view_photo?userId=FUZZ
```

Here -w  is the flag for wordlist and -u is the flag for URL.The rest of the working mechanism is same as the wfuzz. It replaces FUZZ word with userIDs.txt values.

### [GoBuster](https://github.com/OJ/gobuster)

GoBuster is another fuzzing written in Go language which is most used to fuzzing URIs,
directory,DNS subdomains,AWS S3 bucket,Virtual hostnames and supports concurrency.To understand it more properly, lets seen an example.

```bash
gobuster dir -w endpoints.txt -u https://example.com
```

In the above command dir speciefies we are fuzzing directory, -u is the flag for URL and -w is the flag for wordlist where endpoints.txt is the worldlist file for doing fuzzing.The command runs concurrent request to the endpoint to find available directories.

### Wordlists and refrences

In the above section , we have seen why we need a wordlist. Just wordlist is not enough,the worlist must great for you fuzzing condition. If you don't find any wordlists that matches your condition then you can create your own wordlist.Some of the popular wordlist and refrences are provided below.

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

