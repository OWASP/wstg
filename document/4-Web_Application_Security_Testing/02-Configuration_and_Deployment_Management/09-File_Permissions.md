# File Permissions

|ID          |
|------------|
|WSTG-CONF-09|

## Summary

When a resource is given a permissions setting that provides access to a wider range of actors than required, it could lead to the exposure of sensitive information, or the modification of that resource by unintended parties. This is especially dangerous when the resource is related to program configuration, execution, or sensitive user data.

A clear example would be an executable file that can be run by unauthorized users. For another example, consider account information or a token value used to access an API. These are increasingly seen in modern web services and microservices, and may be stored in a configuration file that has world-readable permissions by default upon installation. Such sensitive data could be exposed either by malicious internal actors within the host system or by remote attackers. The latter may have compromised the service through other vulnerabilities, while gaining only normal user privileges.

## Test Objectives

- Review and identify any rogue file permissions on the host filesystem, in container images/filesystems, and on cloud storage objects.
- Assess whether Kubernetes volume mounts and `securityContext` settings enforce least-privilege access to files and secrets.
- Identify secrets stored with overly broad permissions, wherever they are held (filesystem, container image, orchestration secret store, cloud secrets manager export, CI artifacts).

## How to Test

### Traditional OS/Filesystem Permissions

In Linux, use `ls` command to check the file permissions. Alternatively, `namei` can also be used to recursively list file permissions.

`$ namei -l /PathToCheck/`

The files and directories that require file permission testing can include, but are not limited to, the following:

- Web files/directory
- Configuration files/directory
- Sensitive files(encrypted data, password, key)/directory
- Log files(security logs, operation logs, admin logs)/directory
- Executables(scripts, EXE, JAR, class, PHP, ASP)/directory
- Database files/directory
- Temp files/directory
- Upload files/directory

### Container Filesystem Permissions

Container images frequently bake in overly broad permissions on files that end up owned by root or world-writable/readable inside the running container:

- Inspect the image build for permission-widening instructions: `docker history --no-trunc <image>` and review the `Dockerfile` for `COPY`/`ADD` without a following `chmod`/`chown`, or `RUN chmod -R 777 ...` used to work around permission errors.
- From a running container (or `docker exec`), check for world-writable files outside of expected temp paths: `find / -perm -0002 -type f 2>/dev/null`. Omit `-xdev` here, unlike on a host scan, since sensitive files are often on a mounted volume/PVC rather than the container's own root filesystem. A mounted volume's permissions are set by the host or orchestrator at mount time and can differ from, and override, whatever the image's own layers specify for that path, so the two need to be checked separately: image-layer permissions via `docker history`/layer inspection (see above), and mounted-volume permissions via this `find` run against the live container.
- Check whether the container runs as root by default (`docker inspect --format '{{.Config.User}}' <image>` empty or `0` means root) - a root process combined with a writable bind-mounted host path is a common escalation route.
- Check secrets or config baked into image layers with permissive modes: `docker history` plus extracting layers (e.g. via `dive` or `docker save` + `tar`) to confirm files like `/app/.env` or key material are not `644`/`666` when they should be `600` and root-only.

### Kubernetes Volume Mounts and securityContext

- Review Pod/Deployment specs for `securityContext.fsGroup`, `runAsUser`, `runAsNonRoot`, and `readOnlyRootFilesystem` - absence of these often means volumes and the root filesystem are writable by more processes/users than necessary.
- Check mounted `Secret` and `ConfigMap` volumes for an explicit `defaultMode` (octal file mode); the Kubernetes default (`0644`) makes secret files group/world-readable inside the pod. Confirm sensitive mounts set a tighter mode (e.g. `0400` or `0440`) via `defaultMode` or per-item `mode`.
- For `hostPath` volumes, confirm the mounted host directory's own permissions and that the container's UID/GID (from `securityContext`) does not grant broader access than intended on the host.
- Review `automountServiceAccountToken` and whether the projected service-account token volume is more widely readable/mountable than needed by the workload.
- `kubectl auth can-i --list --as=system:serviceaccount:<ns>:<sa>` helps confirm the effective access tied to a pod's identity is not broader than the file/volume permissions imply.

#### SecurityContext and Container-Hardening Checklist

