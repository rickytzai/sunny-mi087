# Sunny — Adaptive Conversation Layer for Voice Agents

**AssemblyAI understands when you speak. Sunny learns how you prefer to converse.**

Sunny is an adaptive voice companion created as **MI-087** for the **AssemblyAI Voice Agent Hackathon**. AssemblyAI supplies real-time speech and turn events. Sunny applies a bounded conversation policy for pause tolerance, interruption behavior, response pacing, and turn-taking.

[View the live demo](https://rickytzai.github.io/sunny-mi087/) · [Watch the final submission film](https://rickytzai.github.io/sunny-mi087/assets/sunny-demo-v4.mp4)

![Sunny in a warm apartment at sunset](assets/sunny-hero.jpg)

> The film is a scripted product visualization with synthesized dialogue. It is not the human evidence recording and contains no raw human audio or transcript.

## The 20-second technical read

| AssemblyAI provides | Sunny Adaptive Layer provides |
| --- | --- |
| `SpeechStarted` | User-specific pause preference |
| Turn events | Response timing preference |
| Real-time speech/timing signals | Interruption and turn-taking preference |
| The signal that new human speech has begun | Playback-yield policy and deterministic fast-path routing |

AssemblyAI detects speech activity and turn boundaries. Sunny uses those events to decide when to keep listening, when to yield playback, and how to pace the next response. Sunny does **not** infer identity, personality, emotion, mental state, or psychological traits.

## Problem

Voice assistants often optimize for answering quickly while missing the rhythm of a real conversation. They may speak through a thinking pause, make interruptions awkward, or apply the same timing policy to every person.

## Solution

Sunny carries a small, bounded set of conversational preferences across turns:

- pause tolerance;
- interruption behavior;
- response pacing;
- conversational turn-taking preference.

A deterministic fast path handles small, time-sensitive decisions. The public repository documents the policy boundary without exposing production credentials, private configuration, human recordings, or transcripts.

## Architecture

~~~mermaid
flowchart LR
    A[Human voice] --> B[AssemblyAI real-time speech]
    B --> C[SpeechStarted + turn events]
    C --> D[Sunny Adaptive Layer]
    P[Bounded conversation preferences] --> D
    D --> E[Deterministic fast path]
    D --> F[Response path]
    E --> G[Playback control]
    F --> G
    G --> H[Speaker]
~~~

The responsibility boundary and event flow are documented in [docs/architecture.md](docs/architecture.md). The preference schema and explicit non-goals are in [docs/adaptation-policy.md](docs/adaptation-policy.md).

## True barge-in

When new human speech begins while playback is active, the documented control flow is:

~~~text
AssemblyAI SpeechStarted
  → Sunny stop/duck playback
  → AssemblyAI new turn
  → Sunny response to the new turn
~~~

The sequence was functionally verified with a human in the loop. No public latency claim is made. See the sanitized [barge-in evidence summary](evidence/barge-in-redacted.json) and [public event example](examples/assemblyai_events.json).

## Evidence status

| Claim | Status | Public evidence | Metric boundary |
| --- | --- | --- | --- |
| Physical human microphone → AssemblyAI events → Sunny → speaker | **VERIFIED FUNCTIONAL** | Evidence ID `20260928_184302`; [redacted summary](evidence/human-e2e-redacted.json) | No latency or accuracy metric published |
| Playback active → `SpeechStarted` → stop/duck → new turn → response | **VERIFIED FUNCTIONAL** | Evidence ID `20260928_184855`; [redacted summary](evidence/barge-in-redacted.json) | No stop-latency metric published |
| Public event ordering and policy-contract fixtures | **VERIFIED SYNTHETIC** | `python -m unittest discover -s tests -v` | Tests documentation fixtures, not the production backend |
| Baseline vs. Sunny benchmark | **NOT YET BENCHMARKED** | None | No comparison numbers claimed |

The verification states above come from completed project validation supplied for this submission. This public snapshot does not independently reproduce the private human session. The full claim-by-claim boundary is in [docs/evidence-status.md](docs/evidence-status.md).

## Public technical evidence

~~~text
docs/
  architecture.md          Responsibility boundary and runtime flow
  adaptation-policy.md     Bounded preferences and explicit non-goals
  evidence-status.md       Verified, synthetic, and unbenchmarked claims
evidence/
  human-e2e-redacted.json  Sanitized functional verification summary
  barge-in-redacted.json   Sanitized barge-in verification summary
examples/
  assemblyai_events.json   Illustrative, non-recorded event sequence
  turn_policy_cases.json   Public policy-contract examples
tests/
  test_public_contract.py  Fixture, ordering, and privacy checks
~~~

The example events and policy cases are explicitly synthetic documentation fixtures. They contain no captured audio, transcript text, user identifiers, or production telemetry.

## Run and verify locally

The demo is a dependency-free static site:

~~~bash
python -m http.server 8000
~~~

Then open `http://localhost:8000`. No API key is needed because the public page does not run the production backend in the browser.

Run the public contract checks with Python 3.9 or later:

~~~bash
python -m unittest discover -s tests -v
~~~

## Proven and next

**Proven for this submission:** human microphone E2E, true human barge-in, bounded personalized turn policy, and deterministic fast-path routing.

**Future product direction:** package the adaptive conversation layer as an SDK/API for voice-agent teams, with potential pricing by conversation minute. This is a direction, not a currently deployed commercial service.

Potential application areas include customer support, accessibility, coaching, interview/intake, and long-form conversational agents.

## Privacy and claim boundary

This repository contains no API keys, credentials, environment files, raw human audio, plaintext human transcripts, private evidence archives, mailbox/shared-state data, or machine-specific paths. See [PRIVACY.md](PRIVACY.md).

Sunny learns bounded conversational preferences—**how you prefer to converse, not who you are**. This repository makes no claim of emotion recognition, identity inference, personality inference, prosody analysis, benchmark superiority, measured latency, production availability, or browser-hosted backend functionality.
