# BlackTrace Target Deployment Manifest

## Platform
- Ubuntu Server 24.04 LTS
- Python 3
- Flask for the diagnostics web application
- Dedicated VirtualBox host-only network

## Services
- `blacktrace-diagnostics`: public challenge clues and health endpoint, port 8080
- `blacktrace-review`: request validation and audit processing; must remain inactive until its execution model and permissions are tested

## Accounts and permissions
- `bt-player`: unprivileged challenge account; no sudo or administrative groups
- `bt-operator`: dedicated service account for the maintenance workflow
- Inbox: restricted to the designated workflow account
- Root proof: root-owned and mode 600

## Safety requirements
- Do not execute untrusted request values through a shell.
- Reject unknown tickets and unsupported actions.
- Keep the review processor inactive until setup and health checks pass.
- Do not modify the separate Wazuh VM.
- Test on a disposable snapshot before submission.

## Current status
This manifest documents intended deployment requirements; it is not evidence that deployment or the complete challenge path has passed testing.
