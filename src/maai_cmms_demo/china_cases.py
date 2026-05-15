"""Utilities for the China industrial examples used in the paper.

These examples are not live integrations. They are small, reviewable data
objects that show how public digitalization signals can be translated into
agentic CMMS/EAM design hypotheses.
"""

from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
from typing import Iterable, List, Optional


@dataclass(frozen=True)
class ChinaIndustrialExample:
    company: str
    sector: str
    public_signal: str
    agentic_eam_implication: str
    candidate_agents: List[str]
    scores: List[int]
    sources: List[str]

    @property
    def mas_fit_score(self) -> float:
        return round(sum(self.scores) / len(self.scores), 2)


def repository_root() -> Path:
    return Path(__file__).resolve().parents[2]


def load_china_examples(path: Optional[Path] = None) -> List[ChinaIndustrialExample]:
    """Load the public-signal example set from JSON."""

    data_path = path or repository_root() / "data" / "china_industrial_examples.json"
    raw = json.loads(data_path.read_text(encoding="utf-8"))
    return [ChinaIndustrialExample(**item) for item in raw["examples"]]


def rank_by_mas_fit(examples: Optional[Iterable[ChinaIndustrialExample]] = None) -> List[ChinaIndustrialExample]:
    """Return examples ranked by their illustrative MAS fit score."""

    items = list(examples or load_china_examples())
    return sorted(items, key=lambda item: item.mas_fit_score, reverse=True)


def summarize_top_examples(limit: int = 5) -> List[dict]:
    """Return a compact summary suitable for demos or notebooks."""

    return [
        {
            "company": item.company,
            "mas_fit_score": item.mas_fit_score,
            "sector": item.sector,
            "candidate_agents": item.candidate_agents,
        }
        for item in rank_by_mas_fit()[:limit]
    ]
