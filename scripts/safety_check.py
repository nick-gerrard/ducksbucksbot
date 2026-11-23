"""Safety gate for pull requests from friends.

It never imports or runs the code it checks: it only reads files and parses them with `ast`.
CI runs the copy of this script from `main` (pull_request_target), so a PR can't switch it off.

Two checks:
  1. Paths: a friend's PR may only add or change files in ducksy/features/ and tests/features/.
     Anything else (the bot core, dependencies, CI, deploy config) needs Nick.
  2. Code: every feature file may only import from an allow-list and may not use the
     escape hatches below (files, processes, network, the bot's token, Python internals).

This is a guard-rail against AI mistakes and casual misuse, not a perfect sandbox. The real
boundaries are the systemd sandbox on the server and the bot's limited Discord permissions.

Usage:
  python -I scripts/safety_check.py --root <pr checkout> [--changed-files FILE] [--owner]
Exit code 0 = OK, 1 = problems found (printed as Markdown).
"""

from __future__ import annotations

import argparse
import ast
import re
import sys
from pathlib import Path

# Files a friend's PR may touch: Python files directly inside these folders (no subfolders).
FRIEND_PATHS = re.compile(r"(ducksy/features|tests/features)/[A-Za-z0-9_]+\.py")
MAX_FEATURE_LINES = 600

ALLOWED_IMPORTS = {
    "__future__",
    "asyncio",
    "collections",
    "dataclasses",
    "datetime",
    "discord",
    "discord.app_commands",
    "discord.ext",
    "discord.ext.commands",
    "discord.ext.tasks",
    "discord.ui",
    "ducksy.ducksbucks",
    "ducksy.settings",
    "ducksy.storage",
    "enum",
    "functools",
    "itertools",
    "json",
    "logging",
    "math",
    "random",
    "re",
    "statistics",
    "string",
    "textwrap",
    "typing",
    "zoneinfo",
}
ALLOWED_IMPORT_PREFIXES = ("ducksy.features.",)

BANNED_NAMES = {
    "eval": "runs arbitrary code",
    "exec": "runs arbitrary code",
    "compile": "builds code at runtime",
    "__import__": "imports modules around the allow-list",
    "open": "reads or writes files (use ducksy.storage.Store to remember things)",
    "globals": "reaches into Python internals",
    "locals": "reaches into Python internals",
    "vars": "reaches into Python internals",
    "getattr": "looks attributes up by string, which hides what the code does",
    "setattr": "sets attributes by string, which hides what the code does",
    "delattr": "deletes attributes by string, which hides what the code does",
    "breakpoint": "pauses the bot",
    "input": "waits forever for keyboard input",
    "exit": "stops the bot",
    "quit": "stops the bot",
}

# Attribute names that are off limits whatever object they're on.
BANNED_ATTRS = {
    # the bot's credentials and raw connections
    "token": "the bot's secret token",
    "http": "the bot's raw HTTP client (holds the token)",
    "ws": "the bot's raw gateway connection",
    # files: discord.File can upload any file the bot can read
    "File": "uploads files from disk",
    # modules that leak through other modules (e.g. discord.utils.os)
    **{
        m: "reaches a module that isn't allowed"
        for m in (
            "os",
            "sys",
            "subprocess",
            "socket",
            "shutil",
            "pathlib",
            "builtins",
            "importlib",
            "ctypes",
            "pickle",
            "marshal",
            "signal",
            "platform",
            "aiohttp",
            "requests",
            "urllib",
            "io",
            "tempfile",
            "multiprocessing",
            "threading",
            "inspect",
            "gc",
        )
    },
    # asyncio's process and raw network helpers
    **{
        a: "starts processes or opens raw network connections"
        for a in (
            "create_subprocess_exec",
            "create_subprocess_shell",
            "subprocess_exec",
            "subprocess_shell",
            "open_connection",
            "open_unix_connection",
            "start_server",
            "start_unix_server",
            "create_connection",
            "create_server",
            "create_datagram_endpoint",
            "sock_connect",
            "run_in_executor",
            "to_thread",
        )
    },
    # destructive server actions
    "leave": "makes the bot leave the server",
    "ban": "bans people",
    "kick": "kicks people",
    "prune_members": "kicks inactive people",
    "close": "shuts the bot down",
    "change_presence": "changes the bot's status for everyone (ask Nick)",
}


def _is_allowed_import(module: str) -> bool:
    return module in ALLOWED_IMPORTS or module.startswith(ALLOWED_IMPORT_PREFIXES)


