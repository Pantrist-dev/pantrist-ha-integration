#!/usr/bin/env python3
"""
Fetch the Pantrist OpenAPI spec and regenerate the Python client used by the
Custom Integration.

The generated package lands at:
    custom_components/pantrist/pantrist_client/

Prerequisites (one-time):
    pip install openapi-python-client

Usage:
    python scripts/generate_client.py
    python scripts/generate_client.py --url https://api.pantrist.app/swagger-ui-yaml
    python scripts/generate_client.py --skip-download   # use cached openapi-watch.yaml
"""

import argparse
import shutil
import subprocess
import sys
import tempfile
import urllib.request
from pathlib import Path

SPEC_URL = "https://api.pantrist.app/swagger-ui-for-app-json"

REPO_ROOT = Path(__file__).resolve().parent.parent
SPEC_FILE = REPO_ROOT / "openapi-watch.json"
OUTPUT_DIR = REPO_ROOT / "custom_components/pantrist/pantrist_client"
PACKAGE_NAME = "pantrist_client"


def _progress(url: str, dest: Path, label: str) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)

    def _hook(count: int, block: int, total: int) -> None:
        if total > 0:
            pct = min(100, count * block * 100 // total)
            print(f"\r  {label}: {pct:3d}%", end="", flush=True)

    urllib.request.urlretrieve(url, dest, reporthook=_hook)
    print()


def download_spec(url: str, dest: Path) -> None:
    print(f"Fetching spec from {url}…")
    _progress(url, dest, dest.name)
    print(f"  Saved to {dest}")


def check_generator() -> None:
    if subprocess.run(
        [sys.executable, "-m", "openapi_python_client", "--version"],
        capture_output=True,
    ).returncode != 0:
        sys.exit(
            "Error: openapi-python-client not found.\n"
            "Install it with:  pip install openapi-python-client"
        )


def generate(spec: Path) -> None:
    print(f"Generating Python client → {OUTPUT_DIR.relative_to(REPO_ROOT)}")
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        result = subprocess.run(
            [
                sys.executable, "-m", "openapi_python_client",
                "generate",
                "--path", str(spec),
                "--output-path", str(tmp_path / PACKAGE_NAME),
                "--overwrite",
            ],
            cwd=tmp,
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            print(result.stdout)
            print(result.stderr, file=sys.stderr)
            sys.exit("openapi-python-client exited with errors.")

        generated = tmp_path / PACKAGE_NAME
        if not generated.exists():
            candidates = list(tmp_path.rglob(PACKAGE_NAME))
            if candidates:
                generated = candidates[0]
            else:
                sys.exit(f"Could not find generated package in {tmp_path}.")

        # openapi-python-client wraps the package in a project directory:
        #   pantrist_client/          <- project (README, pyproject.toml)
        #     pantrist_client/        <- actual importable package (__init__.py)
        # We only want the inner package so COPY app/ . in Docker makes it importable.
        inner = generated / PACKAGE_NAME
        if inner.exists() and (inner / "__init__.py").exists():
            generated = inner

        if OUTPUT_DIR.exists():
            shutil.rmtree(OUTPUT_DIR)
        shutil.copytree(generated, OUTPUT_DIR)

    print(f"  Done. Commit {OUTPUT_DIR.relative_to(REPO_ROOT)}/.")


def main() -> None:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--url", default=SPEC_URL, help="OpenAPI spec URL")
    parser.add_argument(
        "--skip-download",
        action="store_true",
        help="Regenerate from the existing openapi-watch.yaml without fetching",
    )
    args = parser.parse_args()

    check_generator()

    if not args.skip_download:
        download_spec(args.url, SPEC_FILE)
    elif not SPEC_FILE.exists():
        sys.exit(f"Error: {SPEC_FILE} not found. Run without --skip-download first.")

    generate(SPEC_FILE)


if __name__ == "__main__":
    main()
