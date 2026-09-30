"""Numerical excerpt of the existing offline RhythmAdapter prototype.
No human data, provider connection, persistence, or new adaptation algorithm.
See docs/learning-proof.md for provenance and integration limits.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from collections import deque

from typing import Optional

@dataclass
class RhythmConfig:
    """Configuration for rhythm adaptation."""
    # Baseline pause before responding (ms)
    baseline_pause_ms: float = 300.0
    # Minimum pause (never go below this)
    min_pause_ms: float = 50.0
    # Maximum pause (never exceed this)
    max_pause_ms: float = 2000.0
    # Adaptation rate (how fast to adjust to user rhythm)
    adaptation_rate: float = 0.1
    # Interruptibility threshold (0-1)
    interruptibility_threshold: float = 0.5
    # Window size for pause measurement
    measurement_window: int = 10

@dataclass
class RhythmState:
    recent_pauses: deque = field(default_factory=lambda: deque(maxlen=10))
    avg_user_pause_ms: float = 300.0
    next_pause_ms: float = 300.0

class RhythmAdapter:
    def __init__(self, config: Optional[RhythmConfig] = None):
        self.config = config or RhythmConfig()
        self.state = RhythmState()
        self.persona_profile: Optional[object] = None

    def record_user_pause(self, pause_ms: float):
        """Record a user pause duration."""
        self.state.recent_pauses.append(pause_ms)
        self._update_avg_pause()
        self._adapt_next_pause()

    def _update_avg_pause(self):
        if self.state.recent_pauses:
            self.state.avg_user_pause_ms = sum(self.state.recent_pauses) / len(self.state.recent_pauses)

    def _adapt_next_pause(self):
        """Adapt next pause based on user's rhythm."""
        target = self.state.avg_user_pause_ms
        current = self.state.next_pause_ms
        # Smooth adaptation
        adapted = current + (target - current) * self.config.adaptation_rate
        # Clamp to bounds
        self.state.next_pause_ms = max(
            self.config.min_pause_ms,
            min(self.config.max_pause_ms, adapted)
        )

    def get_next_pause(self) -> float:
        """Get the adapted pause for next bot response."""
        return self.state.next_pause_ms
