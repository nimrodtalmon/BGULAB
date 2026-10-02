"""Read the repo's content: pages, people, rules, log, code.

Everything the site shows comes from files in this repo. Nothing is written.
"""

import html
import re
from pathlib import Path

import markdown
import yaml

ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "content"
LOG = ROOT / "log"

SLUG = re.compile(r"^[a-z0-9][a-z0-9-]*$")
LAB_ONLY = re.compile(r"\s*\(lab only\)\s*$", re.I)
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


def anchor(title: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")


def _split(text: str, level: int) -> tuple[str, list[tuple[str, str]]]:
    """Split Markdown at headings of one level, ignoring code fences.

    Returns (text before the first heading, [(heading, text under it), ...]).
    """
    mark = "#" * level + " "
    intro, parts, fence = [], [], False
    for line in text.splitlines():
        if line.startswith("```"):
            fence = not fence
        if not fence and line.startswith(mark):
            parts.append([line[len(mark):].strip(), []])
        elif parts:
            parts[-1][1].append(line)
        else:
            intro.append(line)
    return "\n".join(intro), [(h, "\n".join(b)) for h, b in parts]


def _summary(title: str, lab: bool) -> str:
    tag = ' <span class="tag">lab only</span>' if lab else ""
    return f"<summary>{html.escape(title)}{tag}</summary>"


def fold(body: str, lab: bool) -> str:
    """Render a page with every `##` (and nested `###`) section collapsed.

    A heading ending in "(lab only)" is shown only to signed-in lab members.
    The top `#` heading becomes the page title and is dropped here.
    """
    body = re.sub(r"\A\s*# .*\n", "", body)
    intro, sections = _split(body, 2)
    out = [render_md(intro)]
    for title, text in sections:
        hidden = bool(LAB_ONLY.search(title))
        if hidden and not lab:
            continue
        title = LAB_ONLY.sub("", title)
        sub_intro, subs = _split(text, 3)
        inner = [render_md(sub_intro)]
        for sub_title, sub_text in subs:
            sub_hidden = bool(LAB_ONLY.search(sub_title))
            if sub_hidden and not lab:
                continue
            sub_title = LAB_ONLY.sub("", sub_title)
            inner.append(f'<details class="sub" id="{anchor(sub_title)}">'
                         f"{_summary(sub_title, sub_hidden)}{render_md(sub_text)}</details>")
        out.append(f'<details id="{anchor(title)}">{_summary(title, hidden)}'
                   f'{"".join(inner)}</details>')
    return "\n".join(out)


def page(slug: str) -> dict | None:
    if not SLUG.match(slug):
        return None
    path = CONTENT / "pages" / f"{slug}.md"
    if not path.is_file():
        return None
    meta, body = read_md(path)
    visibility = meta.get("visibility", "public")
    return {
        "slug": slug,
        "title": meta.get("title", slug),
        "lab_only": visibility in ("lab", "members"),
        "body": body,
    }


# People are shown grouped by role, in this order. Within a group, the order
# of people.yaml is kept: earliest first (new people are appended).
ROLE_GROUPS = [
    ("PI", ("pi",)),
    ("Postdocs", ("postdoc",)),
    ("PhD students", ("phd student", "phd")),
    ("MSc students", ("msc student", "msc")),
]
OTHER_GROUP = "Other"


def group_people(people: list) -> list:
    """[(heading, [person, ...]), ...] in ROLE_GROUPS order; empty groups dropped."""
    groups = {h: [] for h, _ in ROLE_GROUPS}
    groups[OTHER_GROUP] = []
    for p in people:
        role = str(p.get("role", "")).strip().lower()
        heading = next((h for h, roles in ROLE_GROUPS if role in roles), OTHER_GROUP)
        groups[heading].append(p)
    return [(h, ps) for h, ps in groups.items() if ps]


def people() -> dict:
    path = CONTENT / "people.yaml"
    data = yaml.safe_load(path.read_text(encoding="utf-8")) if path.is_file() else {}
    present = data.get("present", []) or []
    past = data.get("past", []) or []
    return {
        "present": present,
        "past": past,
        "present_groups": group_people(present),
        "past_groups": group_people(past),
    }


def footer_html() -> str:
    path = CONTENT / "footer.md"
    return render_md(read_md(path)[1]) if path.is_file() else ""


def rules_html() -> str:
    path = CONTENT / "rules.md"
    return render_md(read_md(path)[1]) if path.is_file() else ""


def claude_md_html() -> str:
    path = ROOT / "CLAUDE.md"
    return render_md(path.read_text(encoding="utf-8")) if path.is_file() else ""


def _split_round(body: str) -> tuple[str, str]:
    """Return (public part, lab part) of a round file body."""
    parts = re.split(r"^## (?:Lab|Members)\s*$", body, maxsplit=1, flags=re.M)
    public = re.sub(r"^## Public\s*$", "", parts[0], count=1, flags=re.M).strip()
    lab = parts[1].strip() if len(parts) > 1 else ""
    return public, lab


def rounds() -> list[dict]:
    if not LOG.is_dir():
        return []
    out = []
    for path in LOG.glob("round-*.md"):
        meta, body = read_md(path)
        public, lab = _split_round(body)
        out.append(
            {
                "number": int(meta.get("round", path.stem.split("-")[-1])),
                "date": str(meta.get("date", "")),
                "title": meta.get("title", ""),
                "commits": meta.get("commits", []) or [],
                "public_html": render_md(public),
                "lab_html": render_md(lab),
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
