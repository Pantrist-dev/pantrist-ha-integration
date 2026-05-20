import os

import pytest

from credentials import Credentials, clear, load, save


@pytest.fixture
def creds_path(tmp_path, monkeypatch):
    path = tmp_path / "credentials.json"
    monkeypatch.setattr("credentials.CREDS_PATH", str(path))
    return path


def test_load_returns_none_when_file_missing(creds_path):
    assert load() is None


def test_save_and_load_roundtrip(creds_path):
    save(Credentials(refresh_token="rt", list_id="list-1"))
    loaded = load()
    assert loaded == Credentials(refresh_token="rt", list_id="list-1")


def test_save_leaves_no_tmp_files_after_success(creds_path):
    save(Credentials(refresh_token="rt1", list_id="list-1"))
    assert not list(creds_path.parent.glob("*.tmp"))


def test_load_recovers_from_corrupt_file(creds_path):
    creds_path.write_text("not json")
    assert load() is None
    assert creds_path.with_suffix(".corrupt").exists()
    assert not creds_path.exists()


def test_clear_removes_file(creds_path):
    save(Credentials(refresh_token="rt", list_id="list-1"))
    assert creds_path.exists()
    clear()
    assert not creds_path.exists()


def test_clear_is_noop_when_missing(creds_path):
    clear()  # should not raise
