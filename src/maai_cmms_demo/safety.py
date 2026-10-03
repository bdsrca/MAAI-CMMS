"""Safety checks between untrusted text, model output, and tool execution."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Tuple

from .models import ToolAction


PROMPT_INJECTION_PATTERNS: Tuple[str, ...] = (
    "ignore previous instructions",
    "ignore all previous instructions",
    "system prompt",
    "developer message",
    "bypass policy",
    "disable safety",
    "reveal secrets",
    "show api key",
    "exfiltrate",
)

DEFAULT_TOOL_ALLOWLIST = frozenset(
    {
        ("cmms", "draft_work_order"),
        ("inventory", "reserve_part_draft"),
    }
)


@dataclass(frozen=True)
class TextSafetyResult:
    safe: bool
    matched_patterns: Tuple[str, ...]


def screen_untrusted_text(*values: str) -> TextSafetyResult:
    text = "\n".join(value or "" for value in values).lower()
    matches = tuple(pattern for pattern in PROMPT_INJECTION_PATTERNS if pattern in text)
    return TextSafetyResult(safe=not matches, matched_patterns=matches)


def _is_draft_operation(operation: str) -> bool:
    return operation.startswith("draft_") or operation.endswith("_draft")


def validate_tool_action(
    action: ToolAction,
    *,
    allowlist: Iterable[tuple[str, str]] = DEFAULT_TOOL_ALLOWLIST,
    dry_run_only: bool = True,
) -> None:
    allowed = set(allowlist)
    key = (action.system, action.operation)
    if key not in allowed:
        raise PermissionError(f"Tool action is not allowlisted: {action.system}.{action.operation}")
    if dry_run_only and not _is_draft_operation(action.operation):
        raise PermissionError("Only draft/dry-run tool operations are allowed in this demo.")
    if not action.requires_approval:
        raise PermissionError("Demo tool actions must require human approval.")
