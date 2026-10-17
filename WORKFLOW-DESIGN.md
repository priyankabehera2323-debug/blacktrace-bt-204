# Project BlackTrace — Workflow Design

## Challenge type
Linux privilege escalation, with web reconnaissance as the initial stage.

## Story
The BlackTrace diagnostics service was moved during maintenance.
Ticket BT-204 is awaiting review. Players investigate the service
account, maintenance configuration, and request-processing workflow.

## Intended progression
1. Discover the diagnostics service and its public records.
2. Identify the maintenance operator and review workflow.
3. Trace how a request moves from submission to privileged processing.
4. Identify and demonstrate the unsafe trust boundary.
5. Retrieve the designated root proof flag.

## Required implementation
- A documented request submission mechanism.
- A predictable review trigger.
- A deliberately vulnerable processor isolated to this CTF.
- A normal, unprivileged player starting account.
- A root-owned proof flag readable only after the intended escalation.
- Setup, health-check, and reset scripts.

## Security and reliability requirements
- Do not make the inbox world-writable.
- Do not grant the player unrestricted sudo access.
- Do not rely on the administrator account to prove exploitability.
- Do not modify the separate Wazuh VM.
- Setup and reset must be repeatable on Ubuntu 24.04.
- Health checks must verify the services, files, permissions, and objective.
- The build must include cleanup and recovery instructions.
