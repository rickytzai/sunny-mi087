# What actually changes across observations

**VERIFIED: existing offline numerical rhythm prototype. NOT VERIFIED: adaptation inside the live human E2E path.**

The public [executable excerpt](../proof/rhythm_excerpt.py) preserves five methods from the existing `rhythm_adaptation.py` without changing their bodies. The [provenance and replay](../evidence/learning-source-proof.json) records the source hash, per-method AST hashes and matching original/excerpt outputs. Only numerical pause state is retained; companion imports, utterance storage, profile handling and demo dialogue are excluded.

## State -> policy -> later behavior

1. `record_user_pause(pause_ms)` appends an observation to `recent_pauses` (last 10).
2. `_update_avg_pause()` recomputes `avg_user_pause_ms`.
3. `_adapt_next_pause()` sets `next_pause_ms = clamp(current + 0.1 * (mean - current), 50, 2000)` with default configuration.
4. `get_next_pause()` returns the changed delay. The original `simulate_conversation()` consumes it in `time.sleep(pause_before / 1000)` before the next `sunny.turn()`.

| Synthetic observation | Old next-pause policy | New mean | Next response wait selected |
| --- | --- | --- | --- |
| 900 ms | 300 ms | 900 ms | 360 ms |
| 900 ms | 360 ms | 900 ms | 414 ms |
| 100 ms | 414 ms | 633.333 ms | 435.933 ms |

These are deterministic synthetic inputs and computed policy values, **not measured human latency or benchmark results**. The third value still rises because the rolling mean remains above the current policy. A fresh adapter resets to 300 ms; this is in-memory state, not verified cross-session personalization.

Run `python -m unittest discover -s tests -v`. Tests execute the source excerpt, check the changing output, bounds, rolling window and source-method provenance. A static JSON expectation alone is not the proof.

## Scope limits discovered in the source audit

- The live microphone/barge-in harness calls `Sunny` directly; it does not wire in `RhythmAdapter`. Human E2E validates voice flow, not learning.
- `_update_eot_signals()` in the original is a stub. Learned end-of-turn patterns are **NOT_IMPLEMENTED** there.
- The original initializes state to 300 ms and fixes its deque at 10; `baseline_pause_ms` and `measurement_window` are not applied by the constructor. The excerpt preserves these limitations.
- Response-length learning, persisted preferences and live preference accuracy are **NOT_ENOUGH_EVIDENCE**.
- The published proof consumes numerical pauses only. Identity, voiceprints, personality and emotion inference are out of scope.

## Reviewer terminology audit

**JEF: OMITTED_NOT_SUPPORTED.** The existing `JevFastPath` is a rule-based intent router with fallback. It is not the proposed evidence-to-policy feedback loop. We do not rename it JEF or claim the proposed WAIT/RESPOND/INTERRUPT/FAST/REASON pipeline.

**Relationship-aware preference distillation: OMITTED_NOT_SUPPORTED.** The separate synthetic `PersonaDistiller` has no relationship-context policy. It also contains broader profile/mood fields, so it is not published or represented as a privacy-bounded preference implementation. Relationship-aware preference distillation remains future work, outside this submission's verified contribution.

The narrow supported wording is: **Sunny's offline rhythm prototype updates a bounded next-response pause policy from pause observations.**
