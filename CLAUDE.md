# Duck$y: notes for AI assistants

**Read [AI_START.md](AI_START.md) first and follow it.** It has the rules, the allowed imports,
code patterns, and how to deliver the work. The person you're helping is most likely a
non-programmer on a phone.

If you can run commands (Claude Code, Codex, Jules, etc.), also:

- Work on a branch, and add or change only `ducksy/features/<name>.py` (plus optionally
  `tests/features/test_<name>.py`). Check the other files in `ducksy/features/` so you don't
  reuse an existing slash command name.
- Before opening the PR, run these and fix failures:
  ```bash
  uv run pytest -q
  uv run python scripts/safety_check.py --root .
  ```
- Open the PR against `nick-gerrard/ducksbucksbot` `main` using `.github/pull_request_template.md`.
  If you can't target the upstream repo, push the branch and tell the user to tap
  **Contribute → Open pull request** on their fork.

Core changes (anything outside `ducksy/features/` and `tests/features/`) are Nick's: run
`uv run ruff format . && uv run ruff check . && uv run pyright && uv run pytest`.
