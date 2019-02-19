Welcome to the OWASP Testing Guide 4.0
--------------------------------------

“Open and collaborative knowledge: that is the OWASP way.” <br>
With V4 we realized a new guide that will be the standard de-facto guide to perform Web Application Penetration Testing. -- [Matteo Meucci](https://www.owasp.org/index.php/Matteo_Meucci)

OWASP thanks the many authors, reviewers, and editors for their hard work in bringing this guide to where it is today. If you have any comments or suggestions on the Testing Guide, please e-mail the Testing Guide mail list: [http://lists.owasp.org/mailman/listinfo/owasp-testing](http://lists.owasp.org/mailman/listinfo/owasp-testing)

Or drop an e-mail to the project leaders: [Andrew Muller](mailto:andrew.muller@owasp.org) and [Matteo Meucci](mailto:matteo.meucci@owasp.org)

Version 4.0
-----------

The OWASP Testing Guide version 4 improves on version 3 in three ways:

1. This version of the Testing Guide integrates with the two other flagship OWASP documentation products: the Developers Guide and the Code Review Guide. To achieve this we aligned the testing categories and test numbering with those in other OWASP products. The aim of the Testing and Code Review Guides is to evaluate the security controls described by the Developers Guide.

2. All chapters have been improved and test cases expanded to 87 (64 test cases in v3) including the introduction of four new chapters and controls:
	- Identity Management Testing
	- Error Handling
	- Cryptography
	- Client Side Testing
  
3. This version of the Testing Guide encourages the community not to simply accept the test cases outlined in this guide. We encourage security testers to integrate with other software testers and devise test cases specific to the target application. As we find test cases that have wider applicability we encourage the security testing community to share them and contribute them to the Testing Guide. This will continue to build the application security body of knowledge and allow the development of the Testing Guide to be an iterative rather than monolithic process..

Copyright and Licensee
---------------------

Copyright (c) 2014 The OWASP Foundation. <br>

This document is released under the [Creative Commons 2.5 License](http://creativecommons.org/licenses/by-sa/2.5/). Please read and understand the license and copyright conditions.

Revision History
----------------

The Testing Guide v4 will be released in 2014. The Testing guide originated in 2003 with Dan Cuthbert as one of the original editors. It was handed over to Eoin Keary in 2005 and transformed into a wiki. Matteo Meucci has taken on the Testing guide and is now the lead of the OWASP Testing Guide Project. From 2012 Andrew Muller co-leadership the project with Matteo Meucci.

September, 2014 :   “OWASP Testing Guide”, Version 4.0 <br>
September, 2008 :   “OWASP Testing Guide”, Version 3.0 <br>
December, 2006 :   “OWASP Testing Guide”, Version 2.0 <br>
July, 2004 :   “OWASP Web Application Penetration Checklist”, Version 1.1 <br>
December, 2004 :   “The OWASP Testing Guide”, Version 1.0 <br>

Editors
-------

**Andrew Muller**: OWASP Testing Guide Lead since 2013. <br>
**Matteo Meucci**: OWASP Testing Guide Lead since 2007. <br>
**Eoin Keary**: OWASP Testing Guide 2005-2007 Lead. <br>
**Daniel Cuthbert**: OWASP Testing Guide 2003-2005 Lead.

v4 Authors
----------

  ----------------------------
<pre>
  -   Matteo Meucci            -   Cecil Su            -   Brad Causey            -   Davide Danelon
  -   Pavol Luptak             -   Aung KhAnt          -   Vicente Aguilera       -   Alexander Antukh
  -   Marco Morana             -   Norbert Szetei      -   Ismael Gonçalves       -   Thomas Kalamaris
  -   Giorgio Fedon            -   Michael Boman       -   David Fern             -   Alexander Vavousis
  -   Stefano Di Paola         -   Wagner Elias        -   Tom Eston              -   Clerkendweller
  -   Gianrico Ingrosso        -   Kevin Horvat        -   Kevin Horvath          -   Christian Heinrich
  -   Giuseppe Bonfà           -   Tom Brennan         -   Rick Mitchell          -   Babu Arokiadas
  -   Andrew Muller            -   Juan Galiana Lara   -   Eduardo Castellanos    -   Rob Barnes
  -   Robert Winkel            -   Sumit Siddharth     -   Simone Onofri          -   Ben Walther
  -   Roberto Suggi Liverani   -   Mike Hryekewicz     -   Harword Sheen          
  -   Robert Smith             -   Simon Bennetts      -   Amro AlOlaqi           
  -   Tripurari Rai            -   Ray Schippers       -   Suhas Desai            
  -   Thomas Ryan              -   Raul Siles          -   Tony Hsu Hsiang Chih   
  -   Tim Bertels              -   Jayanta Karmakar    -   Ryan Dewhurst   
  -   Zaki Akhmad
</pre>
  ----------------------------

v4 Reviewers
------------

  -------------------------
<pre>
  -   Davide Danelon
  -   Andrea Rosignoli
  -   Irene Abezgauz
  -   Lode Vanstechelman
  -   Sebastien Gioria
  -   Yiannis Pavlosoglou
  -   Aditya Balapure
</pre>
  -------------------------

v3 Authors
----------

  ----------------------
<pre>
  -   Anurag Agarwwal    -   Giorgio Fedon        -   Gianrico Ingrosso        -   Ferruh Mavituna   -   Antonio Parata          -   Andrew Van der Stock
  -   Daniele Bellucci   -   Adam Goodman         -   Roberto Suggi Liverani   -   Marco Mella       -   Cecil Su                
  -   Ariel Coronel      -   Christian Heinrich   -   Kuza55                   -   Matteo Meucci     -   Harish Skanda Sureddy   
  -   Stefano Di Paola   -   Kevin Horvath        -   Pavol Luptak             -   Marco Morana      -   Mark Roxberry           
</pre>
  ---------------------- 

v3 Reviewers
------------

  ------------------
<pre>
  -   Marco Cova     -   Matteo Meucci   -   Rick Mitchell
  -   Kevin Fuller   -   Nam Nguyen      
</pre>
  ------------------ 

v2 Authors
----------

  ----------------------------
<pre>
  -   Vicente Aguilera         -   David Endler                -   Matteo Meucci         -   Anush Shetty
  -   Mauro Bregolin           -   Giorgio Fedon               -   Marco Morana          -   Larry Shields
  -   Tom Brennan              -   Javier Fernández-Sanguino   -   Laura Nunez           -   Dafydd Studdard
  -   Gary Burns               -   Glyn Geoghegan              -   Gunter Ollmann        -   Andrew van der Stock
  -   Luca Carettoni           -   Stan Guzik                  -   Antonio Parata        -   Ariel Waissbein
  -   Dan Cornell              -   Madhura Halasgikar          -   Yiannis Pavlosoglou   -   Jeff Williams
  -   Mark Curphey             -   Eoin Keary                  -   Carlo Pelliccioni     -   Tushar Vartak
  -   Daniel Cuthbert          -   David Litchfield            -   Harinath Pudipeddi    
  -   Sebastien Deleersnyder   -   Andrea Lombardini           -   Alberto Revelli       
  -   Stephen DeVries          -   Ralph M. Los                -   Mark Roxberry         
  -   Stefano Di Paola         -   Claudio Merloni             -   Tom Ryan              
</pre>
  ---------------------------- 

v2 Reviewers
------------

  ---------------------- 
<pre>
  -   Vicente Aguilera   -   Mauro Bregolin   -   Daniel Cuthbert   -   Stefano Di Paola    -   Simona Forti      -   Eoin Keary   -   Katie McDowell   -   Matteo Meucci     -   Antonio Parata    -   Mark Roxberry
  -   Marco Belotti      -   Marco Cova       -   Paul Davies       -   Matteo G.P. Flora   -   Darrell Groundy   -   James Kist   -   Marco Mella      -   Syed Mohamed A.   -   Alberto Revelli   -   Dave Wichers
</pre>
  ---------------------- 

Trademarks
----------

-   Java, Java Web Server, and JSP are registered trademarks of Sun Microsystems, Inc.
-   Merriam-Webster is a trademark of Merriam-Webster, Inc.
-   Microsoft is a registered trademark of Microsoft Corporation.
-   Octave is a service mark of Carnegie Mellon University.
-   VeriSign and Thawte are registered trademarks of VeriSign, Inc.
-   Visa is a registered trademark of VISA USA.
-   OWASP is a registered trademark of the OWASP Foundation

All other products and company names may be trademarks of their respective owners. Use of a term in this document should not be regarded as affecting the validity of any trademark or service mark.
