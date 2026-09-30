# Architecture and responsibility boundary

Sunny is an adaptive conversation layer built on real-time speech events from AssemblyAI. The separation below is the central technical claim of this public snapshot.

| Component | Responsibility | Does not claim |
| --- | --- | --- |
| AssemblyAI real-time speech | Produce speech activity and turn events such as `SpeechStarted` and turn completion | Sunny-specific personalization or playback policy |
| Sunny event adapter | Normalize provider events for the conversation controller | Speech recognition model ownership |
| Sunny Adaptive Layer | Apply bounded pause, interruption, pacing, and turn-taking preferences | Identity, personality, emotion, or psychological inference |
| Deterministic fast path | Make small event-driven control decisions, including yielding playback on new speech | General reasoning or new user-facing features |
| Response path | Continue from the accepted human turn with the current bounded preferences | A public browser-hosted production service |
| Playback controller | Start, stop, or duck audio according to the selected turn action | A published latency guarantee |

## Event flow

~~~mermaid
sequenceDiagram
    participant H as Human
    participant A as AssemblyAI
    participant S as Sunny Adaptive Layer
    participant P as Playback

    H->>A: Live microphone speech
    A->>S: SpeechStarted / turn events
    S->>S: Apply bounded turn policy
    S->>P: Play response
    H->>A: New speech during playback
    A->>S: SpeechStarted
    S->>P: Stop or duck
    A->>S: New completed turn
    S->>P: Respond to new turn
~~~

The sequence describes responsibility and ordering. It is not a latency chart. The repository does not publish a `SpeechStarted`-to-stop duration because the available public-safe evidence does not support that measurement.

## Public snapshot limits

This repository is a sanitized review surface rather than the private runtime repository. It includes the architecture boundary, redacted verification summaries, synthetic event examples, and contract tests. It excludes credentials, provider configuration, raw recordings, transcripts, production logs, private evidence archives, and operational infrastructure.
