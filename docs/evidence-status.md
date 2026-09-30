# Public evidence status

This page separates functional verification, synthetic documentation checks, and claims that have not been benchmarked.

## Status definitions

- **VERIFIED FUNCTIONAL** — the end-to-end behavior was completed in a human validation session; the public artifact is a redacted summary.
- **VERIFIED SYNTHETIC** — a deterministic public fixture passes its documented invariants; it is not production or human-session telemetry.
- **NOT YET BENCHMARKED** — no public-safe, statistically meaningful measurement is available, so no number or superiority claim is made.

## Claim table

| Claim | Status | Evidence | What remains unclaimed |
| --- | --- | --- | --- |
| Physical microphone input reached AssemblyAI real-time speech events, Sunny, and speaker output | VERIFIED FUNCTIONAL | Project evidence ID `20260928_184302`; [`human-e2e-redacted.json`](../evidence/human-e2e-redacted.json) | Accuracy, latency, uptime, and device-generalization metrics |
| Human speech during active playback caused `SpeechStarted`, playback yield, a new turn, and a new Sunny response | VERIFIED FUNCTIONAL | Project evidence ID `20260928_184855`; [`barge-in-redacted.json`](../evidence/barge-in-redacted.json) | `SpeechStarted`-to-stop latency and percentile distribution |
| Public examples preserve provider/layer responsibility and barge-in ordering | VERIFIED SYNTHETIC | [`assemblyai_events.json`](../examples/assemblyai_events.json), [`turn_policy_cases.json`](../examples/turn_policy_cases.json), and public contract tests | Production backend equivalence or runtime performance |
| Baseline assistant vs. Sunny | NOT YET BENCHMARKED | No supported public dataset | Any improvement percentage or comparative score |
| Pause/hesitation performance | NOT YET BENCHMARKED | No supported public dataset | False-cut rate, wait-time improvement, or preference accuracy |

## Evidence boundary

The functional status and evidence identifiers come from the project verification record supplied for the submission. The raw evidence remains private because it includes human audio and transcript content. These summaries do not reveal that content and do not independently reproduce the sessions.

No benchmark file is published because no real, public-safe benchmark values were available. Missing evidence weakens the claim rather than strengthening the story.
