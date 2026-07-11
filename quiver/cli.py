#!/usr/bin/env python3
"""Quiver CLI: keep Hermes aware of its lazy-tool/context optimizer."""
from __future__ import annotations

import argparse
import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import urllib.error
import urllib.request
from dataclasses import dataclass
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_HERMES_HOME = Path(os.environ.get("HERMES_HOME", "/srv/minio/hermes-native/.hermes"))
CATALOG_SLUG = "systems/tool-catalog"
LAZY_SKILL_REL = Path("skills/devops/lazy-tools/SKILL.md")
NIGHTLY_NAME = "lazy-tools-nightly-learn"
BROADHEADS = {
    "browser",
    "session_search",
    "code_execution",
    "vision",
    "video",
    "image_gen",
    "video_gen",
    "x_search",
    "tts",
    "clarify",
}
LIGHT_HEADS = {"web", "terminal", "file", "skills", "todo", "memory", "delegation", "cronjob"}


@dataclass
class Check:
    name: str
    ok: bool
    detail: str = ""
    fix: str = ""
    warn: bool = False

    @property
    def icon(self) -> str:
        if self.ok:
            return "OK"
        return "WARN" if self.warn else "FAIL"


def run(cmd: list[str], *, input_text: str | None = None, timeout: int = 60) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        cmd,
        input=input_text,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=timeout,
        check=False,
    )


def command_exists(name: str) -> bool:
    return shutil.which(name) is not None


def load_catalog_content() -> str:
    seed = REPO_ROOT / "scripts" / "seed-catalog.py"
    spec = importlib.util.spec_from_file_location("quiver_seed_catalog", seed)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load {seed}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)  # type: ignore[union-attr]
    return module.CATALOG_CONTENT


def hermes_home() -> Path:
    return DEFAULT_HERMES_HOME


def installed_skill_path() -> Path:
    return hermes_home() / LAZY_SKILL_REL


def repo_skill_path() -> Path:
    return REPO_ROOT / "skills" / "lazy-tools" / "SKILL.md"


def cron_output() -> str:
    if not command_exists("hermes"):
        return ""
    return run(["hermes", "cron", "list"], timeout=90).stdout


def tool_output() -> str:
    if not command_exists("hermes"):
        return ""
    return run(["hermes", "tools", "list"], timeout=60).stdout


def prompt_size_output() -> str:
    if not command_exists("hermes"):
        return ""
    return run(["hermes", "prompt-size"], timeout=60).stdout


def checks() -> list[Check]:
    out: list[Check] = []
    out.append(Check("hermes command", command_exists("hermes"), shutil.which("hermes") or "missing", "Install Hermes or fix PATH"))
    out.append(Check("gbrain command", command_exists("gbrain"), shutil.which("gbrain") or "missing", "Install GBrain or fix PATH"))
    out.append(Check("quiver repo", (REPO_ROOT / "README.md").exists(), str(REPO_ROOT), "Clone onchito-walks/quiver"))

    skill = installed_skill_path()
    out.append(Check("lazy-tools skill installed", skill.exists(), str(skill), f"quiver install --apply copies {repo_skill_path()}"))

    if command_exists("gbrain"):
        got = run(["gbrain", "get", CATALOG_SLUG], timeout=60)
        out.append(Check("GBrain tool catalog", got.returncode == 0 and "Tool Catalog" in got.stdout, CATALOG_SLUG, "quiver repair --apply seeds catalog"))
    else:
        out.append(Check("GBrain tool catalog", False, "gbrain unavailable", "Install/fix GBrain first"))

    cron = cron_output()
    out.append(Check("nightly fletcher cron", NIGHTLY_NAME in cron, NIGHTLY_NAME, "quiver install --apply creates/updates cron", warn=True))

    tools = tool_output()
    if tools:
        enabled_lines = {line.strip().split()[2] for line in tools.splitlines() if line.strip().startswith("✓ enabled") and len(line.strip().split()) >= 3}
        disabled_lines = {line.strip().split()[2] for line in tools.splitlines() if line.strip().startswith("✗ disabled") and len(line.strip().split()) >= 3}
        missing_light = sorted(LIGHT_HEADS - enabled_lines)
        unsheathed = sorted(BROADHEADS & enabled_lines)
        ok = not missing_light and not unsheathed
        detail = f"enabled={','.join(sorted(enabled_lines))}; broadheads_enabled={','.join(unsheathed) or 'none'}; missing_light={','.join(missing_light) or 'none'}"
        out.append(Check("Hermes tool quiver shape", ok, detail, "quiver install --apply runs hermes tools enable/disable", warn=not ok))
    else:
        out.append(Check("Hermes tool quiver shape", False, "could not read hermes tools", "Run hermes tools list", warn=True))

    ps = prompt_size_output()
    ok_prompt = "15 tools" in ps and "36.9 KB" in ps
    out.append(Check("prompt/tool budget", ok_prompt, next((l.strip() for l in ps.splitlines() if "Tool schemas" in l), "unknown"), "Check Hermes tool config", warn=not ok_prompt))

    th_repo = Path("/home/ubuntu/src/hermes-trailhead")
    th_cmd = shutil.which("hermes-trailhead")
    th_module = th_repo.exists() and (th_repo / "hermes_trailhead" / "cli.py").exists()
    out.append(Check("Trailhead reachable", bool(th_cmd or th_module), th_cmd or str(th_repo), "Install PATH wrapper or clone Trailhead", warn=not bool(th_cmd)))

    return out


