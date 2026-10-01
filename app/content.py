"""Read the repo's content: pages, people, projects, rules, log, code.

Everything the site shows comes from files in this repo. Nothing is written.
"""

import re
from pathlib import Path

import markdown
import yaml

ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "content"
LOG = ROOT / "log"

SLUG = re.compile(r"^[a-z0-9][a-z0-9-]*$")
CODE_SKIP_DIRS = {".git", "__pycache__", ".pytest_cache", ".ruff_cache", ".venv", "venv"}
CODE_SKIP_FILES = re.compile(r"(\.pyc$|^\.env)")


def render_md(text: str) -> str:
    return markdown.markdown(text, extensions=["tables", "fenced_code", "sane_lists"])


def read_md(path: Path) -> tuple[dict, str]:
    """Split a Markdown file into (frontmatter dict, body)."""
    raw = path.read_text(encoding="utf-8")
    if raw.startswith("---\n"):
        end = raw.find("\n---", 4)
        if end != -1:
            meta = yaml.safe_load(raw[4:end]) or {}
            return meta, raw[end + 4 :].lstrip("\n")
    return {}, raw


def _doc(path: Path, slug: str) -> dict:
    meta, body = read_md(path)
    return {
        "slug": slug,
        "title": meta.get("title", slug),
        "visibility": meta.get("visibility", "public"),
        "meta": meta,
        "html": render_md(body),
    }


def page(slug: str) -> dict | None:
    if not SLUG.match(slug):
        return None
    path = CONTENT / "pages" / f"{slug}.md"
    return _doc(path, slug) if path.is_file() else None


def projects() -> list[dict]:
    folder = CONTENT / "projects"
    if not folder.is_dir():
        return []
    return [_doc(p, p.stem) for p in sorted(folder.glob("*.md"))]


def project(slug: str) -> dict | None:
    if not SLUG.match(slug):
        return None
    path = CONTENT / "projects" / f"{slug}.md"
    return _doc(path, slug) if path.is_file() else None


def people() -> dict:
    path = CONTENT / "people.yaml"
    data = yaml.safe_load(path.read_text(encoding="utf-8")) if path.is_file() else {}
    return {"present": data.get("present", []) or [], "past": data.get("past", []) or []}


def rules_html() -> str:
    path = CONTENT / "rules.md"
    return render_md(read_md(path)[1]) if path.is_file() else ""


def claude_md_html() -> str:
    path = ROOT / "CLAUDE.md"
    return render_md(path.read_text(encoding="utf-8")) if path.is_file() else ""


def _split_round(body: str) -> tuple[str, str]:
    """Return (public part, members part) of a round file body."""
    parts = re.split(r"^## Members\s*$", body, maxsplit=1, flags=re.M)
    public = re.sub(r"^## Public\s*$", "", parts[0], count=1, flags=re.M).strip()
    members = parts[1].strip() if len(parts) > 1 else ""
    return public, members


def rounds() -> list[dict]:
    if not LOG.is_dir():
        return []
    out = []
    for path in LOG.glob("round-*.md"):
        meta, body = read_md(path)
        public, members = _split_round(body)
        out.append(
            {
                "number": int(meta.get("round", path.stem.split("-")[-1])),
                "date": str(meta.get("date", "")),
                "title": meta.get("title", ""),
                "commits": meta.get("commits", []) or [],
                "public_html": render_md(public),
                "members_html": render_md(members),
            }
        )
    return sorted(out, key=lambda r: r["number"], reverse=True)


def round_(number: int) -> dict | None:
    return next((r for r in rounds() if r["number"] == number), None)


def code_tree() -> list[str]:
    """Every file in the deployed repo, as relative paths."""
    files = []
    for path in ROOT.rglob("*"):
        rel = path.relative_to(ROOT)
        if any(part in CODE_SKIP_DIRS for part in rel.parts):
            continue
        if path.is_file() and not CODE_SKIP_FILES.search(path.name):
            files.append(rel.as_posix())
    return sorted(files)


def code_file(rel: str) -> str | None:
    """Contents of one repo file, or None if it is outside the tree shown."""
    if rel not in code_tree():
        return None
    try:
        return (ROOT / rel).read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return "(binary file)"
