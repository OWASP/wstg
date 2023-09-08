# Vulnerability Naming Schemes

With a constantly growing number of IT assets to administer, security practitioners require new and more powerful tools to perform automated and large scale analysis. Thanks to software attention can be focused on the more creative and intellectually challenging problems. Unfortunately, having vulnerability assessment tools, antivirus software, and intrusion detection systems communicate its not an easy job. It has resulted in several technical complications, requiring a standardized way to identify each software flaw, vulnerability, or configuration issues identified. The lack of this interoperability capabilities can cause inconsistencies during the security assessment, confusing reporting, and extra correlation efforts among other problems that will produce an important waste of resources and time.

A naming scheme is a systematic methodology used to identify each one of those vulnerabilities in order to facilitate clear identification and information sharing. This goal is achieved by the definition of a unique, structured, and software-efficient name for each vulnerability. There are multiple schemes used to facilitate this effort, the most common are:

- Common Platform Enumeration (`CPE`)
- Software Identification Tag (`SWID`)
- Package URL (`PURL`)

## Software Identification Tag

Software Identification Tag (`SWID`) is an International Organization for Standardization's standard defined by the ISO/IEC 19770-2:2015. The `SWID` tags are used to identify each software clearly as part of comprehensive software asset management lifecycles. This information schema is recommended to be used by the National Institute of Standards and Technology (NIST) as the primary identification for any developed or installed software. From `SWID` it's possible to generate other schemas such as the `CPE` used by the National Vulnerability Database (NVD) whereas the reverse process is not possible.

Each `SWID` tag is represented as a standardized XML format. A `SWID` tag is composed for three groups of elements. The first block composed by 7 predefined elements required to be considered a valid tag. Followed by an optional block which provides a set of 30 possible predefined elements that the tag creator can use to provide reliable and detailed information. Finally, the `Extended` group of elements provides the opportunity for the tag creator to define any non predefined elements required to accurately define the described software. The high level of granularity provided by `SWID`, not only provides the capability to describe a given product of software, but also it's specific status on the software lifecycle.

### Examples

- _ACME Roadrunner Service Pack 1_ patch created by the ACME Corporation for the already installed product identified with the `@tagId`: _com.acme.rms-ce-v4-1-5-0_:

```xml
<SoftwareIdentity
                  xmlns="http://standards.iso.org/iso/19770/-2/2015/schema.xsd"
                  name="ACME Roadrunner Service Pack 1"
                  tagId="com.acme.rms-ce-sp1-v1-0-0"
                  patch="true"
                  version="1.0.0">
  <Entity
          name="The ACME Corporation"
          regid="acme.com"
          role="tagCreator softwareCreator"/>
  <Link
        rel="patches"
        href="swid:com.acme.rms-ce-v4-1-5-0">
    ...
</SoftwareIdentity>
```

- Red Hat Enterprise Linux version 8 for x86-64 architecture:

```xml
<SoftwareIdentity
                  xmlns="http://standards.iso.org/iso/19770/-2/2015/schema.xsd"
                  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                  xsi:schemaLocation="http://standards.iso.org/iso/19770/-2/2015/schema.xsd"
                  xml:lang="en-US"
                  name="Red Hat Enterprise Linux"
                  tagId="com.redhat.RHEL-8-x86_64"
                  tagVersion="1"
                  version="8"
                  versionScheme="multipartnumeric"
                  media="(OS:linux)">
```

## Common Platform Enumeration

The Common Platform Enumeration scheme (`CPE`) is a structured naming scheme for information technology systems, software, and packages maintained by `NVD`. Commonly used in conjunction with the Common Vulnerabilities and Exposures identification codes (e.g. `CVE-2017-0147`). Despite being considered a deprecated scheme superseded by `SWID`, `CPE` is still widely used by several security solutions.

Defined as a Dictionary of registered values provided by `NVD`. Each `CPE` code can be defined as a well-formatted name or as a URL. Each value MUST follow this structure:

- _cpe-name_ = "cpe:" component-list
- _component-list_ = part ":" vendor ":" product ":" version ":" update ":" edition ":" lang
- _component-list_ = part ":" vendor ":" product ":" version ":" update ":" edition
- _component-list_ = part ":" vendor ":" product ":" version ":" update
- _component-list_ = part ":" vendor ":" product ":" version
- _component-list_ = part ":" vendor ":" product
- _component-list_ = part ":" vendor
- _component-list_ = part
- _component-list_ = empty
- _part_ = "h" / "o" / "a" = string
- _vendor_ = string
- _product_ = string
- _version_ = string
- _update_ = string
- _edition_ = string
- _lang_ LANGTAG / empty
- _string_ = *( unreserved / pct-encoded )
- _empty_ = ""
- _unreserved_ = ALPHA / DIGIT / "-" / "." / "_" / " ̃"
- _pct-encoded_ = "%" HEXDIG HEXDIG
- _ALPHA_ = %x41-5a / %x61-7a ; A-Z or a-z
- _DIGIT_ = %x30-39 ; 0-9
- _HEXDIG_ = DIGIT / "a" / "b" / "c" / "d" / "e" / "f"
- _LANGTAG_ = cf. [RFC5646]

