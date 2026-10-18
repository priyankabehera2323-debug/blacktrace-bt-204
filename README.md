# BlackTrace BT-204

An in-progress Linux cybersecurity CTF challenge designed for an isolated
Ubuntu 24.04 lab.

## Current status

- Automated tests: 25 passing in the latest local run.
- Clean target deployment: not verified.
- Complete player-to-root-proof path: not verified.
- Walkthrough screenshots and video: pending.

## Project structure

- `target-files/` — challenge application, policy, workflow, and service files.
- `tests/` — automated unit and integration tests.
- `install-target.sh` — target installation script.
- `target-setup.sh` — target preflight checks.
- `target-health-check.sh` — target health checks.
- `IMPLEMENTATION-CHECKLIST.md` — development checklist.
- `TARGET-DEPLOYMENT-DESIGN.md` — deployment design.

## Safety

For authorized, isolated lab use only. This project is under development
and is not yet validated as a complete playable challenge.
