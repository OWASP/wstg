# Sysreptor-Checklisten Mapping

| SysReptor ID | Checklisten ID | Befundname (Englisch) | Befundname (Deutsch) |
| --- | --- | --- | --- |
| `f184fd0e-61ce-4441-8ad7-4b1c769bcaa0` | `WSTG-ATHZ-02-4` | Authorization Bypass via Special Request Headers | Umgehung der Autorisierung durch spezielle Request-Header |
| `6dda8065-776f-4fc9-a7bf-78bf73232d29` | `WSTG-APIT-04-1` | Broken Function Level Authorization (BFLA) | Fehlerhafte Autorisierung auf API-Funktionsebene (BFLA) |
| `d9b69440-08f6-41d9-acf8-ef830d559093` | `WSTG-APIT-02-1` | Broken Object Level Authorization (BOLA / IDOR) | Fehlerhafte Autorisierung auf API-Objektebene (BOLA / IDOR) |
| `f7b8c006-4a33-415f-8ff8-d8c478305764` | `WSTG-ATHZ-05-1` | Usage of Deprecated OAuth Grant Types | Verwendung veralteter OAuth Grant-Typen |
| `71c66b44-c240-4ac2-afd2-8d8f179ff811` | `WSTG-ATHZ-02-1` | Unauthenticated Access / Forced Browsing | Unauthentifizierter Zugriff / Forced Browsing |
| `0ff95f89-a761-47a4-99cd-6f38931219c9` | `WSTG-ATHZ-02-2` | Horizontal Privilege Escalation | Horizontale Rechteausweitung (Privilege Escalation) |
| `4082d305-c9c0-49c9-a788-966998870857` | `WSTG-ATHZ-04-4` | Insecure Direct Object Reference (IDOR) | Unsichere direkte Objektverweise (IDOR) |
| `b23bdc69-fdff-4816-a641-315c3d544dd9` | `WSTG-APT-01-3` | Missing Tenant Isolation | Fehlende Mandantentrennung (Tenant Isolation) |
| `b3d9a319-0aa2-418c-a906-964eeebb216a` | `WSTG-ATHZ-05-2` | OAuth Credential Leakage via URLs or Referer Headers | OAuth-Credential-Leakage über URLs oder Referer-Header |
| `ba828fbc-91b2-497d-9ef6-9455668016dd` | `WSTG-ATHZ-01-1` | Path Traversal | Verzeichnisdurchquerung (Path Traversal) |
| `217c563b-d4b2-475d-ad65-7888fd7af628` | `WSTG-ATHZ-02-3` | Vertical Privilege Escalation | Vertikale Rechteausweitung (Privilege Escalation) |
| `e850873f-2580-4dbd-9ac5-f59ffaa9d292` | `WSTG-ATHN-04-4` | Authentication Bypass via Loose Type Comparison / Magic Hashes | Authentifizierungsumgehung durch schwache Typenvergleiche / Magic Hashes |
| `af067e8e-3375-4ed6-a72e-b5ab27fe0135` | `WSTG-ATHN-04-1` | Authentication Bypass via Parameter Modification | Authentifizierungsumgehung durch Parameter-Manipulation |
| `fd13a20a-dd1b-4e94-80e8-b707f738f577` | `WSTG-ATHN-04-5` | Authentication Bypass via Same Length Password | Authentifizierungsumgehung durch Passwörter gleicher Länge |
| `6169fc59-0cf0-41f2-ae6e-0f3212baa756` | `WSTG-ATHN-06-1` | Sensitive Information Exposure via Browser History | Preisgabe sensibler Informationen über den Browserverlauf |
| `0fa62b3b-562a-4d58-a0f1-c39f856c136c` | `WSTG-ATHN-08-3` | Brute-forcible Security Question Answers | Durch Brute-Force ermittelbare Antworten auf Sicherheitsfragen |
| `2d597a6e-de04-47fd-b8fe-6e4d49ceaa20` | `WSTG-ATHN-03-2` | CAPTCHA Implementation Weakness | Schwäche in der CAPTCHA-Implementierung |
| `1bc13abe-779a-470b-b17c-302827bc4a2e` | `WSTG-SESS-06-4` | Cross-Device Session Reuse | Geräteübergreifende Sitzungswiederverwendung |
| `baeb9110-d089-4e38-b381-de29e88f3aa8` | `WSTG-ATHN-05-2` | Excessive 'Remember Me' Token Lifetime | Übermäßige Lebensdauer des 'Angemeldet bleiben'-Tokens |
| `ecb305dc-d5ce-4140-8bdc-5d79166a305a` | `WSTG-SESS-07-1` | Excessive Session Lifetime | Fehlendes oder schwaches Sitzungs-Timeout |
| `94372bcf-7173-4d5e-9c46-4a1d423817bc` | `WSTG-SESS-06-2` | Incomplete Server-Side Session Termination | Unvollständige serverseitige Sitzungsbeendigung |
| `19f86e86-8824-40e2-890e-8a879375118c` | `WSTG-SESS-01-1` | Information Leakage in Session Tokens | Informationspreisgabe in Sitzungs-Tokens |
| `44e292e8-1430-4287-9b4b-927b283610e3` | `WSTG-ATHN-11-3` | Insecure MFA Recovery Options | Unsichere MFA-Wiederherstellungsoptionen |
| `6e2f1a03-a815-433d-9479-df639c3e39ee` | `WSTG-ATHN-05-1` | Insecure Storage of 'Remember Me' Credentials | Unsichere Speicherung von 'Angemeldet bleiben'-Anmeldedaten |
| `daceebaf-5cd0-4272-b200-ecbf87de8b3d` | `WSTG-ATHN-08-2` | Insecure Self-Generated Security Questions | Unsichere selbst erstellte Sicherheitsfragen |
| `dbdbdf52-6bf0-4da2-9acb-b4cd36af9e6b` | `WSTG-SESS-10-4` | JWT Algorithm Confusion | JWT-Algorithmus-Verwirrung (HMAC vs. Public Key) |
| `abbcb30f-439c-4740-9929-69345dd36e15` | `WSTG-SESS-10-5` | JWT Key ID (kid) Manipulation | Manipulation der JWT Key ID (kid) |
| `38c780ff-011a-4601-b62d-5ba72d74d71f` | `WSTG-SESS-10-2` | JWT Signature Validation Missing ('none' Algorithm) | Fehlende JWT-Signaturprüfung ('none'-Algorithmus) |
| `eebf071c-e596-4b6c-9e79-869486e426e5` | `WSTG-SESS-10-3` | JWT Uses Weak Signing Algorithm | Schwacher JWT-Signaturalgorithmus (HMAC-Schlüssel) |
| `920b452f-81db-41cb-b397-3e496b3e0ce5` | `WSTG-ATHN-11-1` | MFA Flow Bypass | Umgehung des MFA-Flusses |
| `7f660069-c00b-4952-b177-7cd66c1ef5c2` | `WSTG-ATHN-11-2` | MFA Management Vulnerabilities | Schwachstellen in der MFA-Verwaltung |
| `5349efbd-706b-4f81-b7c4-fd8daa3c9027` | `WSTG-ATHN-03-1` | Missing Account Lockout Mechanism | Fehlender Konto-Sperrmechanismus |
| `364fdf43-c2c3-4ddb-b855-b4941efed46e` | `WSTG-SESS-06-1` | Missing or Hidden Logout User Interface | Fehlende oder versteckte Logout-Benutzeroberfläche |
| `abe1f2c1-2003-424a-81ed-2a4a21c46818` | `WSTG-ATHN-11` | Missing Multi-Factor Authentication (MFA) | Fehlende Multi-Faktor-Authentifizierung (MFA) |
| `617969ff-fedb-47e6-afaa-68549251d433` | `WSTG-ATHN-09-1` | New Password Sent in Cleartext via Email | Neues Passwort im Klartext per E-Mail gesendet |
| `4a46b69a-1d7e-40ee-a220-9a03d52105c3` | `WSTG-SESS-02-3` | Overly Permissive Cookie Domain or Path Attributes | Zu weitreichende Cookie-Attribute ('Domain' oder 'Path') |
| `a1474d58-f11f-4fb1-bb8c-0a031d9d6dd2` | `WSTG-ATHN-09-2` | Predictable Password Reset Token | Vorhersehbare Passwort-Reset-Tokens |
| `9ff7fe4a-d836-4831-b2aa-e25fd8bb6ad8` | `WSTG-SESS-01-2` | Predictable Session Identifiers | Vorhersagbare Sitzungs-Tokens |
| `cc1f285d-8698-4782-8da0-e75a49d2f8d5` | `WSTG-ATHN-06-2` | Sensitive Data Stored in Browser Cache | Sensible Daten im Browser-Cache gespeichert |
| `0d94925f-5e1e-4c33-8a12-48520a433965` | `WSTG-SESS-10-1` | Sensitive Data in JWT Payload | Sensible Daten im JWT-Payload |
| `6984ad3d-69ec-4f03-96f5-42e3021b946b` | `WSTG-SESS-02-2` | Session Cookie Missing 'HttpOnly' Attribute | Fehlendes 'HttpOnly'-Attribut bei Cookie |
| `38fa9dbe-b6f1-4d68-8b93-f85e5f02358e` | `WSTG-SESS-02-4` | Session Cookie Missing 'SameSite' Attribute | Fehlendes 'SameSite'-Attribut bei Cookie |
| `84605ad1-75b8-4724-91d2-844b042b5408` | `WSTG-SESS-02-1` | Session Cookie Missing 'Secure' Attribute | Fehlendes 'Secure'-Attribut bei Cookie |
| `3e21cad0-e880-4ee2-8122-8e86693a3ecc` | `WSTG-SESS-03-1` | Session Fixation | Sitzungsfixierung (Session Fixation) |
| `144e85f1-77c2-4d4b-b00b-bad3bc8ec995` | `WSTG-SESS-08-1` | Session Puzzling / Session Variable Overloading | Sitzungspuzzle / Überladung von Sitzungsvariablen |
| `3c27d744-f44e-45d3-ab9b-29df8fce1d13` | `WSTG-SESS-04-1` | Session Tokens Exposed in URL | Sitzungs-Tokens in URL exponiert (GET-Anfragen) |
| `0c51fbd2-755c-4ed9-b2d2-4b130e66651b` | `WSTG-SESS-04-2` | Session Tokens Exposed via Caching | Sitzungs-Tokens durch Caching exponiert |
| `27641b1f-cd6f-420a-a6e2-4fb8f00a4522` | `WSTG-SESS-06-3` | Single Sign-Off Failure in SSO Environments | Fehlschlagen des Single Sign-Offs in SSO-Umgebungen |
| `20cb1873-57b2-403a-bf36-8c8d2fcf6f85` | `WSTG-SESS-09-1` | Susceptibility to Session Hijacking | Anfälligkeit für Session Hijacking |
| `cf30c4f4-ff53-46ee-b30d-2163cae8a6c9` | `WSTG-SESS-11-1` | Unrestricted Concurrent Sessions | Uneingeschränkte gleichzeitige Sitzungen |
| `43d86509-fc98-4036-8aa9-0de425945de4` | `WSTG-IDNT-04-1` | Username Enumeration | Benutzer-Aufzählung (Enumeration) |
| `9b5a6b68-fc9a-4cbe-902f-db4ed7a370ca` | `WSTG-ATHN-03-3` | Weak Account Unlock Mechanism | Schwacher Mechanismus zur Kontoentsperrung |
| `4143b53d-8f83-4fb9-a60b-883841e52c7b` | `WSTG-ATHN-07-2` | Use of Weak Alternative Credentials | Verwendung schwacher alternativer Anmeldedaten |
| `80e2373f-f143-432f-b67c-c7ea6d384312` | `WSTG-ATHN-11-4` | Weak OTP Implementation | Schwache oder durch Brute-Force ermittelbare OTPs |
| `06bd803b-5be3-46ae-80d4-4a95c9fc7633` | `WSTG-ATHN-07-1` | Weak Password Policy | Schwache Passwortrichtlinie |
| `4a47dffa-33a6-45c0-bdf6-71cad54d87eb` | `WSTG-ATHN-09-2` | Weak Password Reset Mechanism | Schwacher Mechanismus zum Zurücksetzen von Passwörtern |
| `522ddf99-6d78-4a99-95cb-5b64b24d0001` | `WSTG-ATHN-08-1` | Weak Pre-generated Security Questions | Schwache vorgefertigte Sicherheitsfragen |
| `02e46712-0e3d-480d-8408-0d5033afbd7a` | `WSTG-ATHN-10-1` | Weaker Authentication in Alternative Channels | Schwächere Authentifizierung in alternativen Kanälen |
| `c5581325-d308-4366-ade6-711d05b4ed7e` | `WSTG-APT-02-1` | End-of-Life Software | Veraltete / End-of-Life Software im Einsatz |
| `08fdf2c7-0c2c-4002-9361-e8e8ae4c8864` | `WSTG-APT-02-1` | Known Vulnerable Component | Verwundbare Software-Komponente (Bekannte CVEs) |
| `abce75c9-638d-46ec-8a29-689f20e97c60` | `WSTG-APT-02-1` | Outdated Libraries | Veraltete Bibliotheken |
| `7349e070-aeb4-412f-a088-dd86e562e23e` | `WSTG-APT-02-1` | Vulnerable Framework Version | Verwundbare Framework-Version |
| `b5d353bf-287f-4f6d-9e98-a844a5e482ae` | `WSTG-APT-02-1` | Vulnerable JavaScript Dependency | Verwundbare JavaScript-Abhängigkeit |
| `fe674a78-e38d-41e0-b1b8-411dea08f94e` | `WSTG-CRYP-01-2` | TLS Certificate Validation Issues | Ungültiges oder nicht vertrauenswürdiges TLS-Zertifikat |
| `c31597f5-bea2-4393-ba31-eb01e918040d` | `WSTG-CRYP-01-1` | Deprecated TLS Versions Enabled | Veraltete TLS-Protokolle aktiviert |
| `524acd37-e9af-4561-8463-9858c4d8f450` | `WSTG-CRYP-04-2` | Insecure Random Number Generation | Unsichere Zufallszahlengenerierung |
| `cf580f7b-cab7-499a-8b74-be947eace332` | `[NEU HINZUFÜGEN]` | Missing Encryption at Rest | Fehlende Verschlüsselung sensibler Daten in der Datenbank |
| `30833f5d-2939-4a1e-911f-416712d77876` | `WSTG-CRYP-01-3` | Mixed Active Content | Gemischte aktive Inhalte (Mixed Content) |
| `658f671b-2363-48de-950f-e78195d839f7` | `WSTG-CRYP-02-1` | Padding Oracle Attack | Padding-Oracle-Angriff |
| `a97499d9-91f1-4d42-bf4a-72e4e5d24992` | `WSTG-CRYP-03-1` | Sensitive Data Transmitted over HTTP | Sensible Daten über unverschlüsseltes HTTP übertragen |
| `d4985bbb-37ad-4ccb-a92e-327058159065` | `WSTG-CRYP-01-1` | Weak Cipher Suites Enabled | Schwache TLS-Ciphers aktiviert |
| `6afca0f2-0258-4e81-abd9-688ecec848d3` | `WSTG-CRYP-04-1` | Weak Cryptographic Algorithms | Verwendung schwacher kryptografischer Algorithmen |
| `ef09eb92-2418-4287-a92d-6e3573fb5778` | `[NEU HINZUFÜGEN]` | Weak Password Hashing | Schwache Passwort-Hashing-Algorithmen |
| `09d1f8ed-72c1-4b55-8dc1-042e4ece0bc0` | `WSTG-CRYP-01-1` | Weak TLS Configuration | Schwache TLS-Konfiguration |
| `b63ffda7-99cd-45d0-ac19-87466bc87ec8` | `WSTG-BUSL-06-1` | Business Logic Bypass | Umgehung der Geschäftslogik / Workflows |
| `662aa666-d85d-43df-a19d-f7dd80b4aa08` | `WSTG-BUSL-01-1` | Business Logic Data Validation Failure | Fehler in der Validierung von Geschäftslogik-Daten |
| `dcfceacd-0524-4837-8157-261daeb7dacb` | `WSTG-BUSL-10-2` | Coupon / Voucher Reuse | Mehrfachnutzung von Gutscheinen (Coupon Reuse) |
| `2aef56e6-35a1-4968-8aa1-272e6a478ca9` | `[NEU HINZUFÜGEN]` | Insufficient Step-Up Authentication | Unzureichende Step-Up-Authentifizierung bei kritischen Aktionen |
| `74599e1f-7844-4e88-819e-e3d3dd03fff3` | `WSTG-BUSL-03-1` | Integrity Check Bypass via Hidden Fields | Umgehung der Integritätsprüfung über versteckte Felder |
| `c4d8c7b8-afc2-41e7-be27-9faec85d747d` | `WSTG-BUSL-06-1` | Missing Approval Workflow | Fehlender Genehmigungs-Workflow |
| `601281ef-5348-43e8-b4ce-a0c1ea3be43e` | `WSTG-BUSL-07-1` | Missing Defenses Against Application Misuse | Fehlende Abwehrmaßnahmen gegen Anwendungs-Missbrauch |
| `70344f93-3c1e-448f-a6aa-f13af8e95901` | `WSTG-BUSL-05-1` | Missing Function Use Limits | Fehlende Beschränkungen der Funktionsnutzung |
| `e9bed5f6-2c3d-4a3a-9352-4d01ffe9e319` | `WSTG-BUSL-05-1` | Missing Rate Limiting | Fehlendes Rate Limiting |
| `8822c86b-1146-44e4-9780-bfb7ebdc76db` | `WSTG-BUSL-06-1` | Predictable Workflow | Vorhersagbarer Workflow |
| `2045ca8b-d854-4eaa-9dd5-0bd650cd7a00` | `WSTG-BUSL-10-1` | Price Manipulation | Preismanipulation am Payment-Gateway |
| `e3082723-ab62-4d8a-81c5-b044bc1d0b6a` | `WSTG-BUSL-04-1` | Process Timing Vulnerabilities | Prozess-Timing-Schwachstellen |
| `1ecc5d1b-e034-4aa0-92cb-93f62b4b2c52` | `WSTG-BUSL-10-2` | Race Condition | Race Condition (TOCTOU) |
| `71a5c02a-9ab8-4ba9-b9ca-83b11c1c922d` | `WSTG-BUSL-02-1` | Ability to Forge Requests via Hidden Features | Möglichkeit zur Fälschung von Anfragen über versteckte Funktionen |
| `d850f5f5-c5ac-418b-af85-1d31376b9ba2` | `WSTG-INPV-11-2` | ASP/.NET Code Injection | ASP/.NET-Code-Injection |
| `17d93918-e84f-471a-b465-570793abb918` | `WSTG-INPV-12-2` | Blind OS Command Injection | Blinde OS Command-Injection |
| `d96c43a4-1b02-4f41-a4e3-ce38f08dba1b` | `WSTG-INPV-05-4` | Blind / Time-Based SQL Injection | Blind / Time-Based SQL-Injection |
| `477b2c62-d68e-475e-afa5-1f548fc2c0ee` | `WSTG-INPV-12-1` | Command Injection | OS Command-Injection |
| `74561a14-b5b3-4209-8f73-d4a4a98562e1` | `WSTG-INPV-15-1` | CRLF Injection / HTTP Response Splitting | HTTP Response Splitting (CRLF-Injection) |
| `0a8ff02c-75ed-42dc-a774-5d597e5e7807` | `WSTG-INPV-13-1` | Format String Injection | Format String-Injection |
| `56cdae7d-a51f-411a-b3db-7e569ec2fc0e` | `WSTG-INPV-04-1` | HTTP Parameter Pollution | Serverseitige HTTP Parameter Pollution (HPP) |
| `856592ea-fe6d-43e3-ae18-35a538bd324d` | `WSTG-INPV-16-1` | HTTP Request Smuggling | HTTP Request Smuggling (CL.TE / [TE.CL](http://te.cl/)) |
| `1a4787db-a4aa-4409-83c8-adf09fd17405` | `WSTG-INPV-14-1` | Incubated Vulnerability (Persistent Attack) | Inkubierte Schwachstelle (Persistent Attack) |
| `acee6d19-146d-4f2e-a350-82cdb217b463` | `WSTG-INPV-06-1` | LDAP Injection | LDAP-Injection |
| `fdcda37e-887b-4242-b9e5-0adc435df793` | `[NEU HINZUFÜGEN]` | NoSQL Injection | NoSQL-Injection |
| `892b5c1c-6eb9-4c96-82e8-f8717d412d35` | `WSTG-INPV-11-1` | PHP Code Injection | PHP-Code-Injection |
| `2a075b88-5a3e-4e25-806a-c735a48da613` | `[NEU HINZUFÜGEN]` | Prototype Pollution | Prototype Pollution |
| `26f4d942-beca-4179-9f89-f84c12e1fb70` | `WSTG-INPV-18-1` | Server-Side Template Injection (SSTI) | Server-Side Template Injection (SSTI) |
| `d50e3958-4270-4bb0-88c3-f7b8f6f88584` | `WSTG-INPV-05-1` | SQL Injection | SQL-Injection |
| `3085e8c8-61cc-4242-8f75-3ad55dd8eae4` | `WSTG-INPV-07-2` | XML External Entity (XXE) Injection | XML External Entity (XXE)-Injection |
| `521751fb-943b-4655-8b0a-38aab60a00e2` | `WSTG-INPV-07-1` | XML Tag/Content Injection | XML Tag/Inhalt-Injection |
| `5d3cc328-2ca3-44a4-918c-77a5b01b1fb9` | `WSTG-INPV-09-1` | XPath Injection | XPath-Injection |
| `4541d0a2-6cdc-4b5f-bf43-7d726e245513` | `WSTG-APT-02-1` | Dependency Confusion | Dependency Confusion |
| `074dab4c-6bb0-447d-aff7-e2084864b0ab` | `WSTG-APT-03-2` | Insecure Deserialization | Deserialisierung von nicht vertrauenswürdigen Daten |
| `5e8d2c71-0764-4f34-ac8d-cb6e424b44c1` | `WSTG-APT-03-3` | Insecure Update Mechanism | Unsicherer Update-Mechanismus |
| `a66ae0a9-c2ad-42e5-bf57-aeb17c11844c` | `WSTG-APT-03-1` | Missing Signature Validation | Fehlende Überprüfung von Software-Signaturen |
| `390efe91-df3a-49e4-9cff-1f409b3d84e6` | `[NEU HINZUFÜGEN]` | Missing Subresource Integrity (SRI) | Fehlende Subresource Integrity (SRI) |
| `dcde3825-bed4-4225-a0ee-2394b9b59de2` | `WSTG-APT-04-2` | Missing Security Alerting | Fehlendes oder unwirksames Security Alerting |
| `4d0d8d4c-e4b5-4044-83b2-ac3fe8629c0e` | `WSTG-APT-04-1` | Missing Audit Logging | Unzureichende Protokollierung (Audit Logging) |
| `c825db86-7f31-417c-bfca-c1f0993228d8` | `WSTG-APT-04-1` | Missing Security Event Logging | Fehlendes Logging sicherheitsrelevanter Ereignisse |
| `8be1c45d-f214-4e9c-9a22-07fd545d2a62` | `[NEU HINZUFÜGEN]` | Sensitive Information in Logs | Sensible Informationen in Server-Logs |
| `0b3ee6b6-67d6-4fd8-8b8d-622cec2f87d1` | `WSTG-ATHZ-01-1` | Arbitrary File Read | Beliebiges Lesen von Dateien (Arbitrary File Read) |
| `b53b1bcd-399b-4344-a41a-29b5d1703e23` | `WSTG-BUSL-09-1` | Arbitrary File Write | Beliebiges Schreiben von Dateien (Arbitrary File Write) |
| `536112f2-2220-41a9-b1e3-246421ed02db` | `WSTG-BUSL-09-2` | Archive Directory Traversal (Zip Slip) | Archive Directory Traversal (Zip Slip / Zip-Bombe) |
| `464a118a-aa46-4dde-8211-a34d20e6e27c` | `WSTG-INPV-02-3` | Blind Cross-Site Scripting (XSS) | Blindes Cross-Site Scripting (Blind XSS) |
| `52da968d-975a-40c4-b595-07f9a8aca1fd` | `WSTG-CLNT-09-1` | Clickjacking | Clickjacking (UI Redressing) |
| `581a1492-dcba-49f8-907d-82da8919cad2` | `WSTG-INFO-05-2` | Client-Side Secrets | Sensible Informationen in clientseitigen Variablen |
| `22f23705-4a81-47be-affd-d2fdf622149d` | `WSTG-SESS-05-1` | Cross-Site Request Forgery (CSRF) | Cross-Site Request Forgery (CSRF) |
| `ea1a8274-b7e1-4e1d-b71f-f9e0a831670d` | `WSTG-CLNT-01-1` | DOM-based Cross-Site Scripting (XSS) | DOM-basiertes Cross-Site Scripting (XSS) |
| `82746a34-44ac-46c1-9ae6-89d944b13abf` | `WSTG-INPV-10-1` | Email Header Injection | Email Header Injection |
| `915a1654-1293-4a38-86df-915ed619e4cc` | `WSTG-APIT-03-1` | Excessive Data Exposure | Übermäßige Datenoffenlegung (Excessive Data Exposure) |
| `78f6717a-cd24-45b1-a53a-e1f4ca95a1b2` | `[NEU HINZUFÜGEN]` | GraphQL Authorization Bypass | Umgehung der Autorisierung in GraphQL |
| `aa6cf95e-5231-4cb4-b09b-fc44ab2994a6` | `WSTG-APIT-99-1` | GraphQL Introspection Enabled | GraphQL Introspection aktiviert |
| `72250d29-1afe-46eb-9a47-0ec77528ba73` | `WSTG-INPV-17-1` | Host Header Injection | Host-Header-Injection |
| `a3360960-21ac-45ad-a0f2-e80b32943eff` | `WSTG-CLNT-03-1` | HTML Injection | HTML-Injection |
| `6a213aeb-d0a0-4fd7-883e-039689decd54` | `[NEU HINZUFÜGEN]` | Information Disclosure | Allgemeine Informationspreisgabe |
| `1f9444b4-b343-48db-a9c1-858168622f5b` | `WSTG-ATHZ-01-1` | Local File Inclusion (LFI) | Local File Inclusion (LFI) |
| `62b3717e-553d-4112-b843-3a4f60a3f71e` | `WSTG-BUSL-09-1` | Upload of Malicious Files (Web Shells) | Upload von bösartigen Dateien (Web Shells) |
| `38a83b7f-e4ec-4ab4-9307-0c9da0af669a` | `WSTG-INPV-20-1` | Mass Assignment | Mass Assignment / Autobinding |
| `bfa77fd8-52e0-4e4d-901c-d77e70959b54` | `WSTG-ERRH-01-1` | Mishandling of Exceptional Conditions | Fehlerhafte Fehlerbehandlung & Informationspreisgabe |
| `03ff314a-8fa5-4dbb-a942-3cef2fc19331` | `[NEU HINZUFÜGEN]` | Missing API Authentication | Fehlende API-Authentifizierung |
| `5046f108-3822-446f-9b49-4efb7469b00b` | `[NEU HINZUFÜGEN]` | Missing API Authorization | Fehlende API-Autorisierung |
| `bfd063b5-2020-4f87-8a1c-a4f49bb47dfe` | `WSTG-INFO-03-4` | Missing security.txt | Fehlende security.txt |
| `87c09b42-1c60-4842-9f70-322bcc0eb8eb` | `WSTG-CLNT-04-1` | Open Redirect | Clientseitige URL-Weiterleitung (Open Redirect) |
| `2c29f84b-b204-455f-a10d-d164670918ab` | `WSTG-INPV-01-1` | Reflected Cross-Site Scripting (XSS) | Reflektiertes Cross-Site Scripting (XSS) |
| `87c16914-7ae7-4889-b16e-723fbebb8e5e` | `WSTG-INPV-12-1` | Remote Code Execution | Remotecodeausführung (RCE) |
| `c9f7913b-638c-4e4f-9bf3-1c26e6a0e738` | `WSTG-ATHZ-01-2` | Remote File Inclusion (RFI) | Remote File Inclusion (RFI) |
| `9261d030-b3f8-45f3-a551-a4a65a08d217` | `WSTG-INFO-03-1` | Information Disclosure via robots.txt | Informationspreisgabe durch robots.txt |
| `c3ae8c25-33b4-4b85-99ad-14ccb12ae6ab` | `WSTG-INFO-05-2` | Sensitive Information in Client-Side Code | Sensible Informationen in clientseitigem Quellcode |
| `28862244-7a2a-42d7-b1e3-0d15ecdcd2af` | `WSTG-INPV-02-1` | Stored Cross-Site Scripting (XSS) | Gespeichertes Cross-Site Scripting (XSS) |
| `98ab8593-b1f5-46af-88de-9a97c23d36ed` | `WSTG-INPV-02-2` | Stored XSS via File Upload (MIME Mishandling) | Gespeichertes XSS durch Datei-Upload (MIME-Fehler) |
| `62d2caff-2881-4e28-b94f-d5ab70b57a09` | `WSTG-BUSL-08-1` | Unrestricted File Upload | Ungeprüfter Datei-Upload (Unrestricted File Upload) |
| `28544843-688a-4619-85bc-a1b8e242222d` | `WSTG-CONF-13-1` | Web Cache Deception | Web Cache Deception |
| `5f2ef3b1-692a-4e24-bb9f-697ffa2d365a` | `[NEU HINZUFÜGEN]` | Web Cache Poisoning | Web Cache Poisoning |
| `269297d0-a052-41c6-8a91-1e4e5e563a54` | `WSTG-CONF-04-1` | Backup Files Accessible | Zugriff auf ungeschützte Backup-Dateien |
| `202c86b0-02fb-4200-8cc4-4decb822a1e7` | `WSTG-CLNT-07-1` | CORS Misconfiguration | Unsichere CORS-Richtlinie |
| `e441539f-054f-4cea-b762-6d84a07cc988` | `WSTG-CONF-06-1` | Dangerous HTTP Methods Enabled | Gefährliche HTTP-Methoden unterstützt (z. B. PUT, DELETE) |
| `b8c91414-5ce8-486c-9b12-4c0b169305ec` | `WSTG-CONF-05-1` | Debug Interface Exposed | Exponierte Debug- / Admin-Schnittstelle |
| `a868a064-4664-4476-beb6-28b9e9608c9f` | `WSTG-ATHN-02-1` | Default Credentials | Verwendung von Standard-Zugangsdaten (Default Credentials) |
| `ee69edc9-d3c5-4cc8-996d-f4c6c7c67dd5` | `WSTG-CONF-02-1` | Default Files Accessible | Zugriff auf Standard-Dateien und -Verzeichnisse |
| `717b2313-4d27-43f3-bf24-777f748fd293` | `[NEU HINZUFÜGEN]` | Directory Listing Enabled | Directory Listing aktiviert |
| `91895583-3adf-4a7d-83ae-2df40a481c8c` | `WSTG-CONF-02-3` | Exposed Configuration Files | Exponierte Konfigurationsdateien |
| `eff45b0f-16b2-42c3-850b-9cac80ff78eb` | `WSTG-CONF-02-1` | Exposed Development Files | Exponierte Entwicklungsdateien |
| `415046ac-6af7-44ef-8dfa-1bb9f777907a` | `WSTG-CONF-02-1` | Git Repository Exposed | Exponiertes Git-Repository |
| `8079cfa7-ee53-44dc-a091-d4f6283677dd` | `WSTG-CONF-12-1` | Missing Content Security Policy (CSP) | Content Security Policy (CSP) fehlt oder im Report-Only-Modus |
| `749c55bd-8b51-44fb-b1fb-6a2670548d64` | `WSTG-CONF-07-1` | Missing HTTP Strict Transport Security (HSTS) | HTTP Strict Transport Security (HSTS) fehlt |
| `1fa35d2a-aa62-44e9-a480-b35552b7659c` | `[NEU HINZUFÜGEN]` | Missing Permissions-Policy | Fehlender Permissions-Policy Header |
| `ca7788ce-a3ae-4722-9ce4-60adaecf309c` | `[NEU HINZUFÜGEN]` | Missing Referrer-Policy | Fehlender Referrer-Policy Header |
| `56ec86fb-6b40-4636-8914-ed41e87db105` | `WSTG-CONF-14-1` | Missing Security Headers | Fehlende HTTP-Sicherheitsheader |
| `c7f7d6c1-7d06-49b2-a4c1-413825ba906c` | `[NEU HINZUFÜGEN]` | Missing X-Content-Type-Options | Fehlender X-Content-Type-Options Header |
| `e1bd6f7c-e3e5-4451-b4ad-d040a70891a3` | `WSTG-APIT-01-1` | OpenAPI Specification Exposed | Exponierte OpenAPI-Spezifikation |
| `cb2b06a1-a0a0-47ec-a16b-4ea1906afe5e` | `WSTG-APIT-01-1` | Public Swagger Documentation | Exponierte Swagger-Dokumentation |
| `ca4baf22-491b-44da-bbb6-fafd4abbec09` | `WSTG-INFO-05-3` | Source Maps Accessible | Sensible Informationen in Source Map-Dateien (Source Maps Accessible) |
| `6baaa6c8-54e9-478b-853f-f1ab7b0ee252` | `WSTG-ERRH-01-1` | Verbose Error Messages | Ausführliche Fehlermeldungen (Verbose Error Messages) |
| `66210984-9784-49c8-9610-e926220698fe` | `WSTG-INPV-19-2` | Blind Server-Side Request Forgery | Blind Server-Side Request Forgery (SSRF) |
| `c2a33554-ca8e-4d6a-ae95-43a87fdff3c8` | `WSTG-INPV-19-1` | Cloud Metadata SSRF | Server-Side Request Forgery (SSRF) auf Cloud-Metadaten |
| `95d77276-f806-4812-b1cc-9c7e9ba0c061` | `WSTG-INPV-19-1` | Server-Side Request Forgery (SSRF) | Server-Side Request Forgery (SSRF) |