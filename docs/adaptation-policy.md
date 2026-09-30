# Bounded adaptation policy

Sunny personalizes turn-taking behavior through a deliberately narrow preference model. It learns **how a person prefers to converse, not who that person is**.

## Allowed preference categories

| Category | What it controls | Example symbolic values |
| --- | --- | --- |
| Pause tolerance | Whether a possible thinking pause should remain open longer | `brief`, `standard`, `extended` |
| Interruption behavior | How playback yields when new speech begins | `stop_on_speech`, `duck_on_speech` |
| Response pacing | Relative delivery cadence selected for a response | `compact`, `balanced`, `deliberate` |
| Turn-taking preference | How readily Sunny claims or yields the floor | `responsive`, `balanced`, `patient` |

The values above are public contract labels. They do not expose private thresholds or imply that a specific duration has been benchmarked.

## Policy inputs and outputs

Inputs are limited to real-time speech/turn events, current playback state, and the bounded preferences above. Outputs are control decisions such as:

- keep listening;
- accept the completed turn;
- stop or duck playback;
- select a response pacing class;
- use the deterministic fast path for an event-driven micro-decision.

## Explicit non-goals

Sunny does not infer or store:

- identity or demographic attributes;
- personality type;
- emotion, mood, or mental state;
- psychological traits;
- a diagnosis or risk score;
- biometric voice identity;
- an interpretation of prosody as emotion.

Content generation may use the accepted turn, but the adaptive layer documented here concerns conversation mechanics: pauses, pacing, interruptions, and turn-taking.

## Illustrative policy trace

The public fixture in [`examples/turn_policy_cases.json`](../examples/turn_policy_cases.json) shows two symbolic cases:

1. A possible pause with `extended` pause tolerance remains in listening state.
2. A `SpeechStarted` event while playback is active produces a stop/duck action before any response to the new turn.

These cases document the contract and are synthetic. They are not captured production telemetry and do not establish latency or comparative performance.
