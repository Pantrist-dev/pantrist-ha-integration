"""When a pantry item counts as low on stock."""

from __future__ import annotations

from typing import Any


def _effective_packages(item: dict[str, Any]) -> float:
    """Packages left, open ones by their fill level (``remainingAmount`` in %)."""
    entries = (item.get("pantrySettings") or {}).get("articleList") or []
    consumed = sum(
        1 - (entry.get("remainingAmount") or 0) / 100
        for entry in entries
        if entry.get("articleIsOpen")
    )
    return (item.get("amount") or 0) - consumed


def is_low_stock(item: dict[str, Any]) -> bool:
    """True when a tracked item is at or below its minimum.

    ``minimumAmount`` counts packages, unless ``minimumAmountMode`` is
    ``content``: then it counts the content of the packages in the item's
    unit (3 rolls out of packs of 8), open packages by their fill level.
    """
    if not item.get("manageMinimumAmount"):
        return False
    minimum = item.get("minimumAmount") or 0
    content_volume = item.get("contentVolume") or 0
    if item.get("minimumAmountMode") == "content" and content_volume > 0:
        content = round(_effective_packages(item) * content_volume, 6)
        return content <= minimum
    return (item.get("amount") or 0) <= minimum
