# Contributing

**Friends: start with [GUIDE.md](GUIDE.md).** It walks you through building a feature from your
phone with an AI agent (Claude Code, Codex or Jules) that opens the PR for you. No coding or
computer needed.

**AI assistants:** read [AI_START.md](AI_START.md). It's the full brief: rules, patterns and
how to hand the work over.

**Nick / core changes:** run `uv run ruff format . && uv run ruff check . && uv run pyright &&
uv run pytest` before pushing. If you change what features may use, update
`scripts/safety_check.py`, AI_START.md and GUIDE.md §6 together; `tests/test_docs.py` checks
that the import list in AI_START.md matches the safety check.

**Adding a friend:** Settings → Collaborators → Add people (Write role), or
`gh api -X PUT repos/nick-gerrard/ducksbucksbot/collaborators/<username> -f permission=push`.
Every PR still needs your approval (CODEOWNERS + branch protection); tags are admin-only.
