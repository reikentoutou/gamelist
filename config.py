"""Global configuration: paths, theme colors, font family."""

import os
import sys

# ── Data file path ────────────────────────────────────────────
BASE_DIR = (
    os.path.dirname(sys.executable)
    if getattr(sys, "frozen", False)
    else os.path.dirname(os.path.abspath(__file__))
)
DATA_FILE = os.path.join(BASE_DIR, "game_data.json")
DEFAULT_DATA = {"available": {}, "pending": []}

# ── Font ──────────────────────────────────────────────────────
if sys.platform == "win32":
    FONT_FAMILY = "Microsoft YaHei UI"
elif sys.platform == "darwin":
    FONT_FAMILY = "PingFang SC"
else:
    FONT_FAMILY = "sans-serif"

# ── Theme colors (light, dark) ────────────────────────────────
ACCENT = ("#005FB8", "#60CDFF")
ACCENT_HOVER = ("#0053A0", "#3CC0FF")
DANGER = ("#D13438", "#F1707B")
DANGER_HOVER = ("#B12E31", "#E54856")
SUCCESS_FG = ("#107C10", "#6CCB5F")
MISS_FG = ("#D13438", "#F1707B")
IMPORT_BTN = "#6C63FF"
IMPORT_BTN_HOVER = "#5A52D5"
