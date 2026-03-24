"""Data persistence: load, save, migrate."""

import json
import os

from config import DATA_FILE, DEFAULT_DATA


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
