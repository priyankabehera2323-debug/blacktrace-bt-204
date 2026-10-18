# BlackTrace — Target Deployment Design

## Target
- Ubuntu 24.04 LTS
- Diagnostics service on port 8080
- Host-only lab interface: 192.168.155.10
- Player account: bt-player
- Maintenance ticket: BT-204

## Deployment requirements
1. Preserve the existing diagnostics service and public records.
2. Ensure bt-player has no sudo, lxd, or administrative privileges.
3. Create a validated maintenance-request handoff.
4. Keep request storage restricted to the designated service account.
5. Keep privileged processing separate from untrusted request handling.
6. Never interpolate request data into a shell command.
7. Create a root-owned proof objective readable only by root initially.
8. Provide repeatable setup, health-check, and reset procedures.
9. Test the deployment and challenge path from a clean snapshot.
10. Keep the challenge isolated from public networks.

## Completion criteria
- Setup succeeds on a clean Ubuntu 24.04 target.
- Invalid requests are rejected.
- The review trigger behaves predictably.
- The intended multi-stage challenge path is verified.
- Reset restores the documented starting state.
- No Wazuh VM configuration is changed.

## Current limitation
The existing target workflow is not yet verified end to end.
This design does not claim that the challenge is complete.
