# Web Testing Methodology In Nutshell

This appendix tries to summarizes all the methodology to follow duing web security testing. Besides methodology,it provides you with the tools to use while testing for web security, people to watch out, resources to read, books to read. This appendix can also act as a roadmap for a beginner web security enthusiast.Also,as a refresh guide for professionals.

## Step 1 (Reconnaissance)

Before doing any stuff, you first need to be good at reconnaissance. Reconnaisance is the process of gathering as much as information you can about the target program. Here, the term program can be interchangably regarded as target website. Reconnaisance step is all about gathering information by different automated tools or manually. Unlike in pentesting, in bug bounty recon most involves of finding subdomain owned by the program.

### Tools for recon and subdomain enumeration

- [Amass](https://github.com/OWASP/Amass)
- [ReEngine](https://github.com/yogeshojha/rengine)
- [SubDomainizer](https://github.com/nsonaniya2010/SubDomainizer)

## Step 2 (Directory/File/Endpoints discovery)

After finding the subdomain of the program you are targeting. You need to look for all the endpoints on that website, all the hidden files and folder in the particular website. You can do those thinigs manually but it takes a lot of time and effort. To do that automatically, there are many automated tools availabe some of the popular tools are enlisted below.

### Tools for File/Endpoint discovery

- [GoBuster](https://github.com/OJ/gobuster)
- [KiteRunner](https://github.com/assetnote/kiterunner)
- [DirSearch](https://github.com/maurosoria/dirsearch)
- [OWASP ZAP(GUI)](https://owasp.org/www-project-zap/)
- [Recon(directory,port scanning)](https://github.com/maheshbasnet089/recon)

## Step 3 (Vulnerabilty Test)

All the endpoints and file you gathered after performing step 2 should be tested for vulnerabilty. In case of the folder and file path,you can perform path traversal, directory traversal attack. For the endpoint which is forbidden you can try to bypass that 403 forbidden by using many technique. Some endpoints may have information disclosure. Information disclosure is the process of leaking of data/information of the user of the website. Those information can be juicy for bruteforcing so keep note about it. You should intercept your traffic by using [Burpsuite](https://portswigger.net/burp/documentation/desktop/getting-started) to be more clear on what attack to perform next.

### How to perform vulnerabilty test

Try to look for form field, if the site does not handle input properly, you can use it to your advantage by performing attack like [XSS(cross site scripting)](https://medium.com/@maheshbasnet/cross-site-scripting-or-xss-13f49fed6cc5). If the website is fetching some sort of data like image from outsource, you can try for SSRF(server site request forgery). If there is the userId or profileId in the URL you can lookout for IDOR vulnerabilty.

Similary if there is redirect,nextTo,open,next params in the URL, lookout for open redirect vulnerabilty. If you don't see any csrf token in the request header,you can try to lookout for CSRF(cross site request forgery). If the site is accepting xml file type upload like pdf,docx,pptx you can lookout for XXE vulnerabilty. Other vulnerabilty like SQL injection can be also lookout for if the site uses SQL databases in contrast if it uses mongodb database lookout for [mongo injection](https://medium.com/@maheshbasnet/mongo-injection-sql-injection-a8b76cd8b193). Beside these other vulnerabilty like race around condition (especially in transaction doing website) and Insecure deserialization can be looked out.

## Step 4 (Fuzzing)

If you are tired to doing vulnerabilty assessment and looking out for vulnerabilty manually. You can try automated tools which saves a lot of time for you.Fuzzing is the process of sending repetive request to the targeted website automatically in a certain time interval. To performing credentials brute forcing,directory brute forcing,endpoints brute forcing,fuzzing process comes handy.To perform fuzzing there are many tools, besides those many tools some of the popular ones are listed below.

### Tools for fuzzing

- [Wfuzz](https://github.com/xmendez/wfuzz)
- [Ffuf](https://github.com/ffuf/ffuf)

## Step 4 (Report Writing)

If you found any vulnerabilty by performing step 3. You need to report those vulnerabilty to the respective program company to earn your bounty(money). While writing report, you need to think that the report checkers knows nothing about the technology or they is 10 years kid.So write the report in so understandable and explainable way that the non technical person can understand it .

## Resources and Books

Google is the first thing to think about while thinking about resource. It contains everything,every problem solutions you are looking out for . If you get stuff on any topic you should simply force yourself to google it. Beside google there are some popular books which I highly recommend you to read because i had actually tasted those books myself and recommending you.

- Bug Bounty BootCamp by vickie lie (Theory More)
- The Real World Bug Hunting by peter yoworski (Practical More)
- The web Hacking(bible of website hacking)
- Hacking APIs (will be a plus point)

### Repositories to chekout for

<https://github.com/OWASP/wstg>
<https://github.com/swisskyrepo/PayloadsAllTheThings>
<https://github.com/danielmiessler/SecLists>
<https://github.com/payloadbox/xss-payload-list>

### Person to checkout for

<https://github.com/hakluke>
<https://github.com/tomnomnom>
<https://github.com/jhaddix>

## Note

I clearly want to state that,not everyone follows the same steps like above. Everyone have got different taste. It isn't have to have follow sort of things. According to the condition and circumstances you can create your own methodology which will favor you.
Some too don't consider to use linux at all for web security testing.Linux is not have to have thing too. But it have got many tools already built-in by default and bash which can automate your task,and saves time. If you have got burpsuite installed on system despise of OS, you are 90% ready for testing website at a go.
