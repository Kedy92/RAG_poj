from __future__ import annotations

from dataclasses import dataclass
import re


@dataclass(frozen=True)
class ClassificationResult:
    program_area: str
    geography: str
    donor_type: str
    target_group: str
    outcomes: list[str]
    indicators: list[str]
    confidence: float


FIELD_PATTERNS = {
    "program_area": re.compile(r"program area:\s*(.+)", re.IGNORECASE),
    "geography": re.compile(r"country:\s*(.+)", re.IGNORECASE),
    "donor_type": re.compile(r"donor type:\s*(.+)", re.IGNORECASE),
    "target_group": re.compile(r"target group:\s*(.+)", re.IGNORECASE),
}


def classify_application(text: str) -> ClassificationResult:
    fields = {
        field: _match_field(pattern, text)
        for field, pattern in FIELD_PATTERNS.items()
    }
    outcomes = _extract_list_after_label("Expected outcomes", text)
    indicators = _extract_indicators(text)
    filled_fields = sum(1 for value in fields.values() if value != "unknown")
    confidence = (filled_fields + bool(outcomes) + bool(indicators)) / 6

    return ClassificationResult(
        program_area=fields["program_area"],
        geography=fields["geography"],
        donor_type=fields["donor_type"],
        target_group=fields["target_group"],
        outcomes=outcomes,
        indicators=indicators,
        confidence=round(confidence, 2),
    )


def _match_field(pattern: re.Pattern[str], text: str) -> str:
    match = pattern.search(text)
    if not match:
        return "unknown"
    return match.group(1).strip().rstrip(".")


def _extract_list_after_label(label: str, text: str) -> list[str]:
    pattern = re.compile(rf"{label}:\s*(.+)", re.IGNORECASE)
    match = pattern.search(text)
    if not match:
        return []
    return [item.strip().rstrip(".") for item in match.group(1).split(",") if item.strip()]


def _extract_indicators(text: str) -> list[str]:
    marker = "indicators related to"
    lowered = text.lower()
    start = lowered.find(marker)
    if start == -1:
        return []
    sentence = text[start + len(marker):].split(".", maxsplit=1)[0]
    return [item.strip() for item in re.split(r",| and ", sentence) if item.strip()]
