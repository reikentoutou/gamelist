"""File import: read, parse, and batch-import games."""

import csv
import io

from data.game import build_game_record


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
