# Project BlackTrace — Implementation Checklist

## 1. Player account
- [ ] Create bt-player as an ordinary, unprivileged user.
- [ ] Verify bt-player has no sudo, lxd, or administrative group access.

## 2. Diagnostics web service
- [ ] Preserve the existing BT-204 records.
- [ ] Document how players discover the maintenance workflow.
- [ ] Keep the service running as bt-operator.

## 3. Request workflow
- [ ] Document how a player submits a maintenance request.
- [ ] Implement a predictable review trigger.
- [ ] Keep the inbox restricted; never make it world-writable.
- [ ] Isolate the intentional vulnerability to this CTF.
- [ ] Ensure the workflow can be reset safely.

## 4. Root proof objective
- [ ] Create a root-owned proof flag during setup.
- [ ] Verify an ordinary player cannot read it directly.
- [ ] Verify the intended challenge path reaches the objective.

## 5. Reproducibility and testing
- [ ] Write setup.sh.
- [ ] Write health-check.sh.
- [ ] Write reset.sh.
- [ ] Test from a clean Ubuntu 24.04 baseline.
- [ ] Document exact commands and expected results.
- [ ] Record the walkthrough and package the deliverables.

## 6. Safety
- [ ] Do not modify the separate Wazuh VM.
- [ ] Preserve the existing working installation until testing passes.
- [ ] Do not expose the vulnerable service to the public internet.

## 7. Finalization status — 2026-10-17
- [x] Existing diagnostics service and BT-204 public records inspected.
- [x] Unprivileged bt-player account exists.
- [x] Root proof file exists and is intended to remain root-only.
- [x] Local request prototype passes basic validation tests.
- [ ] Connect a validated player request to a predictable review trigger.
- [ ] Ensure privileged processing never invokes a shell with untrusted input.
- [ ] Implement full target setup, health-check, and reset procedures.
- [ ] Validate the complete challenge from a clean snapshot.
