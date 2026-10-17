# Project BlackTrace — Author Walkthrough

## 1. Challenge Overview

BlackTrace is a Linux privilege-escalation CTF designed for Ubuntu 24.04. Players investigate maintenance ticket BT-204, enumerate diagnostic records, and examine how a privileged review workflow handles untrusted request data.

**Current status:** The local request-processing prototype has passed basic validation tests. The complete player-to-root challenge path has not yet been verified.

## 2. Lab Environment

- Target: Ubuntu 24.04
- Attacker: Kali Linux
- Unprivileged player account: `bt-player`
- Diagnostics service: port 8080
- Local prototype interface: port 8081, bound to localhost
- Recovery: VirtualBox snapshot

The local prototype is separate from the live target workflow.

## 3. Challenge Investigation Path

1. Discover the diagnostics service and enumerate its public records.
2. Read the BT-204 maintenance handover and deployment checklist.
3. Identify the service account and review workflow.
4. Inspect the request-processing code and its trust boundary.
5. Investigate how untrusted request data could cross a privilege boundary.
6. Verify the intended challenge objective in an isolated, reproducible lab.

**Verification note:** The intended live exploitation path and root proof objective still require end-to-end testing as `bt-player`. Do not mark these stages complete until verified.

## 4. Verified Local Prototype Tests

The following tests have passed in the build workspace:

- Python and Flask availability check.
- Python syntax compilation for the three prototype modules.
- Request interface health endpoint.
- Valid BT-204 request accepted and saved to the local test outbox.
- Unknown ticket rejected.
- Unsupported action rejected.
- Safe review processor successfully processed a valid local request.
- Safe review processor rejected an unsupported action.
- Local reset cleared the test request.
- Git commits recorded the health-check and request-interface updates.

These tests validate the local prototype, not the live privileged workflow.

## 5. Evidence Required for Final Submission

Capture genuine evidence of:

- Diagnostics discovery from Kali.
- BT-204 public records.
- Service account and workflow configuration.
- Relevant processor code and file permissions.
- Player-level access and each verified challenge stage.
- The intended proof objective reached through the challenge path.
- Setup, health-check, and reset results.
- A clean-baseline run from the documented starting state.

Record exact commands and actual outputs. Do not fabricate screenshots or present prototype results as live-target results.

## 6. Reproducibility

The current `setup.sh` is a preflight check, not a full deployment script. The current `reset.sh` resets local prototype data, not the complete target environment.

A repeatable setup and reset process must be implemented and tested on a disposable snapshot before submission.

## 7. Security Remediation

- Never interpolate untrusted request fields into shell commands.
- Validate inputs using strict allowlists.
- Use argument arrays rather than shell command strings.
- Keep privileged interfaces narrowly scoped.
- Apply least-privilege permissions to request files and services.
- Audit privileged workflow activity.
- Keep the intentionally vulnerable challenge isolated from production networks.

## 8. Outstanding Work

- Complete and verify the intended player-to-root challenge path.
- Implement repeatable setup and full reset procedures.
- Test the full challenge as `bt-player`.
- Test on a clean Ubuntu 24.04 baseline.
- Capture screenshots and exact commands.
- Record the MP4 walkthrough.
- Package the final submission as `CandidateName_MachineName.zip` and verify its contents.

**Completion rule:** Do not describe BlackTrace as submission-ready until the complete challenge succeeds reproducibly from a clean baseline.
