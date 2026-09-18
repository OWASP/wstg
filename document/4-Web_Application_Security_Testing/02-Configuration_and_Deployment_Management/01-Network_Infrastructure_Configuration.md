# Network Infrastructure Configuration

|ID          |
|------------|
|WSTG-CONF-01|

## Summary

A web application's infrastructure - web/application servers, databases, authentication servers, load balancers/CDNs, and (in modern deployments) cloud network controls and container/orchestration layers - is only as secure as its weakest, most poorly configured element. A single unreviewed or vulnerable component can compromise the application itself, even if the application's own code is sound; for example, a web server flaw disclosing source code hands an attacker information to attack the application directly.

After mapping the infrastructure (see [Map Network and Application Architecture](../01-Information_Gathering/10-Map_Application_Architecture.md)), testing should:

- Identify every element and how it affects the application's security.
- Review each element for known vulnerabilities.
- Review the administrative tools used to maintain them.
- Review authentication systems for manipulation by external users.
- Maintain and check against a change-controlled list of ports required by the application.

## Test Objectives

- Review the applications' configurations set across the network and validate that they are not vulnerable.
- Validate that used frameworks and systems are secure and not susceptible to known vulnerabilities due to unmaintained software or default settings and credentials.
- Where the infrastructure is cloud-hosted or containerized, review network isolation controls (security groups/NSGs, VPC/subnet layout, load balancer/CDN configuration, service mesh policies, Kubernetes `NetworkPolicy`) for unintended exposure or overly permissive rules.

## How to Test

### Known Server Vulnerabilities

Vulnerabilities in various areas of the application architecture, whether in the web server or the backend database, can severely compromise the application. For example, consider a server vulnerability that allows a remote, unauthenticated user to upload files to the web server or even replace existing files. This vulnerability could compromise the application, since a rogue user may be able to replace the application itself or introduce code that would affect the backend servers, as its application code would be run just like any other application.

Reviewing server vulnerabilities can be hard to do if the test needs to be done through a blind penetration test. In these cases, vulnerabilities need to be tested from a remote site, typically using an automated tool. However, testing for some vulnerabilities can have unpredictable results on the web server, and testing for others (like those directly involved in denial of service attacks) might not be possible due to the service downtime involved if the test was successful.

Some automated tools will flag vulnerabilities depending on the version of the web server they retrieve. This leads to both false positives and false negatives. On one hand, if the web server version has been removed or obscured by the local site administrator the scan tool will not flag the server as vulnerable even if it is. On the other hand, if the vendor providing the software does not update the web server version when vulnerabilities are fixed, the scan tool will flag vulnerabilities that do not exist. The latter case is actually very common as some operating system vendors back port patches of security vulnerabilities to the software they provide in the operating system, but do not do a full upload to the latest software version. This happens in most GNU/Linux distributions such as Debian, Red Hat, and SuSE. In most cases, vulnerability scanning of an application architecture will only find vulnerabilities associated with the "exposed" elements of the architecture (such as the web server) and will usually be unable to find vulnerabilities associated to elements which are not directly exposed, such as the authentication backend, the backend database, or reverse proxies in use.

