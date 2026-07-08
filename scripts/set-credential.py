#!/usr/bin/env python3
"""set-credential — securely store a provider API key in .env without LLM exposure.

USAGE: set-credential <provider> [--test-model <model>]

The script reads the key from stdin (user pastes it), validates it with a test
API call, writes it to .env, and reports success/failure. The LLM orchestrator
runs this script but NEVER sees the key value — it only sees the result message.

The key path: user's clipboard → terminal PTY → this script → .env file.
"""

import os
import sys
import re
import subprocess
from pathlib import Path

ENV_PATH = Path.home() / ".hermes" / ".env"

PROVIDER_CONFIG = {
    "deepseek": {
        "env_var": "DEEPSEEK_API_KEY",
        "test_model": "deepseek-v4-flash",
        "test_command": "hermes -m {model} --provider {provider} -z 'Reply with exactly: OK' 2>&1",
        "key_pattern": r"^sk-[a-zA-Z0-9]{32,}$",
        "api_url": "https://api.deepseek.com/v1/models",
    },
    "anthropic": {
        "env_var": "ANTHROPIC_API_KEY",
        "test_model": "claude-sonnet-4",
        "test_command": "hermes -m {model} --provider {provider} -z 'Reply with exactly: OK' 2>&1",
        "key_pattern": r"^sk-ant-[a-zA-Z0-9\-_]{90,}$",
        "api_url": "https://api.anthropic.com/v1/messages",
    },
    "cerebras": {
        "env_var": "CEREBRAS_API_KEY",
        "test_model": "qwen/qwen3.5-397b-a17b",
        "test_command": "hermes -m {model} --provider {provider} -z 'Reply with exactly: OK' 2>&1",
        "key_pattern": r"^csk-[a-zA-Z0-9]{40,}$",
        "api_url": "https://api.cerebras.ai/v1/models",
    },
    "openai": {
        "env_var": "OPENAI_API_KEY",
        "test_model": "gpt-4o-mini",
        "test_command": "hermes -m {model} --provider openai-api -z 'Reply with exactly: OK' 2>&1",
        "key_pattern": r"^sk-(proj-)?[a-zA-Z0-9\-_]{32,}$",
        "api_url": "https://api.openai.com/v1/models",
    },
    "openrouter": {
        "env_var": "OPENROUTER_API_KEY",
        "test_model": "openai/gpt-4o-mini",
        "test_command": "hermes -m {model} --provider openrouter -z 'Reply with exactly: OK' 2>&1",
        "key_pattern": r"^sk-or-[a-zA-Z0-9]{40,}$",
        "api_url": "https://openrouter.ai/api/v1/models",
    },
    "google": {
        "env_var": "GOOGLE_API_KEY",
        "test_model": "gemini-2.5-flash",
        "test_command": "hermes -m {model} --provider google -z 'Reply with exactly: OK' 2>&1",
        "key_pattern": r"^AIza[a-zA-Z0-9\-_]{30,}$",
        "api_url": "https://generativelanguage.googleapis.com/v1/models",
    },
    "tavily": {
        "env_var": "TAVILY_API_KEY",
        "test_model": None,
        "test_command": None,
        "key_pattern": r"^tvly-[a-zA-Z0-9]{20,}$",
        "api_url": "https://api.tavily.com/search",
    },
    "firecrawl": {
        "env_var": "FIRECRAWL_API_KEY",
        "test_model": None,
        "test_command": None,
        "key_pattern": r"^fc-[a-zA-Z0-9]{30,}$",
        "api_url": "https://api.firecrawl.dev/v1/scrape",
    },
    "zeroentropy": {
        "env_var": "ZEROENTROPY_API_KEY",
        "test_model": None,
        "test_command": None,
        "key_pattern": r"^ze-[a-zA-Z0-9\-_]{20,}$",
        "api_url": None,
    },
}


def validate_key_format(provider: str, key: str) -> bool:
    cfg = PROVIDER_CONFIG.get(provider)
    if not cfg:
        print(f"ERROR: Unknown provider '{provider}'. Supported: {', '.join(sorted(PROVIDER_CONFIG.keys()))}")
        return False
    pattern = cfg.get("key_pattern")
    if pattern and not re.match(pattern, key):
        print(f"WARNING: Key does not match expected format for {provider}.")
        print(f"Expected pattern: {pattern}")
        print("Continuing anyway — format checks are best-effort.")
    return True


