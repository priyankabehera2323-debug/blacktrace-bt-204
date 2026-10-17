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
