# Project BlackTrace — Author Walkthrough

## 1. Project Overview

**BlackTrace** is a Linux security challenge designed around a maintenance-review workflow on Ubuntu 24.04. The challenge focuses on service enumeration, Linux permissions, request validation, and trust boundaries in privileged workflows.

The scenario centers on maintenance ticket **BT-204**. Players investigate diagnostic records and workflow configuration to understand how a privileged review process handles data submitted by an untrusted requester.

## 2. Lab Environment

| Component | Configuration |
|---|---|
| Target platform | Ubuntu 24.04 |
| Attacker environment | Kali Linux |
| Intended player account | `bt-player` |
| Diagnostics service | Port 8080 |
| Local request prototype | Port 8081, bound to localhost |
| Virtualization | Oracle VirtualBox |
| Recovery approach | VirtualBox snapshot |

The local request prototype is separate from the existing target services. Testing the prototype does not, by itself, demonstrate successful exploitation of the privileged target workflow.

## 3. Challenge Design

The intended investigation covers the following areas:

1. Discover the exposed diagnostics service.
2. Enumerate public diagnostic records and locate the BT-204 maintenance ticket.
3. Examine service accounts, file permissions, and workflow configuration.
4. Trace how a request moves from the interface to the review processor.
5. Identify the trust boundary between unprivileged input and privileged processing.
6. Evaluate the security impact and verify the challenge objective in an isolated lab.

The central security lesson is that privileged workflows must not trust identity or authorization claims supplied directly by an untrusted requester.

## 4. Implementation

The build includes the following components:

- **Request interface:** Accepts JSON requests and validates ticket and action fields.
- **Review policy:** Defines the accepted ticket, supported actions, and expected reviewer identity.
- **Review processor:** Applies policy checks and handles the review workflow without constructing shell commands from untrusted input.
- **Proof setup:** Creates a root-owned proof file for the intended local challenge.
- **Audit logging:** Records review activity.
- **Health and reset scripts:** Support prototype validation and local test-data cleanup.

The current local prototype uses a dedicated test outbox. Its reset script does not reset the complete target environment.

## 5. Testing and Validation

All 17 automated unit tests passed in the build workspace.

The local HTTP prototype was also tested manually:

| Test | Observed result |
|---|---|
| Health endpoint | Returned `status: ok` |
| Valid BT-204 request | Accepted with HTTP 202 |
| Unknown ticket | Rejected with HTTP 400 |
| Unsupported action | Rejected with HTTP 400 |
| JSON array instead of an object | Rejected with HTTP 400 |

The automated tests cover request validation, policy enforcement, processor behavior, proof-file permissions, and checks against shell execution in the safer processor.

**Scope of results:** These results establish local prototype and unit-test behavior. They do not establish that the complete player-to-root path has succeeded on a clean Ubuntu target.

## 6. Security Analysis and Remediation

A privileged service must treat request data as untrusted, even when that data contains a familiar ticket number or reviewer name.

Recommended mitigations include:

- Enforce authorization independently of requester-supplied identity fields.
- Use strict allowlists for accepted tickets and actions.
- Avoid shell execution with untrusted input; prefer direct function calls or argument arrays where external commands are necessary.
- Restrict service accounts and filesystem permissions according to least privilege.
- Separate unprivileged request handling from privileged processing.
- Record relevant workflow events in protected audit logs.
- Keep intentionally vulnerable challenge environments isolated from production systems.

## 7. Reproducibility and Recovery

The current `setup.sh` performs preflight checks rather than complete deployment. The current `reset.sh` clears local prototype data only.

Before the challenge can be described as reproducible, deployment and reset must be verified on a disposable, clean Ubuntu 24.04 snapshot. Testing should confirm the initial state, service configuration, permissions, challenge behavior, and recovery procedure.

## 8. Evidence and Submission Checklist

Capture genuine screenshots and command output for:

- Diagnostics service discovery.
- BT-204 diagnostic records.
- Relevant service configuration and file permissions.
- Request validation and policy enforcement.
- Automated test results.
- Setup, health-check, and reset behavior.
- The actual challenge objective, if successfully demonstrated on the isolated target.
- A repeatable run from a clean baseline.

Record exact commands and observed results. Do not present prototype tests as evidence of a live-target exploit.

## 9. Current Status

The local request prototype and automated unit tests have passed. Full end-to-end validation of the intended player-to-root challenge, along with clean-baseline deployment and complete reset testing, remains unverified.

The final submission should include the author walkthrough, supporting evidence, a recorded MP4 demonstration, and the required packaged project files.

**Author's note:** BlackTrace demonstrates the importance of validating authorization at privilege boundaries and keeping privileged operations narrowly scoped. The documented results distinguish implemented components from behavior that still requires end-to-end verification.
