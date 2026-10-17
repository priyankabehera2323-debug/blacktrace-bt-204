# BlackTrace — Request Workflow Specification

## Goal
Allow the unprivileged bt-player account to submit a BT-204 maintenance
request through a documented interface, without direct access to the
restricted inbox or unrestricted sudo privileges.

## Current state
- Diagnostics service runs as bt-operator on port 8080.
- Public records identify ticket BT-204.
- The inbox is restricted to bt-operator.
- The review processor runs as root.
- The review service is a static one-shot systemd service.

## Required design
1. Provide a documented request-submission interface.
2. Validate the request's expected fields and size.
3. Keep the inbox restricted to the intended service account.
4. Provide a predictable review trigger.
5. Isolate the intentional vulnerability to this CTF.
6. Keep all other services and the separate Wazuh VM unchanged.
7. Ensure setup, health-check, and reset scripts are repeatable.

## Acceptance tests
- bt-player can access public diagnostics records.
- bt-player cannot directly read the restricted inbox.
- bt-player has no sudo or administrative group access.
- A valid request can follow the documented workflow.
- The review trigger behaves predictably.
- The root proof flag remains protected until the intended challenge path.
- Reset restores a known, documented challenge state.

## Implementation note
Do not grant broad sudo access or make the inbox world-writable.
Test the new workflow in the build workspace before deployment.
