import csv
import io
import json
import os
import sys

BASE_DIR = os.path.dirname(sys.executable) if getattr(sys, 'frozen', False) else os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "game_data.json")

DEFAULT_DATA = {"available": {}, "pending": []}


def load_data():
    if not os.path.exists(DATA_FILE):
        save_data(DEFAULT_DATA)
        return DEFAULT_DATA.copy()
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def migrate_old_data(data):
    """Add name_zh/name_en/name_ja fields to entries that lack them.
    Returns True if data was modified."""
    changed = False
    for key, info in data.get("available", {}).items():
        if "name_zh" not in info:
            info["name_zh"] = key
            info.setdefault("name_en", "")
            info.setdefault("name_ja", "")
            changed = True
    if changed:
        save_data(data)
    return changed


# ── Import helpers ────────────────────────────────────────────

def read_import_file(filepath):
    """Read a file trying common encodings. Returns content str or None."""
    for enc in ("utf-8-sig", "utf-8", "gbk", "gb2312", "cp936"):
        try:
            with open(filepath, "r", encoding=enc) as f:
                return f.read()
        except UnicodeDecodeError:
            continue
    return None


def parse_import_rows(content):
    """Parse CSV or TSV content into a list of row lists."""
    lines = [ln for ln in content.splitlines() if ln.strip()]
    if not lines:
        return []
    first = lines[0]
    if first.count("\t") >= 2 and first.count("\t") >= first.count(","):
        return [[c.strip() for c in ln.split("\t")] for ln in lines]
    return [[c.strip() for c in row] for row in csv.reader(io.StringIO(content))]


def row_to_game_entry(row):
    """Convert a parsed row to (name_zh, name_en, name_ja, system, launch) or None."""
    if len(row) >= 5:
        return row[0].strip(), row[1].strip(), row[2].strip(), row[3].strip(), row[4].strip()
    if len(row) >= 3:
        return row[0].strip(), "", "", row[1].strip(), row[2].strip()
    return None


def build_game_record(name_zh, name_en, name_ja, system, launch):
    """Create a standardized game record dict."""
    return {
        "name_zh": name_zh,
        "name_en": name_en if name_en != "/" else "",
        "name_ja": name_ja if name_ja != "/" else "",
        "system": system,
        "launch": launch,
    }


def import_games(data, rows):
    """Import parsed rows into data. Returns (added, skipped, error_line).
    error_line is 0 if no error, otherwise the 1-based line number."""
    added = 0
    skipped = 0
    for line_num, row in enumerate(rows, start=1):
        if not row or all(c.strip() == "" for c in row):
            continue
        parsed = row_to_game_entry(row)
        if parsed is None:
            return added, skipped, line_num
        name_zh, name_en, name_ja, system, launch = parsed
        if not name_zh:
            continue
        if name_zh in data["available"]:
            skipped += 1
            continue
        data["available"][name_zh] = build_game_record(name_zh, name_en, name_ja, system, launch)
        if name_zh in data["pending"]:
            data["pending"].remove(name_zh)
        added += 1
    return added, skipped, 0


# ── Query helpers ─────────────────────────────────────────────

def game_display_name(info, lang):
    """Pick the best name to display for the given language."""
    name_zh = info.get("name_zh", "")
    name_en = info.get("name_en", "")
    name_ja = info.get("name_ja", "")
    if lang == "en":
        return name_en or name_zh or name_ja
    if lang == "ja":
        return name_ja or name_zh or name_en
    return name_zh or name_en or name_ja


def game_all_names(info):
    """Return a joined string of all non-empty names (excluding '/')."""
    return " / ".join(
        n for n in (info.get("name_zh", ""), info.get("name_en", ""), info.get("name_ja", ""))
        if n and n != "/"
    )


def match_keyword(info, key, keyword):
    """Check if keyword matches any of the three names or the dict key."""
    kw = keyword.lower()
    for val in (key, info.get("name_zh", ""), info.get("name_en", ""), info.get("name_ja", "")):
        if kw in val.lower():
            return True
    return False


def search_games(data, keyword):
    """Return dict of matching {key: info} entries."""
    return {
        key: info
        for key, info in data.get("available", {}).items()
        if match_keyword(info, key, keyword)
    }
