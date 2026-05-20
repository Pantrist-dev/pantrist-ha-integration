"""Persistent storage for the addon's OAuth credentials."""

from __future__ import annotations

import json
import logging
import os
from dataclasses import asdict, dataclass
from pathlib import Path

logger = logging.getLogger(__name__)

CREDS_PATH = "/data/credentials.json"


@dataclass(frozen=True)
class Credentials:
    refresh_token: str
    list_id: str


def load() -> Credentials | None:
    path = Path(CREDS_PATH)
    if not path.exists():
        return None
    try:
        data = json.loads(path.read_text())
        return Credentials(
            refresh_token=data["refresh_token"], list_id=data["list_id"]
        )
    except (json.JSONDecodeError, KeyError, TypeError):
        corrupt_path = path.with_suffix(".corrupt")
        logger.warning("Credentials file corrupt; moving to %s", corrupt_path)
        try:
            path.rename(corrupt_path)
        except OSError:
            logger.exception("Could not rename corrupt credentials file")
        return None


def save(creds: Credentials) -> None:
    path = Path(CREDS_PATH)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".tmp")
    tmp.write_text(json.dumps(asdict(creds)))
    os.replace(tmp, path)


def clear() -> None:
    path = Path(CREDS_PATH)
    if path.exists():
        path.unlink()
