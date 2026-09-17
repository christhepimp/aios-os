"""Phase 0 AIOS shell: intent in, allowlisted tools out."""

from __future__ import annotations

import os
import shlex
import subprocess
from pathlib import Path

MEMORY_FILE = Path.home() / ".aios_memory.txt"
ALLOWED_BINARIES = {"echo", "uname", "pwd", "ls", "date", "whoami", "id"}


def remember(text: str) -> str:
    MEMORY_FILE.parent.mkdir(parents=True, exist_ok=True)
    with MEMORY_FILE.open("a", encoding="utf-8") as fh:
        fh.write(text.strip() + "\n")
    return f"remembered: {text.strip()}"


def recall() -> str:
    if not MEMORY_FILE.exists():
        return "i don't remember anything yet."
    body = MEMORY_FILE.read_text(encoding="utf-8").strip()
    return body or "i don't remember anything yet."


def run_allowed(command: str) -> str:
    parts = shlex.split(command)
    if not parts:
        return "nothing to run."
    binary = Path(parts[0]).name
    if binary not in ALLOWED_BINARIES:
        return f"blocked: '{binary}' is not in the AIOS allowlist."
    try:
        completed = subprocess.run(
            parts,
            check=False,
            capture_output=True,
            text=True,
            timeout=10,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return f"failed: {exc}"
    out = (completed.stdout or "") + (completed.stderr or "")
    return out.strip() or f"exit {completed.returncode}"


def interpret(line: str) -> str:
    text = line.strip()
    low = text.lower()

    if not text:
        return ""
    if low in {"exit", "quit"}:
        return "__exit__"
    if low in {"help", "?"}:
        return (
            "AIOS phase 0. Try: where am i | list files | run echo hello | "
            "remember that ... | what do you remember | help | quit"
        )
    if "where am i" in low or low in {"pwd", "cwd"}:
        return str(Path.cwd())
    if low.startswith("list file") or low in {"ls", "list"}:
        return "\n".join(sorted(os.listdir("."))) or "(empty)"
    if low.startswith("remember that "):
        return remember(text[len("remember that ") :])
    if low.startswith("remember "):
        return remember(text[len("remember ") :])
    if "what do you remember" in low or low in {"memory", "recall"}:
        return recall()
    if low.startswith("run "):
        return run_allowed(text[4:])
    return (
        "i heard you, but phase 0 only maps a few intents. "
        "type help. later this becomes an LLM-backed supervisor."
    )


def main() -> None:
    print("AIOS 0.1 — userspace layer. not a kernel. type help.")
    while True:
        try:
            line = input("aios> ")
        except (EOFError, KeyboardInterrupt):
            print()
            break
        result = interpret(line)
        if result == "__exit__":
            break
        if result:
            print(result)