def print_checks(items: list[Check]) -> int:
    width = max(len(c.name) for c in items) if items else 0
    hard_fail = False
    for c in items:
        if not c.ok and not c.warn:
            hard_fail = True
        detail = f" — {c.detail}" if c.detail else ""
        print(f"{c.icon:<4} {c.name:<{width}}{detail}")
        if not c.ok and c.fix:
            print(f"     fix: {c.fix}")
    return 1 if hard_fail else 0


def install(apply: bool) -> int:
    print("Quiver install plan")
    actions = [
        "copy lazy-tools skill into active Hermes profile",
        "seed/update GBrain systems/tool-catalog",
        "ensure broadheads are disabled and light heads are enabled",
        "ensure nightly fletcher cron exists",
    ]
    for action in actions:
        print(f"- {action}")
    if not apply:
        print("\nDry run only. Re-run with --apply to mutate Hermes/GBrain.")
        return 0

    return repair(apply=True)


def copy_skill() -> bool:
    src = repo_skill_path()
    dst = installed_skill_path()
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(src.read_text(), encoding="utf-8")
    print(f"copied skill: {src} -> {dst}")
    return True


def seed_catalog_via_mcp(content: str) -> bool:
    """Fallback around GBrain CLI embedding drift; reads bearer token without printing it."""
    config = hermes_home() / "config.yaml"
    if not config.exists():
        print(f"MCP fallback skipped: {config} missing")
        return False
    text = config.read_text(encoding="utf-8")
    try:
        block = text.split("mcp_servers:", 1)[1].split("\n  github:", 1)[0]
        url = re.search(r"url:\s*(\S+)", block).group(1).strip()  # type: ignore[union-attr]
        auth = re.search(r"Authorization:\s*[\"']?([^\"'\n]+)", block).group(1).strip()  # type: ignore[union-attr]
    except Exception:
        print("MCP fallback skipped: could not locate gbrain MCP url/auth in config")
        return False
    payload = {
        "jsonrpc": "2.0",
        "method": "tools/call",
        "id": 1,
        "params": {"name": "put_page", "arguments": {"slug": CATALOG_SLUG, "content": content}},
    }
    request = urllib.request.Request(
        url,
        data=json.dumps(payload).encode(),
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream",
            "Authorization": auth,
        },
        method="POST",
    )
    try:
        raw = urllib.request.urlopen(request, timeout=120).read().decode()
    except urllib.error.URLError as exc:
        print(f"MCP fallback failed: {exc}")
        return False
    ok = "created_or_updated" in raw or '"status":"ok"' in raw
    print("seeded GBrain page via MCP fallback" if ok else "MCP fallback returned unexpected response")
    if not ok:
        print(raw[:1000])
        return False
    # Remote MCP writes skip auto-timeline/auto-links; wire the catalog immediately.
    metadata_calls = [
        ("add_timeline_entry", {
            "slug": CATALOG_SLUG,
            "date": "2026-07-11",
            "summary": "Quiver tool catalog refreshed",
            "detail": "Quiver CLI refreshed systems/tool-catalog for lazy-tool routing and Hermes capability awareness.",
        }),
        ("add_link", {
            "from": CATALOG_SLUG,
            "to": "hermes-moncho/architecture/search-plane-registry",
            "link_type": "routes_research_capability",
        }),
        ("add_link", {
            "from": CATALOG_SLUG,
            "to": "hermes-moncho/architecture/config-autocommit-pipeline",
            "link_type": "documents_sync_invariant",
        }),
    ]
    for idx, (tool, args) in enumerate(metadata_calls, start=2):
        payload = {"jsonrpc": "2.0", "method": "tools/call", "id": idx, "params": {"name": tool, "arguments": args}}
        request = urllib.request.Request(
            url,
            data=json.dumps(payload).encode(),
            headers={"Content-Type": "application/json", "Accept": "application/json, text/event-stream", "Authorization": auth},
            method="POST",
        )
        try:
            urllib.request.urlopen(request, timeout=60).read()
        except urllib.error.URLError as exc:
            print(f"metadata call {tool} failed: {exc}")
            return False
    print("wired GBrain catalog timeline/links")
    return True


