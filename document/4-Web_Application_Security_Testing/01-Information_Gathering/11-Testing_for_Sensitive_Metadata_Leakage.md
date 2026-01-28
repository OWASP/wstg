# Testing for Sensitive Metadata Leakage

| ID  |
| --- |
| WSTG-INFO-11 |

## Summary

Web applications often expose publicly accessible files such as images, PDF documents, and office files. These files may contain embedded metadata that is not visible during normal usage but can be extracted using common tools.

Sensitive metadata may reveal internal usernames, file system paths, software versions, device details, or location data. Although this does not directly exploit an application vulnerability, metadata leakage can significantly assist attackers during reconnaissance and social engineering phases.

## Test Objectives

- Identify publicly accessible files that contain embedded metadata.
- Determine whether exposed metadata reveals sensitive or internal information.
- Assess how leaked metadata could support further attacks.

## How to Test

Review files that are accessible without authentication or authorization. These may include files published intentionally by the organization or files generated dynamically by the application.

Testing should include, but not be limited to:

- Images hosted on public web pages.
- Documents available for download (reports, brochures, invoices).
- Files generated through export or reporting functionality.
- User-uploaded files that are publicly accessible.
- Files located in static directories such as `/uploads/`, `/files/`, or `/documents/`.

Testing should not be limited to image files, as document formats often contain richer and more sensitive metadata.

### Metadata Analysis

Inspect downloaded files for embedded metadata fields that may expose sensitive information. Focus on metadata that is specific to the organization or its users rather than generic or default values.

#### Using ExifTool

ExifTool is a commonly used utility for extracting metadata from image and document files. It supports a wide range of formats including JPEG, PNG, PDF, and Office documents.

To extract metadata from a file, the following command can be used:

```text
exiftool image.jpg
```

This command may reveal metadata fields such as:

- GPS coordinates indicating where a photo was taken
- Device make and model (camera, mobile phone)
- Software or application used to create or edit the file
- Author or creator names
- File system paths embedded during document creation
- Creation and modification timestamps

For example, GPS metadata embedded in images may disclose the physical location of an office or an employee’s home, while author names and file paths may expose valid usernames or internal directory structures.

### Security Impact

Exposed metadata may assist attackers by:

- Enabling targeted phishing using real employee names
- Supporting username enumeration attacks
- Revealing internal system naming conventions
- Disclosing physical locations through GPS data
- Allowing attackers to tailor attacks based on known software versions

Although metadata leakage does not directly compromise the application, it lowers the barrier for targeted attacks.

## Example Attack Scenario

An attacker downloads a publicly accessible image from a company website and extracts metadata using ExifTool. The metadata reveals GPS coordinates corresponding to an internal office location and an author name matching an internal username. This information can be used to support targeted social engineering or reconnaissance activities.

## False Positives

- Generic metadata fields that do not reference real users, systems, or locations.
- Metadata automatically added by widely used tools without organization-specific context.

## False Negatives

- Metadata removed from visible fields but still present in embedded objects.
- Sanitized documents that retain hidden properties or revision history not detected by basic analysis.

## Tools

- ExifTool
- pdfinfo
- strings
- binwalk

## Remediation

Carefully review and sanitize files before making them publicly accessible.

Recommended mitigations include:

- Removing metadata from files prior to publication.
- Configuring document generation systems to avoid embedding internal usernames and paths.
- Re-encoding uploaded images on the server side.
- Sanitizing PDF and Office documents before external distribution.
- Disabling document revision history and hidden properties.
- Verifying metadata sanitization as part of the release process.

## References

- OWASP Web Security Testing Guide – Information Leakage
- Vendor documentation for metadata removal tools
- Digital forensics best practices
