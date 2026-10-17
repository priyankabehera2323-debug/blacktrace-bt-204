# Project BlackTrace — Build Plan

## Target
- Ubuntu 24.04 LTS
- One target VM
- Diagnostics service on port 8080

## Challenge progression
1. Discover the BT-204 maintenance clues.
2. Investigate the service account and workflow configuration.
3. Identify the request-processing trust-boundary weakness.
4. Reach the designated root proof objective.

## Required deliverables
- Original challenge source and documentation
- Reproducible setup.sh
- health-check.sh
- reset.sh
- Clean baseline test
- Step-by-step offensive walkthrough
- Screenshots and full walkthrough recording
- Final ZIP package

## Safety and quality
- Keep the existing working baseline recoverable.
- Do not modify the separate Wazuh VM.
- Do not rely on the administrator account as the player.
- Do not introduce world-writable inboxes or unexplained root cron jobs.
- Test setup, reset, and health checks on Ubuntu 24.04.

## Deployment safeguards
- Preserve the existing blacktrace-diagnostics.service.
- Keep blacktrace-review.service inactive until its processor is safely implemented and tested.
- Keep /var/lib/blacktrace/inbox restricted to bt-operator.
- Do not grant bt-player sudo privileges.
- Keep /root/blacktrace-proof.txt root-owned with mode 600.
- Do not modify the separate Wazuh VM.
- Test setup, health-check, and reset on a disposable snapshot.
- Do not claim the challenge is complete until a clean-baseline end-to-end test passes.
