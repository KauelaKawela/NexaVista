import re
from urllib.parse import urlparse

import clr
from datas.data.categories import CATEGORIES


_PRECOMPILED_PATTERNS = {
    cat: [re.compile(p) for p in data.get("domain_patterns", [])]
    for cat, data in CATEGORIES.items()
}

def categorize(text: str, url: str) -> tuple[str, float]:
    domain = urlparse(url).netloc.lower()
    scores: dict[str, float] = {}

    for cat, data in CATEGORIES.items():
        hit = 0
        total_weight = 0
        for kw, weight in data["keywords"].items():
            total_weight += weight
            if kw in text or kw in domain:
                hit += weight

        for pattern in _PRECOMPILED_PATTERNS.get(cat, []):
            if pattern.search(domain):
                hit += data.get("domain_bonus", 5)
        scores[cat] = hit / max(total_weight, 1)

    best = max(scores, key=scores.get)
    confidence = min(scores[best] * 100, 100.0)

    if confidence < 5:
        return "other", round(confidence, 1)
    return best, round(confidence, 1)


def score_color(score: int) -> str:
    if score >= 75:
        return clr.y
    if score >= 50:
        return clr.s
    if score >= 25:
        return clr.am6
    return clr.k
