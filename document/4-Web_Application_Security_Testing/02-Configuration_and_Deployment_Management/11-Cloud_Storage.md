# Cloud Storage

|ID          |
|------------|
|WSTG-CONF-11|

## Summary

Cloud storage services (AWS S3, Azure Blob Storage, Google Cloud Storage, and equivalents) allow web applications to store and access objects without running their own file servers. Improper access control configuration, however, may lead to the exposure of sensitive information, data tampering, or unauthorized access. By default, storage on all three major providers is private and accessible only to explicitly granted identities, but a bucket/container, or individual objects within it, can be made public - either deliberately (and too broadly) or by mistake - allowing an unauthorized user to read, upload, or modify data.

Beyond bucket-level public access, this class of issue also covers: ACL/IAM policy misconfigurations that grant broader-than-intended access to specific principals; weaknesses in signed/presigned URLs used to grant time-limited access without full credentials; and object versioning/lifecycle configuration that can leave older or supposedly-deleted sensitive data recoverable, or move it into locations with weaker access controls.

## Test Objectives

- Assess that the access control configuration for the storage services (bucket/container-level public access, and object/principal-level ACLs or IAM policies) is properly in place.
- Assess whether signed/presigned URLs are scoped, time-limited, and handled appropriately.
- Assess whether object versioning and lifecycle configuration could expose old or supposedly-removed sensitive data.

## How to Test

First, identify the URL to access the data in the storage service, and then consider the following tests:

- Read unauthorized data
- Upload a new arbitrary file

You may use curl for the tests with the following commands and see if unauthorized actions can be performed successfully.

To test the ability to read an object:

```bash
curl -X GET https://<cloud-storage-service>/<object>
```

To test the ability to upload a file:

```bash
curl -X PUT -d 'test' 'https://<cloud-storage-service>/test.txt'
```

