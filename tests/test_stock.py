"""Tests for the low-stock rule."""

from custom_components.pantrist.stock import is_low_stock


def _toilet_paper(remaining: float | None) -> dict:
    """One pack of 8 rolls, minimum 3 rolls, opened with ``remaining`` % left."""
    entry = {"pantryUuid": "X", "count": 1}
    if remaining is not None:
        entry |= {"articleIsOpen": True, "remainingAmount": remaining}
    return {
        "manageMinimumAmount": True,
        "minimumAmount": 3,
        "minimumAmountMode": "content",
        "amount": 1,
        "contentVolume": 8,
        "pantrySettings": {"articleList": [entry]},
    }


def test_packages_compare_the_amount() -> None:
    item = {"manageMinimumAmount": True, "amount": 1, "minimumAmount": 1}
    assert is_low_stock(item) is True
    assert is_low_stock({**item, "amount": 2}) is False


def test_unmanaged_item_is_never_low() -> None:
    assert is_low_stock({"amount": 0, "minimumAmount": 1}) is False


def test_content_minimum_counts_rolls() -> None:
    # A full pack: 8 rolls, above a minimum of 3.
    assert is_low_stock(_toilet_paper(None)) is False
    # 50 %: 4 rolls.
    assert is_low_stock(_toilet_paper(50)) is False
    # 37.5 %: exactly 3 rolls, at the minimum.
    assert is_low_stock(_toilet_paper(37.5)) is True
    # 25 %: 2 rolls.
    assert is_low_stock(_toilet_paper(25)) is True


def test_content_minimum_without_package_size_counts_packages() -> None:
    item = {**_toilet_paper(None), "contentVolume": 0}
    # 1 package against a minimum of 3.
    assert is_low_stock(item) is True
