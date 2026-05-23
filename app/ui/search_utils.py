from __future__ import annotations

from typing import Any

_TR_TABLE = {
    ord("ç"): "c", ord("ğ"): "g", ord("ı"): "i", ord("i"): "i",
    ord("ö"): "o", ord("ş"): "s", ord("ü"): "u",
    ord("à"): "a", ord("á"): "a", ord("â"): "a", ord("ã"): "a",
    ord("ä"): "a", ord("å"): "a", ord("æ"): "a", ord("è"): "e",
    ord("é"): "e", ord("ê"): "e", ord("ë"): "e", ord("ì"): "i",
    ord("í"): "i", ord("î"): "i", ord("ï"): "i", ord("ò"): "o",
    ord("ó"): "o", ord("ô"): "o", ord("õ"): "o", ord("ö"): "o",
    ord("ø"): "o", ord("ù"): "u", ord("ú"): "u", ord("û"): "u",
    ord("ü"): "u", ord("ą"): "a", ord("ć"): "c", ord("ę"): "e",
    ord("ł"): "l", ord("ń"): "n", ord("ó"): "o", ord("ś"): "s",
    ord("ź"): "z", ord("ż"): "z",
}


def _normalize(s: str) -> str:
    s = s.lower().strip()
    s = s.translate(_TR_TABLE)
    return s


def _score_fuzzy(haystack: str, needle: str) -> int:
    """Return match score using substring & char-presence heuristics."""
    if needle in haystack:
        return 100 + len(needle) * 3

    # Partial: each consecutive char match gives score
    score = 0
    prev = -2
    consecutive = 0
    for ch in needle:
        idx = haystack.find(ch, max(0, prev))
        if idx >= 0:
            if idx == prev + 1:
                consecutive += 1
                score += 10 + consecutive * 5
            else:
                consecutive = 1
                score += 5
            prev = idx
        else:
            consecutive = 0
    return score


def entry_matches_query(entry: dict[str, Any], q: str) -> bool:
    if not q:
        return True
    qn = _normalize(q)
    tn = _normalize(str(entry.get("title", "")))
    an = _normalize(str(entry.get("author", "")))
    cn = _normalize(entry_city(entry))
    return qn in tn or qn in an or qn in cn or _score_fuzzy(tn, qn) > 20


def entry_city(entry: dict[str, Any]) -> str:
    city = entry.get("city")
    if city is not None and str(city).strip():
        return str(city).strip()
    loc = str(entry.get("location_name", "")).strip()
    if "," in loc:
        return loc.split(",")[-1].strip()
    return loc


def filter_entries_for_suggest(
    entries: list[dict[str, Any]],
    query: str,
    limit: int = 14,
) -> list[dict[str, Any]]:
    q = _normalize(query)
    if not q:
        return []

    ranked: list[tuple[int, dict[str, Any]]] = []
    for e in entries:
        title = _normalize(str(e.get("title", "")))
        author = _normalize(str(e.get("author", "")))
        city = _normalize(entry_city(e))

        best = 0
        for field in (title, author, city):
            s = _score_fuzzy(field, q)
            if s > best:
                best = s

        if best > 8:
            ranked.append((best, e))

    ranked.sort(key=lambda pair: pair[0], reverse=True)
    return [e for _, e in ranked[:limit]]
