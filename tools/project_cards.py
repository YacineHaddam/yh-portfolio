"""Macros for the Projects section, used via the `macros` plugin.

- `project_cards()` renders every page under `<docs_dir>/projects/` (except
  `index.md`) as a card, so a new project appears on the index without editing it.
- `project_links()` renders a project page's `links` front matter (repo, demo).
"""

from pathlib import Path

import yaml

LINK_LABELS = {"repo": "Repository", "demo": "Demo"}


def read_front_matter(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---", 4)
    return (yaml.safe_load(text[4:end]) or {}) if end != -1 else {}


def render_card(page: Path, meta: dict) -> str:
    tech = " ".join(f"`{name}`" for name in meta.get("tech", []))
    return (
        f"-   __[{meta['title']}]({page.name})__\n\n"
        f"    ---\n\n"
        f"    {meta['summary']}\n\n"
        f"    {tech}"
    )


def render_cards(docs_dir: Path) -> str:
    pages = sorted((docs_dir / "projects").glob("*.md"))
    cards = [
        render_card(page, meta)
        for page in pages
        if page.name != "index.md" and (meta := read_front_matter(page))
    ]
    return '<div class="grid cards" markdown>\n\n' + "\n\n".join(cards) + "\n\n</div>"


def render_links(links: dict) -> str:
    items = [f"- [{LINK_LABELS[key]}]({url})" for key, url in links.items() if key in LINK_LABELS]
    return "\n".join(items)


def define_env(env) -> None:
    @env.macro
    def project_cards() -> str:
        return render_cards(Path(env.conf["docs_dir"]))

    @env.macro
    def project_links() -> str:
        return render_links(env.page.meta.get("links") or {})
