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

## Current test status — 2026-10-17

### Verified in the local build workspace
- Valid BT-204 review request accepted with HTTP 202.
- Request processed by the safe local processor.
- JSONL audit entry created for the review.
- Invalid ticket BT-999 rejected with HTTP 400.
- Unsupported action delete rejected with HTTP 400.
- Workspace health check passed.
- Git working tree was clean after ignoring local test data.

### Verified on the Ubuntu target
- Diagnostics service is active.
- Root review service is inactive.
- bt-player has no sudo or administrative group membership.
- Public diagnostics and maintenance records are accessible.
- Workflow configuration and component permissions were inspected.
- No connected player-to-processor workflow has been verified.

### Remaining
- Implement and document the target request-submission mechanism.
- Define and validate a controlled review trigger.
- Verify the root proof objective from a clean snapshot.
- Complete setup, health-check, and reset tests on the target.
- Record a complete walkthrough only after end-to-end validation.

The local prototype results do not establish that the live target workflow is complete.
