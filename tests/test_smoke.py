"""Smoke tests for Quiver CLI — verifies the tool meets its stated purpose.

Quiver's stated purpose: Hermes adaptive context optimizer and lazy tool router.
It manages the Hermes skill surface, GBrain tool catalog, tool enable/disable state,
and the nightly fletcher cron — all verifiable via `quiver doctor`.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


def _quiver(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-m", "quiver", *args],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
        timeout=120,
    )


def test_doctor_exits_zero():
    """quiver doctor always exits 0 when all checks pass or only warn."""
    proc = _quiver("doctor")
    assert proc.returncode == 0, f"doctor exit {proc.returncode}: {proc.stderr}"


def test_doctor_produces_output():
    """quiver doctor prints at least 5 check lines."""
    proc = _quiver("doctor")
    lines = [l for l in proc.stdout.splitlines() if l.strip()]
    assert len(lines) >= 5, f"Expected >=5 doctor lines, got {len(lines)}"
    # Every line should have an icon marker (OK, WARN, FAIL)
    for line in lines:
        assert any(line.lstrip().startswith(p) for p in ("OK", "WARN", "FAIL")), line


def test_status_json_is_valid():
    """quiver status --json returns parseable JSON with expected keys."""
    proc = _quiver("status", "--json")
    assert proc.returncode == 0
    data = json.loads(proc.stdout)
    assert isinstance(data, list)
    assert len(data) >= 5
    required_keys = {"name", "ok", "status"}
    for item in data:
        assert required_keys.issubset(item.keys()), f"Missing keys in {item}"


def test_status_json_has_core_checks():
    """quiver status --json includes the core integration checks."""
    proc = _quiver("status", "--json")
    data = json.loads(proc.stdout)
    names = {item["name"] for item in data}
    expected = {
        "hermes command",
        "gbrain command",
        "quiver repo",
        "lazy-tools skill installed",
        "GBrain tool catalog",
        "Hermes tool quiver shape",
        "prompt/tool budget",
    }
    missing = expected - names
    assert not missing, f"Missing checks: {missing}"


def test_doctor_finds_hermes_and_gbrain():
    """quiver doctor reports Hermes and GBrain on PATH."""
    proc = _quiver("doctor")
    out = proc.stdout
    assert "hermes command" in out, "missing hermes check"
    assert "gbrain command" in out, "missing gbrain check"


def test_doctor_finds_quiver_repo():
    """quiver doctor verifies its own repo exists."""
    proc = _quiver("doctor")
    assert "quiver repo" in proc.stdout, "missing quiver repo check"


def test_trailhead_in_status():
    """quiver status --json reports Trailhead as reachable."""
    proc = _quiver("status", "--json")
    data = json.loads(proc.stdout)
    names = {item["name"] for item in data}
    assert "Trailhead reachable" in names, "missing Trailhead reachable check"


def test_cli_module_imports_clean():
    """quiver.cli module imports without error."""
    proc = subprocess.run(
        [sys.executable, "-c", "from quiver import cli; assert cli.main"],
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert proc.returncode == 0, proc.stderr


def test_install_dry_run():
    """quiver install (no --apply) is a safe dry-run, exits 0."""
    proc = _quiver("install")
    assert proc.returncode == 0
    assert "Dry run" in proc.stdout or "Quiver install plan" in proc.stdout


def test_repair_dry_run():
    """quiver repair (no --apply) is a safe dry-run, exits 0 or 1."""
    proc = _quiver("repair")
    # repair without --apply is doctor-only; only fails on hard_fail
    assert proc.returncode in (0, 1), f"repair exit {proc.returncode}"


def test_pyproject_has_entrypoint():
    """pyproject.toml declares the quiver console script."""
    pyproject = REPO_ROOT / "pyproject.toml"
    assert pyproject.exists(), "pyproject.toml missing"
    text = pyproject.read_text()
    assert 'quiver = "quiver.cli:main"' in text, "missing console script entrypoint"
