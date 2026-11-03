"""A pantry item's stock: its batches and when it counts as low."""

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


def batch_fields(item: dict[str, Any]) -> dict[str, Any]:
    """The item's stock batches as HA attributes, the one expiring first first.

    A batch is a group of packages in ``pantrySettings.articleList`` that
    share a best-before date (and storage location). Batches without a date
    come last; ``best_before`` is None for them.
    """
    settings = item.get("pantrySettings") or {}
    batches = [
        {
            "count": entry.get("count"),
            "best_before": entry.get("bestBefore") or None,
            "open": bool(entry.get("articleIsOpen")),
        }
        for entry in settings.get("articleList") or []
        if (entry.get("count") or 0) > 0
    ]
    batches.sort(key=lambda b: (b["best_before"] is None, b["best_before"] or ""))
    return {
        "batches": batches,
        "earliest_best_before": settings.get("earliestBestBefore") or None,
    }


def batch_index(item: dict[str, Any], best_before: str) -> int | None:
    """Index in ``articleList`` of the first stocked batch with that date."""
    entries = (item.get("pantrySettings") or {}).get("articleList") or []
    for index, entry in enumerate(entries):
        if entry.get("bestBefore") == best_before and (entry.get("count") or 0) > 0:
            return index
    return None


def minimum_fields(item: dict[str, Any]) -> dict[str, Any]:
    """The item's minimum as HA attributes, both None when it isn't tracked.

    ``min_amount_mode`` says what ``min_amount`` counts: ``packages``, or
    ``content`` in the item's unit (see ``is_low_stock``).
    """
    if not item.get("manageMinimumAmount"):
        return {"min_amount": None, "min_amount_mode": None}
    return {
        "min_amount": item.get("minimumAmount") or 0,
        "min_amount_mode": item.get("minimumAmountMode") or "packages",
    }
