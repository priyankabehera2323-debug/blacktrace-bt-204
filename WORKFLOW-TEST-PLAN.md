# BlackTrace — Workflow Test Plan

## Goal
Connect request submission, review, and challenge evidence into a
repeatable workflow on the isolated Ubuntu CTF target.

## Required checks
1. bt-player can submit only documented BT-204 request fields.
2. Requests are stored without making the inbox world-writable.
3. Invalid tickets and unsupported actions are rejected.
4. The review processor does not interpret untrusted fields as shell code.
5. Review results are auditable.
6. bt-player cannot directly read the root proof file or use sudo.
7. Setup, health-check, and reset are repeatable.
8. The complete challenge is tested from a clean snapshot.

## Safety
Do not run crafted requests through the current root processor.
Do not expose the vulnerable service to the public internet.
Keep the separate Wazuh VM unchanged.