def _is_super_init(node: ast.Attribute) -> bool:
    return (
        node.attr == "__init__"
        and isinstance(node.value, ast.Call)
        and isinstance(node.value.func, ast.Name)
        and node.value.func.id == "super"
        and not node.value.args
    )


def check_source(path: str, source: str) -> list[str]:
    """Problems in one feature file, as human-readable strings."""
    try:
        tree = ast.parse(source, filename=path)
    except SyntaxError as e:
        return [f"`{path}` line {e.lineno}: Python can't read this file ({e.msg})"]

    problems: list[str] = []

    def bad(node: ast.AST, msg: str) -> None:
        problems.append(f"`{path}` line {getattr(node, 'lineno', '?')}: {msg}")

    if source.count("\n") > MAX_FEATURE_LINES:
        problems.append(f"`{path}`: over {MAX_FEATURE_LINES} lines; split it into smaller features")

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if not _is_allowed_import(alias.name):
                    bad(node, f"imports `{alias.name}`, which features can't use")
        elif isinstance(node, ast.ImportFrom):
            if node.level:  # relative import
                bad(node, "uses a relative import; import from `ducksy.` instead")
                continue
            mod = node.module or ""
            if (
                mod == "ducksy"
            ):  # `from ducksy import storage` is the same as `import ducksy.storage`
                for alias in node.names:
                    if not _is_allowed_import(f"ducksy.{alias.name}"):
                        bad(node, f"imports `ducksy.{alias.name}`, which features can't use")
                continue
            if not _is_allowed_import(mod):
                bad(node, f"imports from `{mod}`, which features can't use")
            for alias in node.names:
                full = f"{mod}.{alias.name}"
                if alias.name == "*":
                    bad(node, f"uses `from {mod} import *`; import names one by one")
                elif alias.name in BANNED_ATTRS or alias.name.startswith("_"):
                    bad(node, f"imports `{full}`: {BANNED_ATTRS.get(alias.name, 'private name')}")
        elif isinstance(node, ast.Name):
            if node.id in BANNED_NAMES:
                bad(node, f"uses `{node.id}`: {BANNED_NAMES[node.id]}")
            elif node.id.startswith("__") and node.id not in ("__name__", "__doc__"):
                bad(node, f"uses `{node.id}`, a Python internal")
        elif isinstance(node, ast.Attribute):
            if _is_super_init(node):
                continue  # `super().__init__(...)` is how you set up a discord.ui.View
            if node.attr.startswith("_"):
                bad(node, f"uses `.{node.attr}`: private and internal attributes are off limits")
            elif node.attr in BANNED_ATTRS:
                bad(node, f"uses `.{node.attr}`: {BANNED_ATTRS[node.attr]}")
    return problems


def check_paths(changed: list[str]) -> list[str]:
    problems = []
    for f in changed:
        if not FRIEND_PATHS.fullmatch(f):
            problems.append(f"`{f}` is outside the features folder, so Nick needs to review it")
    return problems


def feature_files(root: Path) -> list[Path]:
    """Bot code that runs on the server. (Tests only run in CI, so they aren't scanned.)"""
    return sorted(p for p in root.glob("ducksy/features/*.py") if p.is_file() or p.is_symlink())


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", type=Path, required=True, help="checkout of the PR")
    ap.add_argument("--changed-files", type=Path, help="file listing changed paths, one per line")
    ap.add_argument(
        "--owner", action="store_true", help="PR is from the repo owner: skip path rule"
    )
    args = ap.parse_args(argv)

    problems: list[str] = []
    if args.changed_files and not args.owner:
        changed = [ln.strip() for ln in args.changed_files.read_text().splitlines() if ln.strip()]
        problems += check_paths(sorted(set(changed)))
    for p in feature_files(args.root):
        if p.is_symlink():
            problems.append(
                f"`{p.relative_to(args.root)}` is a symlink; features must be plain files"
            )
            continue
        problems += check_source(str(p.relative_to(args.root)), p.read_text(errors="replace"))

    if problems:
        print("### 🦆 Safety check: needs changes or a review from Nick\n")
        for prob in problems:
            print(f"- {prob}")
        print(
            "\nIf you're using an AI assistant, paste this list into it and ask it to fix "
            "the feature without the things listed. See CONTRIBUTING.md for what features can use."
        )
        return 1
    print(
        "### 🦆 Safety check passed\n\nOnly feature files changed, and they only use allowed tools."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