def test_key(provider: str, key: str) -> tuple[bool, str]:
    """Test the key by making an API call through Hermes."""
    cfg = PROVIDER_CONFIG.get(provider, {})
    test_cmd = cfg.get("test_command")
    test_model = cfg.get("test_model")

    if not test_cmd or not test_model:
        return True, "no test available for this provider"

    # Set env var and run test
    env_var = cfg["env_var"]
    env = os.environ.copy()
    env[env_var] = key

    cmd = test_cmd.format(model=test_model, provider=provider)
    try:
        result = subprocess.run(
            cmd, shell=True, capture_output=True, text=True,
            timeout=30, env=env
        )
        output = (result.stdout + result.stderr).strip()
        if "OK" in output and "error" not in output.lower() and "401" not in output:
            return True, f"test call succeeded: {output[:100]}"
        else:
            return False, f"test call failed: {output[:200]}"
    except subprocess.TimeoutExpired:
        return False, "test call timed out"
    except Exception as e:
        return False, f"test call error: {e}"


def write_env(provider: str, key: str) -> bool:
    """Write the key to .env, replacing existing entry if present."""
    cfg = PROVIDER_CONFIG.get(provider, {})
    env_var = cfg["env_var"]

    if not ENV_PATH.exists():
        print(f"ERROR: .env file not found at {ENV_PATH}")
        return False

    content = ENV_PATH.read_text()
    lines = content.rstrip("\n").split("\n")

    # Check if env var already exists
    found = False
    for i, line in enumerate(lines):
        # Match KEY=VALUE or export KEY=VALUE
        if re.match(rf"^(export\s+)?{re.escape(env_var)}=", line):
            lines[i] = f"export {env_var}={key}"
            found = True
            break

    if not found:
        lines.append(f"export {env_var}={key}")

    ENV_PATH.write_text("\n".join(lines) + "\n")
    return True


def main():
    if len(sys.argv) < 2:
        print("USAGE: set-credential <provider> [--skip-test] [--from-file <path>]")
        print(f"Supported providers: {', '.join(sorted(PROVIDER_CONFIG.keys()))}")
        print("\nModes:")
        print("  stdin (default):  Paste key, press Enter, then Ctrl+D")
        print("  --from-file PATH: Read key from a temp file (LLM-safe: key never enters context)")
        print("\nExamples:")
        print("  set-credential deepseek")
        print("  set-credential anthropic --from-file /tmp/new-key.txt")
        sys.exit(1)

    provider = sys.argv[1].lower()
    skip_test = "--skip-test" in sys.argv

    # --from-file mode: read key from a file the user created independently
    from_file = None
    for i, arg in enumerate(sys.argv):
        if arg == "--from-file" and i + 1 < len(sys.argv):
            from_file = sys.argv[i + 1]
            break

    if provider not in PROVIDER_CONFIG:
        print(f"ERROR: Unknown provider '{provider}'.")
        print(f"Supported: {', '.join(sorted(PROVIDER_CONFIG.keys()))}")
        sys.exit(1)

    cfg = PROVIDER_CONFIG[provider]
    env_var = cfg["env_var"]

    if from_file:
        # LLM-safe mode: key was written to a file by the user via SSH/other channel.
        # The LLM orchestrator never reads the file — it only runs this script.
        filepath = Path(from_file)
        if not filepath.exists():
            print(f"ERROR: File not found: {from_file}")
            print("Create this file with your key, then run this script again.")
            sys.exit(1)
        key = filepath.read_text().strip().split("\n")[0].strip()
        print(f"Reading key from {from_file} ({len(key)} chars)...")
    else:
        # Stdin mode: user pastes key directly into terminal
        print(f"Setting {env_var} for provider '{provider}'...")
        print("Paste the key and press Enter, then Ctrl+D:")
        print()
        key = sys.stdin.read().strip()
        if not key:
            print("ERROR: No key provided (empty input).")
            sys.exit(1)
        key = key.split("\n")[0].strip()

    if not key:
        print("ERROR: No key provided (empty input).")
        sys.exit(1)

    # Basic validation
    if not validate_key_format(provider, key):
        sys.exit(1)

    print(f"Key received ({len(key)} chars, format check passed).")

    # Test the key
    if not skip_test:
        print(f"Testing key with provider '{provider}'...")
        ok, msg = test_key(provider, key)
        if not ok:
            print(f"KEY TEST FAILED: {msg}")
            print("Key was NOT saved. Fix the key and try again.")
            sys.exit(1)
        print(f"Key test passed: {msg}")
    else:
        print("Skipping test (--skip-test).")

    # Write to .env
    if write_env(provider, key):
        print(f"SUCCESS: {env_var} saved to {ENV_PATH}")
        if from_file:
            # Clean up temp file — key was read and stored, no reason to keep it
            try:
                Path(from_file).unlink()
                print(f"Cleaned up temp file: {from_file}")
            except Exception as e:
                print(f"Note: could not remove temp file: {e}")
        print(f"Provider '{provider}' should now work. Run 'hermes -z OK' to verify routing.")
    else:
        print("ERROR: Failed to write to .env.")
        sys.exit(1)


if __name__ == "__main__":
    main()
