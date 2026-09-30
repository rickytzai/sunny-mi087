# Real microphone validation - sanitized event proof

The original project records identify two completed human sessions: E2E `20260928_184302` and barge-in `20260928_184855`. Their status markers are retained in the [allowlisted timeline](../evidence/human-validation-timeline.json). The timing source was inspected alongside the provider-event handler; absolute clock values are removed and playback start becomes t=0.

| Recorded harness event | Relative seconds |
| --- | --- |
| Playback start | 0.000000 |
| AssemblyAI SpeechStarted detected | 10.345000 |
| PlaybackStop trigger | 10.345000 |
| TurnFinal / new turn | 12.351398 |
| New response playback start | 14.744950 |

The handler invokes playback stop when provider `SpeechStarted` arrives during active playback, before accepting the later completed turn. The identical stored SpeechStarted and stop-trigger timestamps **do not prove zero acoustic latency**. Human speech onset was not recorded. This single-session timeline is evidence of recorded ordering, not a benchmark or performance guarantee.

## Film boundary

The final [v5 film](../assets/sunny-demo-v5.mp4), 01:05-01:20, includes **Real microphone test - sanitized event proof**. It displays E2E provenance and this real event ordering with relative timestamps. It is a visual reconstruction of recorded event metadata, not live footage, a captured waveform or a human audio excerpt. The rest is a scripted product visualization with synthesized character dialogue.

No raw human audio, transcript, identity or voice conversion is included. The animated female character is not the human tester. No tester voice is played. The event-proof sequence replaces the earlier unsupported Jev/persona-distillation visual claims.
