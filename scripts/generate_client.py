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
    python scripts/generate_client.py --patch-only      # re-apply nullable patches only
"""

import argparse
import re
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

    patched = patch_nullable_handling(OUTPUT_DIR / "models")
    print(f"  Patched {patched} DTO file(s) for nullable/enum-empty handling.")
    print(f"  Done. Commit {OUTPUT_DIR.relative_to(REPO_ROOT)}/.")


# ---------------------------------------------------------------------------
# Post-process: patch generator output for two known bugs
# ---------------------------------------------------------------------------
#
# The upstream openapi-python-client (0.28.x) silently mis-parses two
# response patterns that the Pantrist API legitimately produces:
#
#   1. `nullable: true` on a nested $ref property — the generator emits
#      `Nested.from_dict(_value)` without checking for None, so a JSON
#      `null` blows up with `TypeError: 'NoneType' object is not iterable`.
#
#   2. Enum fields where the API returns an empty string `""` — the
#      generator emits `EnumName(_value)` which raises ValueError because
#      `""` is not in the enum's allowed values.
#
# Both patterns appear inside `from_dict` blocks that look like:
#
#       _X = d.pop("...", UNSET)
#       Y: SomeType | Unset
#       if isinstance(_X, Unset):
#           Y = UNSET
#       else:
#           Y = SomeType.from_dict(_X)        # nested $ref
#       # or
#           Y = SomeEnumName(_X)              # enum
#
# The patch broadens the `isinstance(_X, Unset)` guard to also accept
# `None`, and for the enum case to also accept the empty string. After
# the patch, both pieces of malformed JSON normalise to UNSET — which
# the caller already treats as "field absent".


# Captures the four-line block:
#   <indent>if isinstance(_VAR, Unset):
#   <indent>    Y = UNSET
#   <indent>else:
#   <indent>    Y = EXPR(_VAR)               <- either Type.from_dict or Enum
_PARSE_BLOCK_RE = re.compile(
    r"""
    (?P<indent>[ \t]+)
    if\ isinstance\((?P<var>_[A-Za-z_][A-Za-z0-9_]*),\ Unset\):\n
    (?P<unset_line>(?P=indent)[ \t]+[A-Za-z_][A-Za-z0-9_]*\ =\ UNSET\n)
    (?P=indent)else:\n
    (?P=indent)[ \t]+(?P<dst>[A-Za-z_][A-Za-z0-9_]*)\ =\ (?P<call>
        [A-Za-z_][A-Za-z0-9_]*\.from_dict\((?P=var)\)
      | [A-Za-z_][A-Za-z0-9_]*\((?P=var)\)
    )\n
    """,
    re.VERBOSE,
)


def _patch_text(source: str) -> tuple[str, int]:
    """Return (patched_source, replacement_count)."""

    count = 0

    def repl(m: re.Match[str]) -> str:
        nonlocal count
        count += 1
        indent = m["indent"]
        var = m["var"]
        call = m["call"]
        is_enum = ".from_dict(" not in call
        # Universal: also treat JSON null as absent.
        extra = f" or {var} is None"
        if is_enum:
            # Enums also choke on the empty string the API sometimes emits.
            extra += f' or {var} == ""'
        return (
            f"{indent}if isinstance({var}, Unset){extra}:\n"
            f"{m['unset_line']}"
            f"{indent}else:\n"
            f"{indent}    {m['dst']} = {call}\n"
        )

    return _PARSE_BLOCK_RE.sub(repl, source), count


def patch_nullable_handling(models_dir: Path) -> int:
    """Apply the from_dict / enum-empty patch to every generated DTO file.

    Returns the number of files that received at least one replacement.
    """
    if not models_dir.exists():
        return 0
    files_changed = 0
    for path in sorted(models_dir.rglob("*.py")):
        original = path.read_text()
        patched, count = _patch_text(original)
        if count and patched != original:
            path.write_text(patched)
            files_changed += 1
    return files_changed


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
    parser.add_argument(
        "--patch-only",
        action="store_true",
        help="Apply nullable patches to the existing generated client without regenerating",
    )
    args = parser.parse_args()

    if args.patch_only:
        patched = patch_nullable_handling(OUTPUT_DIR / "models")
        print(f"  Patched {patched} model file(s).")
        return

    check_generator()

    if not args.skip_download:
        download_spec(args.url, SPEC_FILE)
    elif not SPEC_FILE.exists():
        sys.exit(f"Error: {SPEC_FILE} not found. Run without --skip-download first.")

    generate(SPEC_FILE)


if __name__ == "__main__":
    main()
