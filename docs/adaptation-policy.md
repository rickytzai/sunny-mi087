# Bounded pause policy

The supported adaptive mechanism is the existing **offline** `RhythmAdapter`, not an automatically learning live backend. See [executable proof and limits](learning-proof.md).

It keeps the last ten numerical pause observations, recomputes their mean, and smooths the next-pause policy toward that mean. The default update rate is 0.1 and the output is clamped to 50–2000 ms. These are configuration/policy values, not measured system latency.

The original simulation consumes the updated value before the next response. Human E2E/barge-in verification does not validate that integration. There is no verified cross-session persistence; learned end-of-turn patterns are a stub.

The symbolic pause, pacing, interruption and turn-taking labels in `examples/turn_policy_cases.json` are legacy synthetic design fixtures. They do not implement learning or prove production equivalence.

Only numerical pause state is public. No identity, personality, emotion, voiceprint or psychological inference is included. Relationship-aware preference distillation and JEF feedback-loop claims are omitted.