The fields above are the permission-specific subset of a broader `securityContext`/container-hardening review. The following checklist covers the fields most often left at their insecure default, for use as a compact reference across container and Kubernetes testing in this section and in [Application Platform Configuration](02-Application_Platform_Configuration.md#container-images):

| Field/setting | Insecure default | What to check |
|---|---|---|
| `runAsNonRoot` / container `USER` | Unset; container runs as root (UID 0) | Pod spec `securityContext.runAsNonRoot: true` and `runAsUser` set to a non-zero UID, or `docker inspect --format '{{.Config.User}}' <image>` non-empty and non-zero. |
| `readOnlyRootFilesystem` | Unset; root filesystem writable | Pod spec sets `readOnlyRootFilesystem: true`, with any paths the process genuinely needs to write mounted as separate volumes. |
| `allowPrivilegeEscalation` | Unset; defaults to allowing escalation | Pod spec sets `allowPrivilegeEscalation: false`. |
| `privileged` | Unset; container is not privileged by default, but check explicit opt-in | Confirm `privileged: true` is not set except where genuinely required (rare for application workloads). |
| Linux capabilities | Container keeps the full default capability set | Pod spec `capabilities.drop: ["ALL"]`, with only the specific capabilities the workload needs re-added via `capabilities.add`. |
| `seccompProfile` | Unset on older clusters; unconfined | Pod or container `securityContext.seccompProfile.type: RuntimeDefault` (or a stricter custom profile). |
| Host namespaces (`hostNetwork`, `hostPID`, `hostIPC`) | Unset; namespaces are isolated by default, but check explicit opt-in | Confirm none of these are set to `true` unless the workload genuinely needs host-level access. |
| Volume `defaultMode` / image layer permissions | Covered above under filesystem and volume permissions | See [Container Filesystem Permissions](#container-filesystem-permissions) and [Kubernetes Volume Mounts and securityContext](#kubernetes-volume-mounts-and-securitycontext) above. |

As with the other checks in this document, treat a missing/insecure setting as a candidate finding to confirm against the workload's actual behavior (for example, an unnecessary capability that the running process doesn't actually use is still worth flagging, but demonstrating it is exploitable, such as via a container breakout using a retained capability, is a stronger finding than the configuration observation alone).

### Cloud Object ACLs and IAM

Cloud storage misconfigurations are a direct analogue of file permissions and should be tested the same way:

- AWS S3: check bucket and object ACLs and bucket policies for public or overly broad grants: `aws s3api get-bucket-acl --bucket <name>`, `aws s3api get-bucket-policy --bucket <name>`, and confirm S3 Block Public Access settings are enabled unless explicitly required otherwise.
- Azure Blob Storage: check container public access level (`Private`/`Blob`/`Container`) and any SAS tokens with excessive scope or long expiry: `az storage container show-permission`.
- GCP Cloud Storage: check bucket/object IAM bindings and legacy ACLs for `allUsers`/`allAuthenticatedUsers`: `gsutil iam get gs://<bucket>`.
- In all cases, distinguish "publicly readable by design" (e.g. static site assets) from unintended exposure of configuration, backups, or credentials - the same distinction as file-permission review on a filesystem.

### Secrets Stored With Overly Broad Permissions

Regardless of where secrets live (filesystem, container image, Kubernetes `Secret`, cloud secrets manager export, CI artifact), verify:

- File-based secrets (`.env`, private keys, service-account JSON, kubeconfig) are not group/world-readable (`600`/`400` and owned by the intended user/service account only).
- Secrets are not committed into container image layers or accessible via `docker history`/layer inspection even if removed in a later layer.
- Secrets pulled into CI build artifacts or logs do not end up in world-readable build caches or artifact storage with default (often permissive) ACLs.

## Remediation

- Set the permissions of files and directories properly so that unauthorized users cannot access critical resources, applying least privilege on the host, in container images, and at the orchestration layer.
- In containers, avoid running as root and avoid `chmod -R 777`/similar broad-permission workarounds; fix the underlying ownership/UID mismatch instead.
- In Kubernetes, set `securityContext` (`runAsNonRoot`, `readOnlyRootFilesystem`, `fsGroup`) and a restrictive `defaultMode` on `Secret`/`ConfigMap` volumes.
- In cloud storage, enable public-access blocking by default and grant access via scoped IAM roles/policies rather than broad ACLs or long-lived, wide-scope SAS tokens.

## Tools

- [Windows AccessEnum](https://technet.microsoft.com/en-us/sysinternals/accessenum)
- [Windows AccessChk](https://technet.microsoft.com/en-us/sysinternals/accesschk)
- [Linux namei](https://linux.die.net/man/1/namei)
- [dive - Docker image layer/permission explorer](https://github.com/wagoodman/dive)
- [kube-bench - CIS Kubernetes Benchmark scanner](https://github.com/aquasecurity/kube-bench)
- [ScoutSuite - Multi-cloud security auditing (AWS/Azure/GCP)](https://github.com/nccgroup/ScoutSuite)
- [Prowler - AWS/Azure/GCP security assessment](https://github.com/prowler-cloud/prowler)

## References

- [CWE-732: Incorrect Permission Assignment for Critical Resource](https://cwe.mitre.org/data/definitions/732.html)
- [Kubernetes: Configure a Security Context for a Pod or Container](https://kubernetes.io/docs/tasks/configure-pod-container/security-context/)
- [Kubernetes: Secrets - defaultMode](https://kubernetes.io/docs/concepts/configuration/secret/#secret-files-permissions)
- [AWS: Blocking public access to your S3 storage](https://docs.aws.amazon.com/AmazonS3/latest/userguide/access-control-block-public-access.html)
- [CIS Docker Benchmark](https://www.cisecurity.org/benchmark/docker)
