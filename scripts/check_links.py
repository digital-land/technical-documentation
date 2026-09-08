#!/usr/bin/env python3
"""Check internal links in docs/ resolve to a page that exists.

Every markdown file under docs/ becomes a page on the site, so a link written as
a site-absolute path (/section/page) must match one of those pages. Links to
images, assets, anchors and external URLs are left alone.

Run with `make check-links`. Exits non-zero and lists every bad link, so a
rename that leaves links behind fails CI instead of silently shipping.
"""

import re
import sys
from pathlib import Path

DOCS = Path(__file__).resolve().parent.parent / "docs"
IGNORED_PREFIXES = ("/images", "/assets")
LINK = re.compile(r"\[([^\]]*)\]\(\s*(/[^)\s]*?)\s*\)")


def page_url(path: Path) -> str:
    """The site path Eleventy will publish this markdown file at."""
    rel = path.relative_to(DOCS).as_posix()
    rel = re.sub(r"\.md$", "", rel)
    rel = re.sub(r"(^|/)index$", r"\1", rel)
    return "/" + rel.rstrip("/")


def suggest(target: str, pages: set) -> str:
    """Best guess at what a broken link meant, for the error message."""
    slug = target.rstrip("/").split("/")[-1].removesuffix(".md")
    if not slug:
        return ""
    matches = sorted(p for p in pages if p.rstrip("/").endswith("/" + slug))
    return f"  did you mean {matches[0]} ?" if len(matches) == 1 else ""


def main() -> int:
    files = sorted(DOCS.rglob("*.md"))
    pages = {page_url(f) for f in files}
    # A directory with an index.md is also reachable with a trailing slash.
    pages |= {p + "/" for p in pages}

    broken = []
    for f in files:
        for match in LINK.finditer(f.read_text(encoding="utf-8", errors="ignore")):
            text, target = match.group(1), match.group(2)
            if target.startswith(IGNORED_PREFIXES):
                continue
            if target.split("#")[0].rstrip("/") in {p.rstrip("/") for p in pages}:
                continue
            broken.append((f.relative_to(DOCS).as_posix(), text.strip(), target))

    if not broken:
        print(f"check-links: {len(files)} files, no broken internal links")
        return 0

    print(f"check-links: {len(broken)} broken internal link(s)\n", file=sys.stderr)
    for path, text, target in broken:
        print(f"  {path}", file=sys.stderr)
        print(f"    [{text}]({target}){suggest(target, pages)}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
