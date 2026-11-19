# Upload of Unexpected File Types

|ID          |
|------------|
|WSTG-BUSL-08|

## Summary

Many applications' business processes allow for the upload and manipulation of data that is submitted via files. But the business process must check the files and only allow certain "approved" file types. Deciding what files are "approved" is determined by the business logic and is application/system specific. The risk is that by allowing users to upload files, attackers may submit an unexpected file type that could be executed and adversely impact the application or system through attacks that may deface the site, perform remote commands, browse the system files, browse the local resources, attack other servers, or exploit the local vulnerabilities, just to name a few.

Vulnerabilities related to the upload of unexpected file types is unique in that the upload should quickly reject a file if it does not have a specific extension. Additionally, this is different from uploading malicious files in that in most cases an incorrect file format may not by it self be inherently "malicious" but may be detrimental to the saved data. For example if an application accepts Windows Excel files, if a similar database file is uploaded it may be read but data extracted may be moved to incorrect locations.

The application may be expecting only certain file types to be uploaded for processing, such as `.csv` or `.txt` files. The application may not validate the uploaded file by extension (for low assurance file validation) or content (high assurance file validation). This may result in unexpected system or database results within the application/system or give attackers additional methods to exploit the application/system.

### Example

Suppose a picture sharing application allows users to upload a `.gif` or `.jpg` graphic file to the site. What if an attacker is able to upload an HTML file with a `<script>` tag in it or PHP file? The system may move the file from a temporary location to the final location where the PHP code can now be executed against the application or system.

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
- Check if the site only does file type checks in client-side JavaScript
- Check if the site only checks the file type by "Content-Type" in HTTP request.
- Check if the site only checks the file type by the file extension.
- Check if other uploaded files can be accessed directly by specified URL.
- Check if the uploaded file can include code or script injection.
- Check if there is any file path checking for uploaded files. Especially, hackers may compress files with specified path in ZIP so that the extracted files can be uploaded to intended path after uploading and unzipping.

### Testing Upload Reference Revalidation and Cross-Field File Reuse

File upload security checks must remain effective throughout the file's lifecycle, including temporary storage, later association with application records, and delivery to clients. Expiration of upload metadata is not itself a vulnerability. The risk arises when an application continues to trust an existing file reference without revalidating it for the current operation, including its type, ownership, and authorization requirements.

#### Test Objectives

- Verify that temporary file references remain bound to the uploading user, original field, and validated file type.
- Determine whether expired or missing upload metadata causes the application to reject the reference or safely revalidate the underlying file.
- Check whether references can be reused in fields with different validation requirements or by users who do not own the files.
- Verify that file delivery does not allow untrusted content to execute under the application's origin.

#### Testing Procedure

Perform the following tests only with accounts and files you control in an authorized test environment:

1. Identify a workflow that uploads a file to temporary storage and later submits a file identifier, basename, or token to associate it with a record. Record the temporary reference and the field's accepted types.
2. Upload a harmless file allowed by a general-purpose File field. Observe the file's lifetime and any associated validation metadata in the test environment.
3. After the metadata naturally expires, or after simulating that expiration in an isolated laboratory, submit the original reference through its intended workflow. Verify that the application rejects it or revalidates the file before use.
4. Where a second field applies different constraints (for example, an Image field), submit the same reference through that field's normal request. Verify that the server enforces the destination field's content and type requirements rather than trusting the earlier validation.
5. Using two controlled test accounts, attempt to reference an upload owned by the other account. Repeat with roles having different permissions. Verify that ownership and authorization are enforced at every step, including when the file is moved or downloaded. A cross-user authorization issue must be independently demonstrated; cross-field reuse alone does not establish one.
6. If the file is moved to permanent storage, verify that its validated type, owner, and permitted use are preserved or re-established. Missing metadata must not cause a permissive fallback.
7. Request the stored file through each relevant rendering or download endpoint. Inspect the response `Content-Type`, `Content-Disposition`, and `X-Content-Type-Options` headers, and determine whether untrusted files are served from the application's origin.
8. With harmless test content, confirm whether the browser downloads the file, displays it as inert content, or interprets it as an active document. Report actual script execution separately from mere storage or inline rendering.

For example, an application may accept a ZIP file through a general File field, retain the temporary file longer than its metadata, and later accept its reference in an Image field. If the file is then served inline with an invalid or inappropriate response `Content-Type`, and without appropriate content-sniffing protections, some browsers may interpret attacker-controlled HTML as an active document. This outcome is browser- and response-dependent; it must be verified rather than assumed.

#### File Delivery Considerations

- Use a correct response `Content-Type` based on validated content and intended use; do not copy an unvalidated filename extension directly into the header.
- Set `X-Content-Type-Options: nosniff` as a defense-in-depth measure, while recognizing that it does not prevent every active-content scenario.
- Use `Content-Disposition: attachment` for untrusted files that should be downloaded rather than rendered inline.
- Consider delivering untrusted user files from an isolated origin without application credentials, especially where active content cannot be excluded.
- Distinguish execution in an anonymous browser context from execution in an authenticated session when assessing impact.

## Related Test Cases

- [File Extensions Handling for Sensitive Information](../02-Configuration_and_Deployment_Management/03-File_Extensions_Handling_for_Sensitive_Information.md)
- [Upload of Malicious Files](09-Upload_of_Malicious_Files.md)
- [Testing for Stored Cross Site Scripting](../07-Input_Validation_Testing/02-Testing_for_Stored_Cross_Site_Scripting.md)

## Remediation

Applications should be developed with mechanisms to only accept and manipulate "acceptable" files that the rest of the application functionality is ready to handle and expecting. Some specific examples include: deny lists or allow lists of file extensions, using "Content-Type" from the header, or using a file type recognizer, all to only allow specified file types into the system.

## References

- [OWASP - Unrestricted File Upload](https://owasp.org/www-community/vulnerabilities/Unrestricted_File_Upload)
- [File upload security best practices: Block a malicious file upload](https://www.computerweekly.com/answer/File-upload-security-best-practices-Block-a-malicious-file-upload)
- [Stop people uploading malicious PHP files via forms](https://stackoverflow.com/questions/602539/stop-people-uploading-malicious-php-files-via-forms)
- [CWE-434: Unrestricted Upload of File with Dangerous Type](https://cwe.mitre.org/data/definitions/434.html)
- [Tarcísio Luchesi (Poystick) — Upload Metadata Expiration, Cross-Field File Reuse, MIME Sniffing, Stored XSS](https://x.com/P0ystick/status/2123420300217856345?a=zG_V3W7Es20E8M6UABU&s=19)
