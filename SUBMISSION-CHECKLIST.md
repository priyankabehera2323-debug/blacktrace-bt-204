# Project BlackTrace — Submission Checklist

## Existing work
- [x] Ubuntu 24.04 target VM and Kali connectivity
- [x] VirtualBox recovery snapshot
- [x] Diagnostics service and BT-204 discovery records
- [x] Unprivileged bt-player account
- [x] Request-interface prototype and input-validation tests
- [x] Build plan, workflow design, and implementation notes
- [x] Setup preflight and health-check starter scripts

## Must complete before submission
- [ ] Finish the end-to-end player request and review workflow
- [ ] Ensure the intended vulnerability is isolated to the CTF
- [ ] Implement a real, repeatable setup process
- [ ] Implement a real reset process
- [ ] Test every stage as bt-player
- [ ] Verify the root proof objective through the intended path
- [ ] Test on a clean Ubuntu 24.04 baseline
- [ ] Capture screenshots and exact commands
- [ ] Finish the walkthrough document
- [ ] Record the MP4 walkthrough
- [ ] Create and verify CandidateName_MachineName.zip

## Current limitations
The setup script is a preflight only. The reset script is a placeholder.
The request interface validates input but does not persist requests or
trigger the review workflow. End-to-end player testing is outstanding.
Do not describe the challenge as submission-ready until these gaps pass.
