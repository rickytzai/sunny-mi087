# Evidence status

| Track | Verification | Public artifact |
| --- | --- | --- |
| Human E2E | Existing physical-microphone session and LIVE_EVIDENCE_EXISTS marker | [E2E summary](../evidence/human-e2e-redacted.json) |
| Human barge-in | Existing provider-triggered stop and later new-turn response; timing source inspected | [recorded relative timeline](../evidence/human-validation-timeline.json) |
| Offline state update | Existing numerical source excerpt executed; original/excerpt replay matched | [learning proof](learning-proof.md) |
| Legacy symbolic event/policy cases | Synthetic documentation only | [fixtures](../examples/) |
| Live adaptation, persistence, learned EOT | Not verified / EOT learning stub | Not claimed |
| JEF and relationship-aware distillation | Not supported by inspected implementation | Omitted |
| Comparative performance | Not benchmarked | No claims |

The human session artifacts and offline learning proof are separate. The public tests can replay numerical state changes and check event metadata; they cannot independently reproduce the private human audio sessions.

Source hashes support provenance, not independent attestation. No raw human audio, transcript or private archive is published. Equal event timestamps do not measure acoustic stop latency. Film 01:05–01:20 is a sanitized visualization of the recorded event evidence, not a human recording.
