# Application Platform Configuration

|ID          |
|------------|
|WSTG-CONF-02|

## Summary

Proper configuration of the single elements that make up an application architecture is important in order to prevent mistakes that might compromise the security of the whole architecture.

Reviewing and testing configurations are critical tasks in creating and maintaining an architecture. This is because various systems often come with generic configurations, which may not align well with the tasks they're supposed to perform on the specific sites where they're installed.

While the typical web and application server installation will contain a lot of functionality (like application examples, documentation, test pages), what is not essential should be removed before deployment to avoid post-install exploitation.

## Test Objectives

- Ensure that default, sample, and known files have been removed from the deployed platform, container image, or serverless package.
- Validate that no debugging code, debug endpoints, debug modes, or unused modules/dependencies are left enabled in production environments.
- Review the logging mechanisms set in place for the application, including what sensitive data may be captured and who/what can access or retain it.
- Confirm framework-, container-, and serverless-specific production hardening settings are applied rather than left at insecure defaults.

## How to Test

### Black-Box Testing

#### Sample and Known Files and Directories

In a default installation, many web servers, application servers, and frameworks provide sample applications, scaffolding, and test pages for the benefit of the developer, so they can confirm the server is working right after install or `init`. Historically this class of issue was exemplified by cases such as CVE-1999-0449 (Denial of Service in IIS when the Exair sample site had been installed), CAN-2002-1744 (Directory traversal vulnerability in CodeBrws.asp in Microsoft IIS 5.0), or CAN-2003-1172 (Directory traversal in the view-source sample in Apache's Cocoon) - the underlying problem (unremoved sample/scaffold content shipping to production) is unchanged today, just with different targets:

- Framework scaffolding left in place: default Django/Rails/Laravel welcome pages, default Spring Boot error/whitelabel pages, create-react-app/Next.js/Vite default landing pages, or an unmodified `index.html` from a starter template - each can leak the exact framework/version in use, and sometimes leftover scaffold routes.
- Auto-generated API documentation/consoles left reachable in production: Swagger UI/OpenAPI (`/swagger-ui`, `/swagger.json`, `/v2/api-docs`), GraphQL Playground/GraphiQL, or gRPC reflection - these often expose the full schema, including undocumented or admin-only operations, and some allow direct request execution ("try it out") without additional authorization checks.
- Legacy sample-file classes: `phpinfo.php`, `test.php`, `info.php`, default CMS install/setup scripts (e.g. `wp-admin/install.php`, Joomla `installation/`) left reachable after go-live.

CGI/web scanners with a database of known sample files and directories are a fast way to check for these; automated discovery should be followed by manual review of the site to catch framework-specific scaffolding that generic scanners don't fingerprint.

#### Debug Endpoints and Debug Modes

Most modern frameworks ship a debug/development mode that is explicitly unsafe for production, since it is designed to give the developer maximum visibility (full stack traces, in-browser code execution, environment variable dumps) at the cost of exposing exactly the same information to an attacker if left enabled:

- Django: `DEBUG=True` renders full stack traces, local variable values, and the list of installed apps/settings on any unhandled exception. Trigger an error (e.g. request a non-existent path or malformed input) and check the response for a Django debug page rather than a generic 404/500.
- Flask/Werkzeug: the Werkzeug debugger, if enabled (`app.run(debug=True)` or `FLASK_DEBUG=1`), exposes an in-browser Python console on unhandled exceptions. Although nominally PIN-protected, the PIN can often be derived from information also present in the error page or the host's own predictable values in older Werkzeug versions - treat any reachable Werkzeug debugger in production as a critical finding (remote code execution), not just an information leak.
- Spring Boot Actuator: endpoints such as `/actuator/env`, `/actuator/heapdump`, `/actuator/httptrace`, and `/actuator/mappings` can expose environment variables/secrets, a full heap dump (which may contain credentials and session data), and internal routing - check whether Actuator endpoints are reachable at all in production, and if so, whether `management.endpoints.web.exposure.include` has been scoped down from an overly broad default.
- Rails: `config.consider_all_requests_local = true` (default in development) renders detailed error pages with source snippets and request/session data; confirm this is `false` in the production environment config.
- Express/Node.js: default error handlers that echo `err.stack` to the client, or leaving a framework's built-in dev middleware (e.g. bundler dev-server middleware) mounted in a production build.
- Next.js/React and other SPA build tooling: production builds that still ship JavaScript source maps (`.map` files) or leave a dev server reachable, both of which can reconstruct original source from minified bundles.
- GraphQL introspection: even without a Playground UI, the introspection query (`{ __schema { types { name } } }`) being answered in production reveals the full schema, including fields/mutations not exposed in the documented API surface.

As a general test: deliberately trigger an application error (malformed input, missing parameter, forced exception) on each distinct component/framework in use, and confirm the response is a generic, non-revealing error rather than a framework debug page.

#### Comment Review

It is very common for programmers to add comments when developing large web-based applications. However, comments included inline in HTML code might reveal internal information that should not be available to an attacker. Sometimes, a part of the source code is commented out when a functionality is no longer required, but this comment is unintentionally leaked out to the HTML pages returned to the users.

Comment review should be done in order to determine if any information is being leaked through comments. This review can only be thoroughly done through an analysis of the web server's static and dynamic content, and through file searches. It can be useful to browse the site in an automatic or guided fashion, and store all the retrieved content. This retrieved content can then be searched in order to analyse any HTML comments available in the code.

#### System Configuration

Various tools, documents, or checklists can be used to give IT and security professionals a detailed assessment of the target systems' conformance to various configuration baselines or benchmarks. Such tools include, but are not limited to, the following:

- [CIS-CAT Lite](https://www.cisecurity.org/blog/introducing-cis-cat-lite/)
- [Microsoft's Attack Surface Analyzer](https://github.com/microsoft/AttackSurfaceAnalyzer)
- [NIST's National Checklist Program](https://nvd.nist.gov/ncp/repository)

### Gray-Box Testing

#### Configuration Review

The web server or application server configuration takes an important role in protecting the contents of the site and it must be carefully reviewed in order to spot common configuration mistakes. Obviously, the recommended configuration varies depending on the site policy, and the functionality that should be provided by the server software. In most cases, however, configuration guidelines (either provided by the software vendor or external parties) should be followed to determine if the server has been properly secured.

It is impossible to generically say how a server should be configured, however, some common guidelines should be taken into account:

- Only enable server modules (ISAPI extensions in the case of IIS) that are needed for the application. This reduces the attack surface since the server is reduced in size and complexity as software modules are disabled. It also prevents vulnerabilities that might appear in the vendor software from affecting the site if they are only present in modules that have been already disabled. The same principle applies to modern middleware/module stacks: review web server modules (Apache/Nginx modules, IIS modules), application framework middleware, and installed package/dependency lists (`npm ls`, `pip list`, etc.) for anything included by a default template but not actually used - an unused dependency is still an attack surface and a patching burden even if never invoked by application code.
- Handle server errors (40x or 50x) with custom-made pages instead of with the default web server pages. Specifically make sure that any application errors will not be returned to the end user and that no code is leaked through these errors since it will help an attacker. It is actually very common to forget this point since developers do need this information in pre-production environments.
- Make sure that the server software runs with minimized privileges in the operating system. This prevents an error in the server software from directly compromising the whole system, although an attacker could elevate privileges once running code as the web server.
- Make sure the server software properly logs both legitimate access and errors.
- Make sure that the server is configured to properly handle overloads and prevent Denial of Service attacks. Ensure that the server has been performance-tuned properly.
- Never grant non-administrative identities (with the exception of `NT SERVICE\WMSvc`) access to applicationHost.config, redirection.config, and administration.config (either Read or Write access).
- Never share out applicationHost.config, redirection.config, and administration.config on the network.
- Do not store sensitive information in readable configuration files.
- Encrypt sensitive configuration data where required.
- Restrict access to shared configuration and protect it appropriately.

#### Logging

Logging is an important part of application security. It supports monitoring, incident response, and investigations. Review both platform and application logging to determine whether security-relevant events are recorded, whether the records are useful, and whether the logging process introduces additional risk.

During the review, verify the following:

- Security-relevant events are logged (authentication, authorization failures, admin actions, input validation failures).
- Log entries contain enough context to support investigation.
- Sensitive data in logs: check that logs do not capture passwords, tokens/API keys, session identifiers, full payment card numbers, or other regulated personal data - a surprisingly common source of this is verbose/debug-level logging left enabled in production (e.g. a framework logging full request/response bodies, or a library logging exception objects that include credentials passed as arguments), and third-party error-tracking/APM integrations forwarding raw request data (headers, bodies) off-host by default.
- Logged data is handled safely before storage and display (e.g. log entries are not later rendered unescaped in a log-viewer UI, which can enable stored XSS via log injection).
- Log access: restricted to authorized personnel/services - check both the log files/streams themselves (file permissions, see [File Permissions](09-File_Permissions.md)) and any centralized logging platform (SIEM, cloud logging service) for overly broad read access or lack of per-tenant isolation in multi-tenant systems.
- Retention: confirm a defined retention period exists and is enforced (both "logs kept too briefly to investigate an incident" and "logs kept indefinitely, becoming a growing repository of sensitive data" are findings worth raising).
- Logs are protected against tampering (append-only/write-once storage or equivalent integrity controls where feasible).
- Logging failures do not expose sensitive debugging information to the end user (a logging subsystem failure should not fall back to displaying the unlogged error directly in the response).
- Logs can be centralized or correlated in distributed environments (containers, serverless functions, and load-balanced nodes each need a consistent way to correlate a single request/trace across components - verify this exists rather than each component logging in isolation with no shared request/trace ID).

Testing should confirm that logs are usable, consistent, and effectively support detection and response activities, without themselves becoming a source of sensitive data exposure.

#### Container Images

Where the application is deployed as a container image, the same "remove what isn't needed" principle from traditional server hardening applies to what gets baked into the image. Most of these checks require the image itself (gray-box); the exceptions are noted.

- Review the `Dockerfile`/image build for leftover default/sample files, build-time secrets (API keys or credentials passed as build args and left in an intermediate layer even if removed from the final layer), and unnecessary build tooling (compilers, package manager caches, shells) that a multi-stage build should have left behind in the build stage. Gray-box: run `docker history --no-trunc <image>` or a layer-inspection tool (e.g. `dive`) against the actual image; a finding requires the secret/tooling to be visible in a retained layer, not just suspected from the `Dockerfile` source.
- Prefer minimal base images (slim/distroless/scratch-based) for the final runtime layer. Gray-box: compare the base image named in the final stage of the `Dockerfile` against the image's actual installed package list (`docker run --rm <image> sh -c "..."` where a shell exists, or layer inspection where it doesn't).
- Confirm debug/development-mode environment variables are not set as image defaults (e.g. `ENV FLASK_DEBUG=1`, `ENV NODE_ENV=development`). Black-box: trigger an application error against the running container and check for a debug page/stack trace (same test as [Debug Endpoints and Debug Modes](#debug-endpoints-and-debug-modes) above) - this is the evidence that the default actually took effect at runtime, since an orchestration-layer override could have corrected an insecure image default. Gray-box: confirm via `docker inspect --format '{{.Config.Env}}' <image>` that the image-level default is itself safe, independent of any override.
- Confirm the container does not run as root by default and that the image does not embed `.git`, `.env`, or other sensitive files copied in via a broad `COPY . .` without a corresponding `.dockerignore`. Gray-box: `docker inspect --format '{{.Config.User}}' <image>` (empty or `0` means root) and a layer/filesystem inspection for the unwanted files.

Example finding: `docker history --no-trunc` on a published image shows a build layer with `RUN echo $DB_PASSWORD > /tmp/debug.log`, leaking the production database password to anyone who can pull the image, even though the final layer no longer contains the file - the evidence is the value visible in that layer's history, not merely that a `Dockerfile` uses a build arg named similarly.

#### Serverless Runtimes

Serverless functions (AWS Lambda, Azure Functions, Google Cloud Functions/Cloud Run functions) shift where configuration mistakes show up, but the same categories of misconfiguration apply. Provider consoles and CLIs differ (AWS, Azure, and GCP each expose this configuration differently); adapt the specific command/console path to the actual provider in scope rather than assuming one is universal.

- Default/sample code: confirm scaffold code generated by `sam init`/`serverless create`/equivalent templates (sample handlers, example event payloads) has been removed rather than deployed alongside the real function. Black-box: invoke any discovered sample-handler routes/paths and confirm they return application data or an error, not scaffold placeholder output.
- Debug/verbose logging and error responses: many serverless frameworks log the full event payload or return a full stack trace in the HTTP response by default in local/dev mode. Black-box: trigger an application error via the function's public entry point and check the HTTP response for a stack trace. Gray-box: review the function's logs (e.g. CloudWatch Logs) for full request/response bodies being captured, per the sensitive-data-in-logs guidance above.
- Overly broad IAM/execution-role permissions: a function's execution role should be scoped to only the resources/actions it needs. Gray-box only in most engagements: read the execution role's attached policy (e.g. `aws iam get-role-policy`) and compare its granted actions/resources against what the function's code actually calls. Where a code-execution or injection bug in the function is independently confirmed, black-box evidence (successfully reading/writing a resource the intended scope shouldn't allow) upgrades this from a configuration observation to a demonstrated finding.
- Environment variables for secrets: confirm secrets are pulled from a secrets manager/parameter store at runtime rather than stored in plaintext function configuration. Gray-box: read the function's configured environment variables via the provider console/CLI and check whether values look like raw secrets versus a reference (ARN/resource ID) to a secrets manager entry.
- Test/invoke consoles: confirm the console-native "test invoke" feature is gated by the same access control as the console/account itself, and that no companion HTTP test endpoint has been left publicly invokable. Black-box: attempt to reach any discovered test/invoke HTTP path directly.

Example finding: a function's execution role is granted `s3:*` on all buckets instead of `s3:GetObject` on one (confirmed gray-box via the role's IAM policy), and a path-traversal bug independently found in the function's own code (confirmed black-box) is used to read/write an unrelated bucket, demonstrating that a contained bug became an account-wide S3 read/write vulnerability because of the over-scoped role.

#### Framework-Specific Production Hardening

Confirm each framework in use has its documented production-hardening settings applied, not just its defaults left in place. The table below gives one representative setting per framework as a starting probe, not a complete hardening test or a checklist to satisfy and stop - the exact name, default, and even availability of a setting can change between major versions of the same framework, and a deployment can still be insecure with every listed setting "correct" if something else in the same framework's checklist was missed.

| Framework | Representative setting to probe |
|-----------|---------------------|
| Django | `DEBUG = False`, `ALLOWED_HOSTS` restricted to real hostnames |
| Flask | `FLASK_DEBUG=0` / `debug=False`, `app.config['ENV'] = 'production'` |
| Ruby on Rails | `RAILS_ENV=production`, `config.consider_all_requests_local = false` |
| Spring Boot | `management.endpoints.web.exposure.include` restricted to what's needed; `server.error.include-stacktrace=never` |
| Express/Node.js | `NODE_ENV=production` (many middleware libraries change behavior, including error verbosity, based on this) |
| Next.js/other SPA frameworks | production build (not dev server) served, source maps excluded or access-restricted |

For each framework in scope:

- Treat the table entry as one representative check to orient the test, not proof the deployment is hardened; work through that framework's current official production-deployment checklist (linked under References) for the complete set.
- Verify the effective runtime configuration, not just the source configuration file: an environment variable, command-line flag, or orchestration-layer override (container env, Kubernetes ConfigMap/Secret, PaaS dashboard setting) can change the value actually in effect at runtime even when the checked-in file looks correct. Confirm via the running application's behavior (e.g. does it emit a debug page on error? does it expose the endpoint?) wherever feasible, rather than only via static file review.
- Do not infer that one correct setting implies the framework is otherwise hardened; unrelated settings from the same checklist can still be missing.

## References

- Apache
    - [Apache HTTP Server Documentation](https://httpd.apache.org/docs/current/)
    - [Performance Tuning](https://httpd.apache.org/docs/current/misc/perf-tuning.html)
- Microsoft IIS
    - [Secure and Harden Internet Information Services](https://learn.microsoft.com/en-us/training/modules/secure-harden-internet-information-services/)
    - [CIS Microsoft IIS Benchmarks](https://www.cisecurity.org/benchmark/microsoft_iis/)
- General
    - [Logging Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html), OWASP
    - [SP 800-92](https://csrc.nist.gov/publications/detail/sp/800-92/final) Guide to Computer Security Log Management, NIST
    - [PCI DSS](https://www.pcisecuritystandards.org/document_library) Requirement 10, PCI Security Standards Council
    - [CERT Security Improvement Modules: Securing Public Web Servers](https://resources.sei.cmu.edu/asset_files/SecurityImprovementModule/2000_006_001_13637.pdf)
- Containers and Serverless
    - [CIS Docker Benchmark](https://www.cisecurity.org/benchmark/docker)
    - [OWASP Serverless Top 10](https://owasp.org/www-project-serverless-top-10/)
    - [AWS Lambda Security Best Practices](https://docs.aws.amazon.com/lambda/latest/dg/security-best-practices.html)
- Framework Production Hardening
    - [Django Deployment Checklist](https://docs.djangoproject.com/en/stable/howto/deployment/checklist/)
    - [Flask Deployment Options](https://flask.palletsprojects.com/en/stable/deploying/)
    - [Ruby on Rails Security Guide](https://guides.rubyonrails.org/security.html)
    - [Spring Boot Actuator - Production Ready Features](https://docs.spring.io/spring-boot/reference/actuator/index.html)