def seed_catalog() -> bool:
    content = load_catalog_content()
    if not command_exists("gbrain"):
        print("cannot seed catalog through CLI: gbrain missing; trying MCP fallback")
        return seed_catalog_via_mcp(content)
    proc = run(["gbrain", "put", CATALOG_SLUG], input_text=content, timeout=120)
    if proc.returncode == 0:
        print(f"seeded GBrain page: {CATALOG_SLUG}")
        return True
    print("gbrain put failed; trying MCP fallback. CLI output follows:")
    print(proc.stdout.strip())
    if seed_catalog_via_mcp(content):
        return True
    with tempfile.NamedTemporaryFile("w", delete=False, suffix="-quiver-tool-catalog.md") as fh:
        fh.write(content)
        tmp = fh.name
    print(f"catalog content left at {tmp}")
    return False


def configure_tools() -> bool:
    if not command_exists("hermes"):
        print("cannot configure tools: hermes missing")
        return False
    ok = True
    disable = sorted(BROADHEADS)
    enable = sorted(LIGHT_HEADS)
    proc = run(["hermes", "tools", "disable", *disable], timeout=120)
    print(proc.stdout.strip())
    ok = ok and proc.returncode == 0
    proc = run(["hermes", "tools", "enable", *enable], timeout=120)
    print(proc.stdout.strip())
    ok = ok and proc.returncode == 0
    return ok


def ensure_cron() -> bool:
    if not command_exists("hermes"):
        print("cannot ensure cron: hermes missing")
        return False
    current = cron_output()
    if NIGHTLY_NAME in current:
        print(f"cron present: {NIGHTLY_NAME}")
        return True
    prompt = (REPO_ROOT / "crons" / "nightly-learn-prompt.md").read_text(encoding="utf-8")
    proc = run([
        "hermes", "cron", "create",
        "--name", NIGHTLY_NAME,
        "--schedule", "0 2 * * *",
        "--skills", "lazy-tools",
        "--toolsets", "web,terminal,file,skills,delegation",
        "--prompt", prompt,
    ], timeout=120)
    print(proc.stdout.strip())
    return proc.returncode == 0


def repair(apply: bool) -> int:
    if not apply:
        return print_checks(checks())
    results = [copy_skill(), seed_catalog(), configure_tools(), ensure_cron()]
    print("\nPost-repair doctor:")
    rc = print_checks(checks())
    return 0 if all(results) and rc == 0 else 1


def status(json_mode: bool) -> int:
    items = checks()
    if json_mode:
        print(json.dumps([c.__dict__ | {"status": c.icon} for c in items], indent=2))
        return 0
    return print_checks(items)


def doctor() -> int:
    return print_checks(checks())


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Quiver Hermes integration manager")
    sub = parser.add_subparsers(dest="cmd", required=False)
    sub.add_parser("doctor", help="verify Quiver/Hermes/GBrain integration")
    p_status = sub.add_parser("status", help="show current Quiver integration state")
    p_status.add_argument("--json", action="store_true")
    p_install = sub.add_parser("install", help="install Quiver into the active Hermes profile")
    p_install.add_argument("--apply", action="store_true", help="actually mutate Hermes/GBrain; default is dry-run")
    p_repair = sub.add_parser("repair", help="repair Quiver integration drift")
    p_repair.add_argument("--apply", action="store_true", help="actually repair; default is doctor-only")
    args = parser.parse_args(argv)

    if args.cmd in (None, "doctor"):
        return doctor()
    if args.cmd == "status":
        return status(args.json)
    if args.cmd == "install":
        return install(args.apply)
    if args.cmd == "repair":
        return repair(args.apply)
    parser.print_help()
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