### Examples

- Microsoft Internet Explorer 8.0.6001 Beta (any edition): `wfn:[part="a",vendor="microsoft",product="internet_explorer", version="8\.0\.6001",update="beta",edition=ANY]` which binds to the following URL: `cpe:/a:microsoft:internet_explorer:8.0.6001:beta`.
- Foo\Bar Big$Money Manager 2010 Special Edition for iPod Touch 80GB: `wfn:[part="a",vendor="foo\\bar",product="big\$money_manager_2010", sw_edition="special",target_sw="ipod_touch",target_hw="80gb"]`, which binds to the following URL:`cpe:/a:foo%5cbar:big%24money_manager_2010:::~~special~ipod_touch~80gb~`.

## Package URL

Package URL standardizes how software package metadata is represented so that packages can be universally located regardless of what vendor, project, or ecosystem the packages belongs.

A PURL is a valid `RFC3986` ASCII string defined URL composed of seven elements. Each of them is separated by a defined character in order to make it easily manipulated by software.

`scheme:type/namespace/name@version?qualifiers#subpath`

The definition for each component is:

- _scheme_: URL scheme compliant constant value of "pkg". (**Required**).
- _type_: package type or package protocol such as maven, npm, nuget, gem, pypi, etc. (**Required**).
- _namespace_: type-specific value to a package prefix such as it's owner name, groupid, etc. (Optional).
- _name_: name of the package. (**Required**).
- _version_: package version. (Optional).
- _qualifiers_: extra qualifying data for a package such as an OS, architecture, a distro, etc. (Optional).
- _subpath_: extra subpath within a package, relative to the package root. (Optional).

### Examples

- Curl software, packaged as a `.deb` package for Debian Jessie meant for an i386 architecture: `pkg:deb/debian/curl@7.50.3-1?arch=i386&distro=jessie`
- Docker image of Apache Casandra signed with the SHA256 hash 244fd47e07d1004f0aed9c: `pkg:docker/cassandra@sha256:244fd47e07d1004f0aed9c`

## Recommendation Uses

| USE  | RECOMMENDATION  |
|---|---|
| Client or Server Application | CPE or SWID |
| Container | PURL or SWID |
| Firmware | CPE or SWID* |
| Library or Framework (package) | PURL |
| Library or Framework (non-package) | SWID |
| Operating System | CPE or SWID |
| Operating System Package | PURL or SWID |

> Note: Due to the deprecated status of `CPE`, industry recommended seems to be that new projects implement `SWID` when they need to decide between the two methods. Even though `CPE` is known to be a widely used naming schema within current active projects and solutions.

## References

- [NISTIR 8060 - Guidelines for the Creation of Interoperable Software Identification (SWID) Tags (PDF)](https://nvlpubs.nist.gov/nistpubs/ir/2016/NIST.IR.8060.pdf)
- [NISTIR 8085 - Forming Common Platform Enumeration (CPE) Names from Software Identification (SWID) Tags](https://csrc.nist.gov/CSRC/media/Publications/nistir/8085/draft/documents/nistir_8085_draft.pdf)
- [ISO/IEC 19770-2:2015 - Information technology— Software asset management—Part2:Software identification tag](https://www.iso.org/standard/65666.html)
- [Official Common Platform Enumeration (CPE) Dictionary](https://nvd.nist.gov/products/cpe)
- [Common Platform Enumeration: Dictionary Specification Version 2.3](https://csrc.nist.gov/publications/detail/nistir/7697/final)
- [PURL Specification](https://github.com/package-url/purl-spec)

### Known Implementations

- [packageurl-go](https://github.com/package-url/packageurl-go)
- [packageurl-dotnet](https://github.com/package-url/packageurl-dotnet)
- [packageurl-java](https://github.com/package-url/packageurl-java), [package-url-java](https://github.com/sonatype/package-url-java)
- [packageurl-python](https://github.com/package-url/packageurl-python)
- [packageurl-rust](https://github.com/package-url/packageurl.rs)
- [packageurl-js](https://github.com/package-url/packageurl-js)
