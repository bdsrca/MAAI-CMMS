"""Provider-neutral LLM boundary for the MAAI-CMMS demo.

The default implementation is deterministic and offline. Real providers can be
integrated behind the same interface, but model output never receives direct
permission to execute tools.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class LLMRequest:
    system_prompt: str
    user_input: str
    context: str = ""


@dataclass(frozen=True)
class LLMResponse:
    text: str
    provider: str
    model: str


class LLMAdapter(Protocol):
    def complete(self, request: LLMRequest) -> LLMResponse:
        """Return model text only. Tool execution is handled elsewhere."""


class DeterministicLLMAdapter:
    """Offline adapter used by tests and demos.

    It intentionally performs no network calls and needs no credentials.
    """

    provider = "local"
    model = "deterministic-stub"

    def complete(self, request: LLMRequest) -> LLMResponse:
        summary = request.user_input.strip() or "No request text provided."
        return LLMResponse(
            text=f"Draft analysis only: {summary}",
            provider=self.provider,
            model=self.model,
        )