In the above command, it is recommended to replace the single quotes (') with double quotes (") when running the command on a Windows machine.

### Azure Blob Storage

Azure Blob Storage URLs follow the format:

```text
https://<account-name>.blob.core.windows.net/<container-name>/<blob-name>
```

To test public read access to a blob directly:

```bash
curl -X GET "https://<account-name>.blob.core.windows.net/<container>/<blob-name>"
```

To test whether the container itself allows public, unauthenticated listing (equivalent to S3 bucket listing), use the List Blobs REST API:

```bash
curl -X GET "https://<account-name>.blob.core.windows.net/<container>?restype=container&comp=list"
```

A `200` response with an XML `<EnumerationResults>` body indicates the container's public access level is set to `Container` (public read + list), rather than `Private` or `Blob` (public read of known blob names only, no listing).

To test upload/overwrite (requires the appropriate permission, which is normally not granted by "public" access levels, but should still be tested since misconfigured SAS tokens or overly permissive anonymous access can allow it):

```bash
curl -X PUT -d 'test' -H "x-ms-blob-type: BlockBlob" -H "x-ms-version: 2023-11-03" "https://<account-name>.blob.core.windows.net/<container>/test.txt"
```

The [Azure CLI](https://learn.microsoft.com/en-us/cli/azure/storage) (`az storage blob list`, `az storage blob upload`) or `az storage container show-permission` can be used where credentials are available (gray-box) to confirm the configured access level directly.

### Google Cloud Storage (GCS)

GCS objects are reachable through either the JSON API or the public `storage.googleapis.com` XML-style endpoint:

```text
https://storage.googleapis.com/<bucket-name>/<object-name>
```

To test public read access:

```bash
curl -X GET "https://storage.googleapis.com/<bucket-name>/<object-name>"
```

To test whether the bucket allows public, unauthenticated listing:

```bash
curl -X GET "https://storage.googleapis.com/storage/v1/b/<bucket-name>/o"
```

A `200` response with a JSON list of objects indicates public listing is enabled (commonly via an `allUsers`/`allAuthenticatedUsers` IAM binding or legacy ACL, rather than being GCS's default).

To test upload:

```bash
curl -X POST --data-binary @test.txt "https://storage.googleapis.com/upload/storage/v1/b/<bucket-name>/o?uploadType=media&name=test.txt"
```

Where credentials are available, [`gsutil`](https://cloud.google.com/storage/docs/gsutil) (`gsutil ls gs://<bucket>`, `gsutil iam get gs://<bucket>`) or the equivalent `gcloud storage` commands can confirm the configured IAM bindings and legacy ACLs directly.

### Amazon S3 Bucket Misconfiguration

The Amazon S3 bucket URLs follow one of two formats, either virtual host style or path-style.

- Virtual Hosted Style Access

```text
https://bucket-name.s3.Region.amazonaws.com/key-name
```

In the following example, `my-bucket` is the bucket name, `us-west-2` is the region, and `puppy.png` is the key-name:

```text
https://my-bucket.s3.us-west-2.amazonaws.com/puppy.png
```

- Path-Style Access

```text
https://s3.Region.amazonaws.com/bucket-name/key-name
```

As above, in the following example, `my-bucket` is the bucket name, `us-west-2` is the region, and `puppy.png` is the key-name:

```text
https://s3.us-west-2.amazonaws.com/my-bucket/puppy.png
```

For some regions, the legacy global endpoint that does not specify a region-specific endpoint can be used. Its format is also either virtual hosted style or path-style.

- Virtual Hosted Style Access

```text
https://bucket-name.s3.amazonaws.com
```

- Path-Style Access

```text
https://s3.amazonaws.com/bucket-name
```

#### Identify Bucket URL

For black-box testing, S3 URLs can be found in the HTTP messages. The following example shows a bucket URL is sent in the `img` tag in an HTTP response.

```html
...
<img src="https://my-bucket.s3.us-west-2.amazonaws.com/puppy.png">
...
```

For gray-box testing, you can obtain bucket URLs from Amazon's web interface, documents, source code, and any other available sources.

#### AWS-CLI

In addition to testing with curl, you can also test with the AWS command-line tool. In this case `s3://` URI scheme is used.

##### List

The following command lists all the objects of the bucket when it is configured public:

```bash
aws s3 ls s3://<bucket-name>
```

##### Upload

The following is the command to upload a file:

```bash
aws s3 cp arbitrary-file s3://bucket-name/path-to-save
```

This example shows the result when the upload has been successful.

```bash
$ aws s3 cp test.txt s3://bucket-name/test.txt
upload: ./test.txt to s3://bucket-name/test.txt
```

This example shows the result when the upload has failed.

```bash
$ aws s3 cp test.txt s3://bucket-name/test.txt
upload failed: ./test2.txt to s3://bucket-name/test2.txt An error occurred (AccessDenied) when calling the PutObject operation: Access Denied
```

##### Remove

The following is the command to remove an object:

```bash
aws s3 rm s3://bucket-name/object-to-remove
```

### ACL and IAM Policy Misconfigurations

Beyond a simple public/private toggle, all three providers support fine-grained access grants that are easy to over-scope:

- AWS S3: review bucket policies and ACLs for grants to `AllUsers`/`AuthenticatedUsers` (the S3 equivalent of "public"), and for bucket policies that grant broad `s3:*` or `s3:GetObject`/`s3:PutObject` to a wildcard principal (`"Principal": "*"`) or to another AWS account that shouldn't need access. Also confirm [S3 Block Public Access](https://docs.aws.amazon.com/AmazonS3/latest/userguide/access-control-block-public-access.html) is enabled at the account/bucket level unless explicitly required otherwise - it acts as a safety net even if an individual policy is misconfigured. `aws s3api get-bucket-acl` and `aws s3api get-bucket-policy` show the effective configuration in gray-box testing.
- Azure Blob Storage: review the container's public access level (`Private`/`Blob`/`Container`) as above, and separately review any Shared Access Signature (SAS) policies and RBAC role assignments (`Storage Blob Data Reader/Contributor`) scoped to the storage account for grants wider than needed.
- GCS: review IAM bindings (`gsutil iam get gs://<bucket>`) and any legacy per-object/per-bucket ACLs for `allUsers` (public) or `allAuthenticatedUsers` (any Google account, not just this application's users) bindings, since the latter is often mistaken for "still private" when it is not.

In all three cases, distinguish objects that are public by design (e.g. static site assets, public downloads) from configuration, backup, or user-data objects that ended up public unintentionally - the intent behind the object, not just its reachability, determines whether a finding is real.

### Signed/Presigned URL Weaknesses

Signed URLs (S3 presigned URLs, Azure SAS tokens, GCS signed URLs) let an application grant time-limited access to a private object without sharing full credentials. Review:

- Expiry: confirm the expiry set on the signed URL (`X-Amz-Expires` for S3, `se=` for Azure SAS, `Expires`/`X-Goog-Expires` for GCS) is as short as the use case allows - a signed URL with a multi-day or multi-year expiry is effectively a permanent credential if it leaks (e.g. via browser history, referrer headers, proxy/access logs, or being shared/forwarded).
- Scope: confirm the signature is scoped to only the specific object/action needed (e.g. GCS/S3 signatures can be scoped to a single object and a single HTTP method; Azure SAS tokens can be scoped to a whole account if generated as an account-level SAS rather than a service/container/blob-level SAS - check which level was used).
- Leakage and reuse: check whether signed URLs are logged in plaintext by intermediate proxies, CDNs, or application logs, and whether the same signed URL is reused across multiple users/sessions rather than generated per-request - a leaked URL is valid for anyone until it expires or is revoked, and most schemes have no way to revoke a single signed URL early short of rotating the underlying key/credential.
- Signature validation: as a basic tampering check, try modifying the object path or query parameters of a valid signed URL (e.g. pointing it at a different object while keeping the same signature) and confirm the request is rejected rather than served.

### Versioning and Lifecycle Issues

Object versioning (keeping prior versions of an object after it is overwritten or deleted) and lifecycle policies (rules that transition or expire objects over time) are commonly enabled for durability/compliance reasons, but can undermine an expectation that "deleted" data is actually gone:

- If versioning is enabled, confirm that a "deleted" object (e.g. one containing data that should be erased for compliance, or an old credential file that was rotated) is not still retrievable via a previous version ID. For S3: `aws s3api list-object-versions --bucket <bucket>`; for GCS: `gsutil ls -a gs://<bucket>/<object>`; for Azure: blob snapshots/versions via `az storage blob list --include v`.
- Confirm access-control settings apply consistently across versions - a bucket/container access-control fix applied after an incident may only affect the current version, leaving older versions of the same object reachable if versioned access is handled separately by the provider.
- Review lifecycle rules that transition objects to a different storage class/tier or a different bucket/account (e.g. archival tiers, cross-region replication) - confirm the destination has equivalent access controls, since a lifecycle transition can silently move sensitive data to a location that wasn't in scope for the original access-control review.
- Where an application relies on "delete" to remove sensitive data (e.g. for a user data-deletion request), confirm this results in actual removal (including all versions and any replicated/lifecycle-transitioned copies) rather than only removing the current version's accessibility.

## Tools

- [AWS CLI](https://aws.amazon.com/cli/)
- [Azure CLI](https://learn.microsoft.com/en-us/cli/azure/) / [Azure Storage Explorer](https://azure.microsoft.com/en-us/products/storage/storage-explorer)
- [gsutil](https://cloud.google.com/storage/docs/gsutil) / [gcloud storage](https://cloud.google.com/sdk/gcloud/reference/storage)
- [S3Scanner](https://github.com/sa7mon/S3Scanner) - bucket discovery and permission enumeration
- [cloud_enum](https://github.com/initstring/cloud_enum) - multi-cloud (AWS/Azure/GCP) storage enumeration
- [ScoutSuite](https://github.com/nccgroup/ScoutSuite) / [Prowler](https://github.com/prowler-cloud/prowler) - broader cloud security posture review, including storage ACL/IAM findings

## References

- [Working with Amazon S3 Buckets](https://docs.aws.amazon.com/AmazonS3/latest/dev/UsingBucket.html)
- [AWS: Blocking Public Access to Your S3 Storage](https://docs.aws.amazon.com/AmazonS3/latest/userguide/access-control-block-public-access.html)
- [Azure: Configure Anonymous Public Read Access for Containers and Blobs](https://learn.microsoft.com/en-us/azure/storage/blobs/anonymous-read-access-configure)
- [Azure: Grant Limited Access with Shared Access Signatures (SAS)](https://learn.microsoft.com/en-us/azure/storage/common/storage-sas-overview)
- [Google Cloud Storage: Access Control](https://cloud.google.com/storage/docs/access-control)
- [Google Cloud Storage: Signed URLs](https://cloud.google.com/storage/docs/access-control/signed-urls)
- [flAWS 2 - Learn AWS Security](http://flaws2.cloud)
- [curl Tutorial](https://curl.se/docs/manual.html)
