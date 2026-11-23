"""Keep AI_START.md honest: its import list and code examples must match the safety check."""

import ast
import re
import textwrap
from pathlib import Path

from scripts.safety_check import ALLOWED_IMPORTS, check_source

ROOT = Path(__file__).resolve().parent.parent
AI_START = (ROOT / "AI_START.md").read_text()


def test_ai_start_lists_every_allowed_import():
    missing = [m for m in ALLOWED_IMPORTS if f"`{m}`" not in AI_START]
    assert not missing, f"AI_START.md doesn't mention allowed imports: {missing}"


def test_ai_start_examples_pass_the_safety_check():
    blocks = re.findall(r"```python\n(.*?)```", AI_START, re.S)
    assert len(blocks) >= 5
    for code in blocks:
        code = textwrap.dedent(code)
        compile(code, "AI_START.md", "exec", flags=ast.PyCF_ALLOW_TOP_LEVEL_AWAIT)
        assert check_source("AI_START.md", code) == []


def test_docs_link_to_each_other():
    for doc in ("README.md", "CONTRIBUTING.md", "CLAUDE.md", "AGENTS.md"):
        assert "AI_START.md" in (ROOT / doc).read_text() or "GUIDE.md" in (ROOT / doc).read_text()
