# BlackTrace Request Interface Design

## Purpose
Accept maintenance requests for ticket BT-204 through a controlled interface.

## Current prototype
- GET /health reports interface status.
- POST /submit validates JSON input.
- Only ticket BT-204 is accepted.
- Supported actions are review and status-check.
- The prototype does not write to the inbox or trigger privileged work.

## Security boundaries
- The bt-player account must remain unprivileged.
- The request interface must not expose arbitrary command execution.
- The restricted inbox must not become world-writable.
- Privileged processing must validate request data and avoid shell interpretation.
- Tests must use a disposable lab snapshot and must not affect the separate Wazuh VM.

## Next implementation stages
1. Define a documented request-submission mechanism.
2. Define a narrow review trigger and its permissions.
3. Implement setup, health-check, and reset scripts.
4. Test access boundaries as bt-player.
5. Verify the full challenge from a clean baseline.
