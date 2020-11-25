# Test Upload of Unexpected File Types

|ID          |
|------------|
|WSTG-BUSL-08|

## Summary

Many applications' business processes allow for the upload and manipulation of data that is submitted via files. But the business process must check the files and only allow certain "approved" file types. Deciding what files are "approved" is determined by the business logic and is application/system specific. The risk in that by allowing users to upload files, attackers may submit an unexpected file type that that could be executed and adversely impact the application or system through attacks that may deface the web site, perform remote commands, browse the system files, browse the local resources, attack other servers, or exploit the local vulnerabilities, just to name a few.

Vulnerabilities related to the upload of unexpected file types is unique in that the upload should quickly reject a file if it does not have a specific extension. Additionally, this is different from uploading malicious files in that in most cases an incorrect file format may not by it self be inherently "malicious" but may be detrimental to the saved data. For example if an application accepts Windows Excel files, if an similar database file is uploaded it may be read but data extracted my be moved to incorrect locations.

The application may be expecting only certain file types to be uploaded for processing, such as `.csv` or `.txt` files. The application may not validate the uploaded file by extension (for low assurance file validation) or content (high assurance file validation). This may result in unexpected system or database results within the application/system or give attackers additional methods to exploit the application/system.

### Example

Suppose a picture sharing application allows users to upload a `.gif` or `.jpg` graphic file to the web site. What if an attacker is able to upload an HTML file with a `<script>` tag in it or PHP file? The system may move the file from a temporary location to the final location where the PHP code can now be executed against the application or system.

## Test Objectives

- Review the project documentation for file types that are rejected by the system.
- Verify that the unwelcomed file types are rejected and handled safely.
- Verify that file batch uploads are secure and do not allow any bypass against the set security measures.

## How to Test

### Specific Testing Method

- Study the applications logical requirements.
- Prepare a library of files that are "not approved" for upload that may contain files such as: jsp, exe, or HTML files containing script.
- In the application navigate to the file submission or upload mechanism.
- Submit the "not approved" file for upload and verify that they are properly prevented from uploading
- Check if the website only do file type check in client-side JavaScript
- Check if the website only check the file type by "Content-Type" in HTTP request.
- Check if the website only check by the file extension.
- Check if other uploaded files can be accessed directly by specified URL.
- Check if the uploaded file can include code or script injection.
- Check if there is any file path checking for uploaded files. Especially, hackers may compress files with specified path in ZIP so that the unzip files can be uploaded to intended path after uploading and unzip.

## Related Test Cases

- [Test File Extensions Handling for Sensitive Information](../02-Configuration_and_Deployment_Management_Testing/03-Test_File_Extensions_Handling_for_Sensitive_Information.md)
- [Test Upload of Malicious Files](09-Test_Upload_of_Malicious_Files.md)

## Remediation

Applications should be developed with mechanisms to only accept and manipulate "acceptable" files that the rest of the application functionality is ready to handle and expecting. Some specific examples include: deny lists or allow lists of file extensions, using "Content-Type" from the header, or using a file type recognizer, all to only allow specified file types into the system.

## References

- [OWASP - Unrestricted File Upload](https://owasp.org/www-community/vulnerabilities/Unrestricted_File_Upload)
- [File upload security best practices: Block a malicious file upload](https://www.computerweekly.com/answer/File-upload-security-best-practices-Block-a-malicious-file-upload)
- [Stop people uploading malicious PHP files via forms](https://stackoverflow.com/questions/602539/stop-people-uploading-malicious-php-files-via-forms)
- [CWE-434: Unrestricted Upload of File with Dangerous Type](https://cwe.mitre.org/data/definitions/434.html)
