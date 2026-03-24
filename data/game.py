"""Game business logic: build, search, display."""


def build_game_record(name_zh, name_en, name_ja, system, launch):
    """Create a standardized game record dict."""
    return {
        "name_zh": name_zh,
        "name_en": name_en if name_en != "/" else "",
        "name_ja": name_ja if name_ja != "/" else "",
        "system": system,
        "launch": launch,
    }


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
