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

## Final integration plan — 2026-10-17

1. Keep the diagnostics service and public BT-204 records unchanged.
2. Keep the request interface bound to localhost during development.
3. Validate request fields before writing any request to the inbox.
4. Use a dedicated, least-privilege handoff mechanism for review requests.
5. Ensure the privileged reviewer uses argument arrays or direct file APIs,
   never a shell command built from untrusted request data.
6. Add setup, health-check, and reset support for the complete target.
7. Test a clean baseline, a valid request, rejected invalid requests, and reset.
8. Verify the root-only objective remains unreadable to bt-player until the
   documented challenge objective is reached.
9. Do not claim end-to-end completion until every intended stage is verified.