Finally, not all software vendors publicly disclose vulnerabilities, which means these weaknesses may not be registered within known vulnerability databases (such as [NVD](https://nvd.nist.gov/), or vendor-specific advisories). This information is only disclosed to customers or published through fixes that do not have accompanying advisories. This reduces the effectiveness of vulnerability scanning tools. Typically, vulnerability coverage of these tools will be very good for common products (such as the Apache web server, Microsoft IIS, or IBM's Lotus Domino) but will be lacking for lesser known products.

This is why reviewing vulnerabilities is best done when the tester is provided with internal information about the software, including versions, releases, and patches applied. With this information, the tester can retrieve data from the vendor and analyze potential vulnerabilities in the architecture, as well as their potential impact on the application. When possible, these vulnerabilities can be tested to determine their real effects and to detect if there might be any external elements (such as intrusion detection or prevention systems) that might reduce or negate the possibility of successful exploitation. Testers might even determine through a configuration review that the vulnerability is not actually present since it affects a software component that is not in use.

It is also worthwhile to note that vendors will sometimes silently fix vulnerabilities and make the fixes available with new software releases. Different vendors have varying release cycles that determine the support they may provide for older releases. A tester with detailed information about the software versions used by the architecture can analyse the risk associated with the use of old software releases that might be unsupported in the short term or are already unsupported. This is critical because if a vulnerability emerges in an unsupported older software version, the systems personnel may not be directly aware of it. No patches will be ever made available for it and advisories might not list that version as vulnerable as it is no longer supported. Even if they are aware of the vulnerability and the associated system risks, a full upgrade to a new software release will be necessary, potentially introducing significant downtime in the application architecture or necessitating application re-coding due to incompatibilities with the latest software version.

### Cloud and Container Network Configuration

The same network-configuration-review principle applies where the "network infrastructure" is defined in cloud provider config or container/orchestration manifests rather than physical routers, switches, and firewalls. Misconfiguration here is one of the most common causes of unintended internet exposure of otherwise internal systems. The table below separates what can be checked without credentials (black-box) from what requires access to the provider's configuration (gray-box), and states the evidence that actually supports a finding - for all of these, a black-box result (a port answering, a service reachable) is the evidence; the configuration setting itself, seen gray-box, is the explanation of why.

| Control | Black-box test | Gray-box test | Evidence a finding requires |
|---------|----------------|----------------|------------------------------|
| Security groups / NSGs / cloud firewall rules | Port scan the target's public IPs for ports beyond the intended public listeners (especially SSH/RDP/database ports). | Read the rule set directly: `aws ec2 describe-security-groups` (AWS), `az network nsg rule list --nsg-name <nsg>` (Azure), or `gcloud compute firewall-rules list` (GCP), checking for `0.0.0.0/0` ingress or unrestricted egress. | The black-box scan shows the port actually answering (not just filtered/no-response), or the gray-box rule set shows a specific rule granting that access with no compensating control. |
| VPC/subnet isolation | Attempt to reach backend-tier hosts (database ports, internal admin paths) directly from the internet, using addresses/hostnames found via reconnaissance. | Review the VPC/subnet layout and route tables: `aws ec2 describe-route-tables` (AWS), `az network vnet subnet list` plus route table inspection (Azure), or `gcloud compute networks subnets list` / `gcloud compute routes list` (GCP), confirming backend tiers sit in private subnets with no route to an internet gateway. | A direct connection from outside the VPC succeeds, or the route table shows a route to an internet/NAT gateway from a subnet that should be private. |
| Load balancer/CDN configuration | Attempt to reach the origin server directly (bypassing the load balancer/CDN hostname), using an IP found via DNS history, certificate transparency logs, or leaked headers. | Review listener rules, origin configuration, and origin-restriction settings (e.g. an origin security group scoped to only the CDN's IP ranges, or an origin-verification header/secret). | The origin responds directly to the bypass attempt (not just to traffic via the intended load balancer/CDN hostname). |
| Service mesh policies | Not directly testable from outside the mesh in most deployments; note as gray-box-only unless the tester has a foothold inside the cluster/mesh. | For Istio: `kubectl get authorizationpolicy --all-namespaces` and `kubectl get peerauthentication --all-namespaces -o yaml` (checking `mtls.mode`) to review authorization policies and mTLS mode for services that should require mesh-internal authentication. | An `ALLOW-ALL` policy or `PERMISSIVE`/absent mTLS mode found in configuration, ideally confirmed by an unauthenticated in-mesh call succeeding where the design intended it to be denied. |
| Kubernetes `NetworkPolicy` | From a pod already inside the cluster (if in scope), attempt a connection from an unauthorized pod to a sensitive workload (e.g. a database pod). | Confirm which CNI plugin is installed (`kubectl get pods -n kube-system` to identify the CNI's own pods, e.g. `calico-node` or `cilium`) and whether it enforces `NetworkPolicy`; run `kubectl get networkpolicy --all-namespaces` and `kubectl describe networkpolicy <name> -n <namespace>` to review policy objects for the sensitive workload and whether namespace-level default-deny is applied. | The in-cluster connection attempt succeeds despite an apparently-restrictive `NetworkPolicy` being present (proving the CNI isn't enforcing it), or `kubectl get networkpolicy` returns nothing at all for a namespace containing a sensitive workload. |

A few things to keep in mind that apply across all five rows:

- These are illustrative checks, not an exhaustive list - the exact API calls, CLI commands, and console paths differ by provider and by version, and change over time. Adapt to the actual deployment (AWS vs. Azure vs. GCP, which CNI plugin, which service mesh) rather than treating the commands above as universal.
- Black-box results are the primary evidence for a finding; gray-box configuration review explains the cause and helps confirm the fix, but a black-box test that fails to reproduce the exposure (e.g. the port is filtered despite a permissive-looking rule, because another control blocks it) means the finding needs re-scoping, not that the configuration review was wrong.

For example: a security group meant to allow the load balancer to reach the application on port 443 also has an inbound rule for port 3306 (MySQL) open to `0.0.0.0/0`, put there temporarily for a one-off migration script and never removed.

### Administrative Tools

Any web server infrastructure requires the existence of administrative tools to maintain and update the information used by the application. This information includes static content (web pages, graphic files), application source code, user authentication databases, etc. The type of administrative tools used can vary depending on the specific site, technology, or software in use: some are web-based administrative consoles (see also [Enumerate Infrastructure and Application Admin Interfaces](05-Enumerate_Infrastructure_and_Application_Admin_Interfaces.md), which covers this in more depth, including modern cloud, Kubernetes, and CI/CD consoles), some are plain-text configuration files (as with Apache), and some are OS-native GUI/command-line tools (as with Microsoft's IIS server or `kubectl`/cloud CLIs in modern deployments).

In most cases, the server configuration is managed with various file maintenance tools, administered through SSH/SFTP, WebDAV, network file systems (NFS, CIFS), infrastructure-as-code pipelines (Terraform/CloudFormation/Ansible), or GitOps tooling that pushes configuration changes automatically. Obviously, the operating system of the elements that make up the application architecture will also be managed using other tools. Applications may also contain embedded administrative interfaces for managing application data (users, content, etc.).

After mapping the administrative interfaces used to manage different parts of the architecture, it is important to review them. If an attacker gains access to any of these interfaces, they could potentially compromise or damage the application architecture. To accomplish this, it's important to:

- Determine the mechanisms that control access to these interfaces and their associated susceptibilities. This information may be available online.
- Ensure that the default username and password are changed.

Some companies choose not to manage all aspects of their web server applications and may delegate content management to other parties. This external company might provide only certain parts of the content (such as news updates or promotions), or it might completely manage the web server (including content and code). It is common to find administrative interfaces available from the internet in these situations, since using the internet is cheaper than providing a dedicated line that will connect the external company to the application infrastructure through a management-only interface. In such situations, it's crucial to test whether the administrative interfaces are vulnerable to attacks.

## Tools

- [nmap](https://nmap.org/) - network/port scanning and service fingerprinting.
- [ScoutSuite](https://github.com/nccgroup/ScoutSuite) - multi-cloud (AWS/Azure/GCP) security configuration auditing, including security groups/NSGs and network exposure.
- [Prowler](https://github.com/prowler-cloud/prowler) - AWS/Azure/GCP security assessment, including network and firewall rule checks.
- [kube-bench](https://github.com/aquasecurity/kube-bench) - CIS Kubernetes Benchmark scanner.
- [kube-hunter](https://github.com/aquasecurity/kube-hunter) - identifies exposed Kubernetes network-facing components.
- [Shodan](https://www.shodan.io/) / [Censys](https://censys.io/) - internet-wide scan data useful for identifying unintentionally exposed infrastructure during black-box assessments.

## References

- [NIST National Vulnerability Database (NVD)](https://nvd.nist.gov/)
- [CIS Benchmarks](https://www.cisecurity.org/cis-benchmarks) - hardening baselines for common web/application servers, cloud providers, and Kubernetes.
- [AWS: Security Groups for Your VPC](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-security-groups.html)
- [Azure Network Security Groups](https://learn.microsoft.com/en-us/azure/virtual-network/network-security-groups-overview)
- [Kubernetes: Network Policies](https://kubernetes.io/docs/concepts/services-networking/network-policies/)
- [Istio: Authorization Policy](https://istio.io/latest/docs/reference/config/security/authorization-policy/)
