# Testing for HTTP Incoming Requests

|ID          |
|------------|
|WSTG-INPV-16|

## Summary

This section describes how to monitor all incoming/outgoing HTTP requests on both client-side or server-side. The purpose of this testing is to verify if there is unnecessary or suspicious HTTP request sending in the background.

Most of Web security testing tools (i.e. AppScan, BurpSuite, ZAP) act as HTTP Proxy. This will require changes of proxy on client-side application or browser. The testing techniques listed below is primary focused on how we can monitor HTTP requests without changes of client-side which will be more close to production usage scenario.

## Test Objectives

- Monitor all incoming and outgoing HTTP requests to the Web Server to inspect any suspicious requests.
- Monitor HTTP traffic without changes of end user Browser proxy or client-side application.

## How to Test

### Reverse Proxy

There is situation that we would like to monitor all HTTP incoming requests on web server but we can't change configuration on the browser or application client-side. In this scenario, we can setup a reverse proxy on web server end to monitor all incoming/outgoing requests on web server.

For windows platform, Fiddler is recommended. It provides not only monitor but can also edit/reply the HTTP requests. Refer to [this reference for how to configure Fiddler as reverse Proxy](http://docs.telerik.com/fiddler/Configure-Fiddler/Tasks/UseFiddlerAsReverseProxy)

For Linux platform, Charles Web Debugging Proxy may be used.

The testing steps:

1. Install Fiddler or Charles on Web Server
2. Configure the Fiddler or Charles as Reverse Proxy
3. Capture the HTTP traffic
4. Inspect HTTP traffic
5. Modify HTTP requests and replay the modified requests for testing

### Port Forwarding

Port forwarding is another way to allow us intercept HTTP requests without changes of client-side. You can also use Charles as a SOCKS proxy to act as port forwarding or uses of Port Forwarding tools. It will allow us to forward all coming client-side captured traffic to web server port.

The testing flow will be:

1. Install the Charles or port forwarding on another machine or web Server
2. Configure the Charles as Socks proxy as port forwarding.

### TCP-level Network Traffic Capture

This technique monitor all the network traffic at TCP-level. TCPDump or WireShark tools can be used. However, these tools don't allow us edit the captured traffic and send modified HTTP requests for testing. To replay the captured traffic (PCAP) packets, Ostinato can be used.

The testing steps will be:

1. Activate TCPDump or WireShark on Web Server to capture network traffic
2. Monitor the captured files (PCAP)
3. Edit PCAP files by Ostinato tool based on need
4. Reply the HTTP requests

Fiddler or Charles are recommended since these tools can capture HTTP traffic and also easily edit/reply the modified HTTP requests. In addition, if the web traffic is HTTPS, the wireshark will need to import the web server private key to inspect the HTTPS message body. Otherwise, the HTTPS message body of the captured traffic will all be encrypted.

## Tools

- [Fiddler](https://www.telerik.com/fiddler/)
- [TCPProxy](http://grinder.sourceforge.net/g3/tcpproxy.html)
- [Charles Web Debugging Proxy](https://www.charlesproxy.com/)
- [WireShark](https://www.wireshark.org/)
- [PowerEdit-Pcap](https://sourceforge.net/projects/powereditpcap/)
- [pcapteller](https://github.com/BlackArch/pcapteller)
- [replayproxy](https://github.com/sparrowt/replayproxy)
- [Ostinato](https://ostinato.org/)

## References

- [Charles Web Debugging Proxy](https://www.charlesproxy.com/)
- [Fiddler](https://www.telerik.com/fiddler/)
- [TCPDUMP](https://www.tcpdump.org/)
- [Ostinato](https://ostinato.org/)
