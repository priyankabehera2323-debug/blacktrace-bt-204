# BlackTrace BT-204 — Maintenance Review Trust-Boundary Challenge

## Player objective
Starting as `bt-player`, investigate the BT-204 maintenance workflow and obtain the designated root-only proof through a reproducible, multi-stage vulnerability chain.

## Required stages
1. **Reconnaissance:** Discover BT-204 and identify the maintenance interface.
2. **Workflow analysis:** Trace how requests are accepted, stored, validated, and processed.
3. **First weakness:** Discover a narrowly scoped information-disclosure or trust-boundary flaw that reveals a clue required for the next stage.
4. **Second weakness:** Use that clue to reach a distinct, restricted workflow capability.
5. **Privilege boundary:** Demonstrate a separate flaw in the privileged review workflow that permits access to the designated proof.
6. **Evidence:** Capture commands and outputs demonstrating each stage from the `bt-player` starting account.

## Security constraints
- Target: Ubuntu 24.04, isolated CTF VM.
- Starting account: `bt-player`, with no sudo or administrative group membership.
- No brute force, destructive actions, kernel exploits, unsafe shell interpolation, or broad automated privilege-escalation tools.
- Do not rely on a simple unsafe sudo/SUID binary, writable root script/service, or readable root key.
- Root proof remains root-owned and mode 0600 at baseline.
- Invalid requests must fail predictably.
- Reset must restore all challenge state and proof permissions.

## Acceptance criteria
- Every stage depends on evidence or access obtained in an earlier stage.
- A fresh player can reproduce the complete path from a clean Ubuntu 24.04 snapshot.
- Unit tests, deployment, health check, reset, and end-to-end player-to-proof tests pass.
- Include a complete write-up, numbered evidence screenshots, and an MP4 walkthrough.

## Status
Design updated. The multi-stage vulnerabilities and full player-to-proof path are not yet implemented or verified. Do not claim assessment completion until the acceptance criteria pass.
