# Architectural Threat Modeling Checklist for Workflow and State Transition Abuse

## Overview

Modern distributed applications frequently fail not because of traditional vulnerabilities, but due to architectural flaws in workflow enforcement, state management, and API orchestration. This checklist helps identify abuse cases where attackers manipulate valid sequences to bypass business controls.

---

## 1. State Transition Enforcement

| Check | Description |
|------|-------------|
| ☐ | All business workflows have an explicit server-side state machine |
| ☐ | Backend validates that transitions occur only from allowed previous states |
| ☐ | State is never inferred from client input |
| ☐ | State changes are atomic |
| ☐ | Invalid or out-of-order transitions are rejected |
| ☐ | State change failures are logged with high severity |

---

## 2. Multi-Step Workflow Validation

| Check | Description |
|------|-------------|
| ☐ | Each workflow step has mandatory prerequisites |
| ☐ | API endpoints enforce correct step ordering |
| ☐ | Replay of previously valid steps is blocked |
| ☐ | Tokens are scoped to workflow state |
| ☐ | Workflow cancellation is fully enforced server-side |

---

## 3. API Sequence Integrity

| Check | Description |
|------|-------------|
| ☐ | APIs require sequence tokens or state hashes |
| ☐ | Server rejects API calls that skip intermediate steps |
| ☐ | Cross-service calls verify upstream workflow state |
| ☐ | Retry logic cannot advance state incorrectly |

---

## 4. Cross-Layer Authorization Consistency

| Check | Description |
|------|-------------|
| ☐ | UI restrictions are never relied on for authorization |
| ☐ | All hidden UI actions are verified server-side |
| ☐ | API endpoints are reviewed for orphaned permissions |
| ☐ | Role changes propagate across services in real time |

---

## 5. Distributed System Abuse

| Check | Description |
|------|-------------|
| ☐ | Event-driven services validate ordering guarantees |
| ☐ | Idempotency is enforced on state transitions |
| ☐ | Partial failures cannot leave workflows in exploitable states |
| ☐ | Asynchronous queues cannot be abused to bypass checks |

---

## 6. Telemetry and Detection

| Check | Description |
|------|-------------|
| ☐ | Workflow state transitions are logged centrally |
| ☐ | Alerts exist for impossible transitions |
| ☐ | Telemetry detects API misuse patterns |
| ☐ | Incident playbooks include workflow abuse scenarios |

---

## 7. Threat Modeling Coverage

| Check | Description |
|------|-------------|
| ☐ | Threat models include abuse of valid sequences |
| ☐ | Architecture reviews consider logic and workflow risks |
| ☐ | Abuse cases are reviewed quarterly |
| ☐ | Product teams test at least one workflow abuse scenario per release |

---

## Example Abuse Scenarios

- Confirming orders without payment  
- Approving refunds without prior authorization  
- Skipping approval workflows via API  
- Replaying legacy endpoints removed from UI  

---

## Objective

Prevent attackers from abusing legitimate application flows to achieve unauthorized outcomes by enforcing architectural integrity across UI, API, and backend layers.

