# Architecture and responsibility boundary

| Component | Actual inspected role | Evidence boundary |
| --- | --- | --- |
| AssemblyAI | Real-time speech activity and turn events | Speech recognition/turn signals belong to the provider |
| Sunny core | Handle accepted text turns and produce a response | Human E2E records show the mic-to-speaker path |
| Provider-event barge-in handler | On SpeechStarted while playback is active, trigger stop before the new completed turn and response | Existing human session; no acoustic-latency guarantee |
| Offline RhythmAdapter | Update numerical rolling pause state and next-response delay | Executable source excerpt and synthetic replay; not wired into the live harness |
| JevFastPath prototype | Rule-based intent routing with fallback | Separate prototype, not the reviewer-proposed JEF feedback loop |

## Verified live sequence

`Physical microphone → AssemblyAI speech/turn events → Sunny core → speaker`

`SpeechStarted during playback → stop trigger → TurnFinal / new turn → response playback`

The [recorded relative timeline](human-validation.md) represents one existing session, not benchmark measurements. The static public website is a visualization, not an online voice backend.

## Separate offline adaptation

`Numerical pause observation → rolling mean → smoothed bounded next_pause_ms → next simulated response delay`

See [learning proof](learning-proof.md) for unchanged source methods, deterministic tests, and integration gaps. We do not assert that provider events already drive this learner in the human-tested runtime. JEF and relationship-aware distillation are not included in the submission flow.
