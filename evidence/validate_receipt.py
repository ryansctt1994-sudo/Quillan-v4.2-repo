#!/usr/bin/env python3
"""Validate Quillan evidence receipts.

Uses the repository JSON Schema when the optional jsonschema package is available,
then performs integrity checks that JSON Schema alone cannot express.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "evidence" / "schema" / "evidence-receipt-v1.schema.json"
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")


def canonical_bytes_without_receipt_hash(receipt: dict) -> bytes:
    clone = json.loads(json.dumps(receipt))
    integrity = clone.setdefault("integrity", {})
    integrity.pop("receipt_sha256", None)
    return (
        json.dumps(clone, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
        .encode("utf-8")
    )


def compute_receipt_sha256(receipt: dict) -> str:
    return hashlib.sha256(canonical_bytes_without_receipt_hash(receipt)).hexdigest()


def fallback_validate(receipt: dict) -> list[str]:
    errors: list[str] = []
    required = {
        "schema", "receipt_id", "run_id", "claim_ids", "repository", "commit",
        "timestamp_utc", "producer", "environment", "invocation", "outcome",
        "artifacts", "integrity",
    }
    missing = sorted(required - receipt.keys())
    if missing:
        errors.append(f"missing required fields: {', '.join(missing)}")

    if receipt.get("schema") != "quillan-evidence-receipt-v1":
        errors.append("schema must be quillan-evidence-receipt-v1")
    if receipt.get("repository") != "ryansctt1994-sudo/Quillan-v4.2-repo":
        errors.append("unexpected repository")
    if not re.fullmatch(r"[0-9a-f]{40}", str(receipt.get("commit", ""))):
        errors.append("commit must be a 40-character lowercase git SHA")
    if receipt.get("outcome", {}).get("status") not in {"PASS", "FAIL", "ERROR", "BLOCKED", "SKIPPED"}:
        errors.append("invalid outcome.status")

    for i, artifact in enumerate(receipt.get("artifacts", [])):
        digest = artifact.get("sha256", "")
        if not SHA256_RE.fullmatch(str(digest)):
            errors.append(f"artifacts[{i}].sha256 is invalid")

    return errors


def validate_receipt(path: Path, verify_integrity: bool = True) -> list[str]:
    receipt = json.loads(path.read_text(encoding="utf-8"))
    errors: list[str] = []

    try:
        import jsonschema  # type: ignore
    except ImportError:
        errors.extend(fallback_validate(receipt))
    else:
        schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
        validator = jsonschema.Draft202012Validator(schema)
        for err in sorted(validator.iter_errors(receipt), key=lambda e: list(e.path)):
            loc = ".".join(str(x) for x in err.path) or "<root>"
            errors.append(f"{loc}: {err.message}")

    if verify_integrity:
        recorded = receipt.get("integrity", {}).get("receipt_sha256")
        if recorded:
            actual = compute_receipt_sha256(receipt)
            if recorded != actual:
                errors.append(
                    f"receipt_sha256 mismatch: recorded={recorded} actual={actual}"
                )

    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("receipt", type=Path)
    parser.add_argument("--no-integrity", action="store_true")
    args = parser.parse_args()

    errors = validate_receipt(args.receipt, verify_integrity=not args.no_integrity)
    if errors:
        for error in errors:
            print(f"INVALID: {error}", file=sys.stderr)
        return 1

    print(f"VALID: {args.receipt}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
