# Project BlackTrace — Author Walkthrough

## 1. Challenge overview
BlackTrace is a Linux privilege-escalation CTF built for Ubuntu 24.04.
The story begins with diagnostics ticket BT-204 and a maintenance review.

## 2. Lab setup
- Target: Ubuntu 24.04
- Attacker: Kali Linux
- Player account: bt-player
- Diagnostics port: 8080
- Recovery: VirtualBox snapshot

## 3. Intended challenge path
1. Enumerate the diagnostics service and its public records.
2. Read the BT-204 maintenance handover and deployment checklist.
3. Identify the service account and review workflow.
4. Inspect the request-processing code and its trust boundary.
5. Demonstrate the intended weakness in the isolated lab.
6. Retrieve the root proof objective.

## 4. Evidence to capture
- Diagnostics service discovery from Kali
- BT-204 public records
- Service account and workflow configuration
- Relevant processor code and permissions
- Each verified challenge stage as bt-player
- Proof objective reached through the intended path
- Health-check and reset results

## 5. Reproducibility
Document the exact setup, health-check, and reset commands after
those scripts are fully implemented and tested on a clean baseline.

## 6. Remediation
Avoid shell interpretation of untrusted request fields. Validate input
against strict allowlists, use argument arrays instead of shell strings,
restrict privileged interfaces, and audit access to request data.

## 7. Current status
Draft only. The end-to-end player workflow, clean-baseline test,
screenshots, and recording are not yet complete.
Do not present unverified steps as successful.
