#!/usr/bin/env python3
"""Run the first Quillan claim-linked structural evidence bundle."""

from __future__ import annotations

from contextlib import redirect_stderr, redirect_stdout
from datetime import datetime, timezone
import hashlib
import io
import json
import os
from pathlib import Path
import platform
import subprocess
import sys
import unittest

import torch

from validate_receipt import compute_receipt_sha256, validate_receipt


ROOT = Path(__file__).resolve().parents[1]
RUN_ID = os.environ.get("QUILLAN_RUN_ID", "QRUN-000002")
RECEIPT_ID = os.environ.get("QUILLAN_RECEIPT_ID", "QREC-000002")
CLAIMS = ["Q-MODEL-002", "Q-MODEL-003", "Q-MODEL-004"]


def git_output(*args: str) -> str | None:
    try:
        return subprocess.check_output(
            ["git", *args],
            cwd=ROOT,
            stderr=subprocess.DEVNULL,
            text=True,
        ).strip()
    except Exception:
        return None


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    commit = os.environ.get("GITHUB_SHA") or git_output("rev-parse", "HEAD")
    if not commit or len(commit) != 40:
        print("Unable to resolve exact 40-character git commit.", file=sys.stderr)
        return 2

    branch = (
        os.environ.get("GITHUB_HEAD_REF")
        or os.environ.get("GITHUB_REF_NAME")
        or git_output("branch", "--show-current")
        or None
    )
    # Generated caches/artifacts are expected; only tracked modifications make the tested checkout dirty.
    dirty = bool(git_output("status", "--porcelain", "--untracked-files=no"))

    run_dir = ROOT / "evidence" / "runs" / RUN_ID
    receipt_dir = ROOT / "evidence" / "receipts" / "bundles"
    run_dir.mkdir(parents=True, exist_ok=True)
    receipt_dir.mkdir(parents=True, exist_ok=True)

    suite = unittest.defaultTestLoader.discover(
        str(ROOT / "eval" / "structural"),
        pattern="test_*.py",
    )
    stream = io.StringIO()
    with redirect_stdout(stream), redirect_stderr(stream):
        result = unittest.TextTestRunner(stream=stream, verbosity=2).run(suite)
    report_text = stream.getvalue()

    report_path = run_dir / "structural-test-report.txt"
    report_path.write_text(report_text, encoding="utf-8")

    results = {
        "schema": "quillan-structural-result-v1",
        "run_id": RUN_ID,
        "claim_ids": CLAIMS,
        "commit": commit,
        "tests_run": result.testsRun,
        "failures": len(result.failures),
        "errors": len(result.errors),
        "skipped": len(result.skipped),
        "successful": result.wasSuccessful(),
        "test_report": "structural-test-report.txt",
    }
    result_path = run_dir / "structural-results.json"
    result_path.write_text(
        json.dumps(results, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    status = "PASS" if result.wasSuccessful() else "FAIL"
    exit_code = 0 if result.wasSuccessful() else 1

    receipt = {
        "schema": "quillan-evidence-receipt-v1",
        "receipt_id": RECEIPT_ID,
        "run_id": RUN_ID,
        "claim_ids": CLAIMS,
        "repository": "ryansctt1994-sudo/Quillan-v4.2-repo",
        "commit": commit,
        "branch": branch,
        "dirty_worktree": dirty,
        "timestamp_utc": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "producer": {
            "kind": "ci" if os.environ.get("GITHUB_ACTIONS") == "true" else "local",
            "name": "github-actions" if os.environ.get("GITHUB_ACTIONS") == "true" else platform.node(),
            "workflow_run": os.environ.get("GITHUB_RUN_ID"),
            "independent_of_project_author": False,
        },
        "implementation": {
            "entrypoint": "Quillan-v4.2-model/quillan_council_enhanced.py",
            "config_path": "eval/structural/test_enhanced_council.py::FixtureConfig",
            "checkpoint": None,
        },
        "environment": {
            "python": platform.python_version(),
            "platform": platform.platform(),
            "torch": torch.__version__,
            "cuda": torch.version.cuda,
            "device": "cpu",
            "dependency_lock_sha256": None,
        },
        "invocation": {
            "command": "python evidence/run_structural_evidence.py",
            "working_directory": ".",
            "seed": "1337/2026 fixture seeds",
            "dataset_id": "synthetic-structural-fixture",
            "dataset_sha256": None,
            "config_sha256": None,
        },
        "outcome": {
            "status": status,
            "exit_code": exit_code,
            "supports_state": "EXECUTED" if result.wasSuccessful() else "IMPLEMENTED",
            "summary": (
                "Structural checks executed successfully; Q-MODEL-002 through Q-MODEL-004 meet the EXECUTED gate."
                if result.wasSuccessful()
                else "One or more claim-linked structural checks failed."
            ),
            "measurements": {
                "tests_run": result.testsRun,
                "failures": len(result.failures),
                "errors": len(result.errors),
                "skipped": len(result.skipped),
            },
            "acceptance": {
                "criterion": "All four structural guard tests pass; this receipt advances only Q-MODEL-002 through Q-MODEL-004.",
                "met": result.wasSuccessful(),
            },
        },
        "artifacts": [
            {
                "path": str(report_path.relative_to(ROOT)),
                "sha256": sha256_file(report_path),
                "kind": "stdout",
            },
            {
                "path": str(result_path.relative_to(ROOT)),
                "sha256": sha256_file(result_path),
                "kind": "result",
            },
        ],
        "integrity": {
            "receipt_sha256_policy": "Hash canonical UTF-8 JSON with integrity.receipt_sha256 omitted.",
            "receipt_sha256": None,
        },
        "notes": [
            "This run exercises a tiny synthetic configuration and does not use a trained checkpoint.",
            "Q-MODEL-001 remains IMPLEMENTED because canonical model/config designation is unresolved.",
            "A PASS supports EXECUTED only for Q-MODEL-002 through Q-MODEL-004.",
            "This is internal CI evidence, not independent reproduction.",
        ],
    }

    receipt["integrity"]["receipt_sha256"] = compute_receipt_sha256(receipt)
    receipt_path = receipt_dir / f"{RUN_ID}.json"
    receipt_path.write_text(
        json.dumps(receipt, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    validation_errors = validate_receipt(receipt_path)
    if validation_errors:
        for error in validation_errors:
            print(f"RECEIPT INVALID: {error}", file=sys.stderr)
        return 2

    print(report_text)
    print(f"RESULT: {result_path.relative_to(ROOT)}")
    print(f"RECEIPT: {receipt_path.relative_to(ROOT)}")
    print(f"RECEIPT_SHA256: {receipt['integrity']['receipt_sha256']}")
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
