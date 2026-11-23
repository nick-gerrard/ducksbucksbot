# Duck$y: notes for AI assistants

**Read [AI_START.md](AI_START.md) first and follow it.** It covers the rules, the allowed
imports, code patterns, and how to open the PR. The person you're helping is most likely a
non-programmer on a phone and a collaborator on this repo: work on a branch here and open the
PR into `main` yourself.

Core changes (anything outside `ducksy/features/` and `tests/features/`) are Nick's. Before
pushing those, run
`uv run ruff format . && uv run ruff check . && uv run pyright && uv run pytest`.

Repo secrets: there are none, and keep it that way. Collaborators can run any workflow from
their own branches, so a secret added to this repo could be read by any of them.
