# Project BlackTrace — Request Workflow

## Purpose
Provide a documented, repeatable maintenance-review workflow for the
BT-204 Linux privilege-escalation challenge.

## Components
1. Diagnostics web service running as bt-operator.
2. Restricted maintenance-request inbox.
3. Root-owned review processor, isolated to this CTF.
4. Dedicated bt-player account with no administrative privileges.
5. Root-owned proof flag.

## Required behavior
- Players discover the workflow from the public diagnostics records.
- Request submission must be documented and predictable.
- The review trigger must be explicit and reproducible.
- The inbox must not be world-writable.
- The player must not receive unrestricted sudo permissions.
- The intended vulnerability must be documented for the author and
  isolated from other services.
- The proof flag must remain unreadable to the player until the
  intended challenge objective is achieved.

## Implementation order
1. Build the request-submission mechanism in the workspace.
2. Configure a narrow, auditable review trigger.
3. Implement setup, health-check, and reset scripts.
4. Test using bt-player, not the administrator account.
5. Verify the challenge from a clean baseline.
6. Document and record the final walkthrough.

## Safety
Do not modify the separate Wazuh VM.
Do not expose the challenge service to the public internet.
Keep the existing installation recoverable until the new build passes.
