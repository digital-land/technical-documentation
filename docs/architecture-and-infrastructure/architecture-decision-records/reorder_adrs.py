import re
from datetime import datetime
from pathlib import Path

path = Path("index.md")
text = path.read_text(encoding="utf-8")

m = re.search(r"(?ms)\A(.*?)(^##\s+.+$)", text)
if not m:
    raise SystemExit("Couldn't find any ADR headings starting with '##'.")

prefix = m.group(1)
rest = text[len(prefix):]

blocks = re.findall(r"(?ms)(^##\s+.*?)(?=^##\s+|\Z)", rest)

def parse_date(block: str) -> datetime:
    date_match = re.search(
        r"(?im)^\s*(?:\*\*Date\*\*|Date)\s*:\s*([0-9]{4}[-/][0-9]{2}[-/][0-9]{2})\s*$",
        block,
    )
    if not date_match:
        raise ValueError(
            f"Missing Date line in ADR block starting: {block.splitlines()[0]}"
        )
    raw = date_match.group(1).replace("/", "-")
    return datetime.strptime(raw, "%Y-%m-%d")

sorted_blocks = sorted(blocks, key=parse_date, reverse=True)

path.write_text(prefix + "".join(sorted_blocks), encoding="utf-8")
print("Reordered ADRs newest-to-oldest.")
