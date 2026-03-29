"""
categories.py  —  Kategori tanımları ve puan ağırlıkları
Her kategori:
  - keywords  : {anahtar_kelime: ağırlık}  — içerik/title/meta eşleşmesi
  - domain_patterns : regex listesi domain üzerinde ek eşleşme
  - domain_bonus    : domain pattern eşleşince eklenen ham puan
  - icon      : terminal ikonu
"""

CATEGORIES: dict = {
    # ── Teknoloji / Geliştirici ────────────────────────────────────
    "technology": {
        "icon": "💻",
        "keywords": {
            "software": 3, "programming": 3, "developer": 3, "code": 3,
            "github": 4, "python": 3, "javascript": 3, "linux": 3,
            "api": 2, "framework": 2, "library": 2, "open source": 3,
            "tech": 2, "hardware": 2, "computer": 2, "ai": 2,
            "machine learning": 3, "data science": 3, "cloud": 2,
            "devops": 3, "docker": 3, "kubernetes": 3, "stack overflow": 4,
        },
        "domain_patterns": [
            r"github\.com", r"stackoverflow\.com", r"dev\.to",
            r"hackernews", r"techcrunch\.com", r"wired\.com",
            r"python\.org", r"nodejs\.org", r"rust-lang\.org",
        ],
        "domain_bonus": 8,
    },

    # ── Haber / Medya ──────────────────────────────────────────────
    "news": {
        "icon": "📰",
        "keywords": {
            "news": 4, "breaking": 3, "headline": 3, "article": 2,
            "journalist": 3, "reporter": 3, "press": 2, "media": 2,
            "latest": 2, "update": 2, "world": 2, "politics": 3,
            "opinion": 2, "editorial": 3, "magazine": 2,
        },
        "domain_patterns": [
            r"bbc\.", r"cnn\.", r"reuters\.", r"nytimes\.", r"theguardian\.",
            r"bloomberg\.", r"forbes\.", r"huffpost\.", r"apnews\.",
            r"haberler\.", r"sabah\.", r"hurriyet\.", r"milliyet\.",
        ],
        "domain_bonus": 10,
    },

    # ── Alışveriş / E-ticaret ──────────────────────────────────────
    "shopping": {
        "icon": "🛒",
        "keywords": {
            "buy": 4, "cart": 4, "checkout": 4, "shop": 4, "store": 3,
            "product": 3, "price": 3, "sale": 3, "discount": 3, "offer": 2,
            "order": 3, "shipping": 3, "delivery": 2, "payment": 3,
            "amazon": 5, "ebay": 5, "ecommerce": 4, "marketplace": 3,
            "satın al": 4, "sepet": 4, "indirim": 3, "fiyat": 3,
        },
        "domain_patterns": [
            r"amazon\.", r"ebay\.", r"etsy\.", r"aliexpress\.",
            r"trendyol\.", r"hepsiburada\.", r"n11\.", r"gittigidiyor\.",
        ],
        "domain_bonus": 10,
    },

    # ── Eğitim ─────────────────────────────────────────────────────
    "education": {
        "icon": "🎓",
        "keywords": {
            "learn": 4, "course": 4, "tutorial": 4, "education": 4,
            "university": 4, "school": 3, "lecture": 3, "study": 3,
            "lesson": 3, "training": 3, "certificate": 3, "degree": 3,
            "student": 3, "teacher": 3, "academic": 3, "research": 3,
            "eğitim": 4, "ders": 3, "öğren": 3, "kurs": 4,
        },
        "domain_patterns": [
            r"\.edu$", r"coursera\.", r"udemy\.", r"edx\.",
            r"khanacademy\.", r"wikipedia\.", r"udacity\.",
        ],
        "domain_bonus": 9,
    },

    # ── Sosyal Medya ───────────────────────────────────────────────
    "social": {
        "icon": "📱",
        "keywords": {
            "social": 4, "profile": 3, "follow": 3, "share": 3,
            "post": 2, "tweet": 4, "like": 2, "friend": 3, "community": 3,
            "forum": 3, "discussion": 3, "chat": 3, "message": 2,
            "network": 3, "feed": 3,
        },
        "domain_patterns": [
            r"twitter\.com", r"x\.com", r"facebook\.", r"instagram\.",
            r"linkedin\.", r"reddit\.", r"tiktok\.", r"discord\.",
            r"mastodon\.", r"bluesky\.",
        ],
        "domain_bonus": 10,
    },

    # ── Video / Medya ──────────────────────────────────────────────
    "media": {
        "icon": "🎬",
        "keywords": {
            "video": 4, "watch": 3, "stream": 3, "movie": 3, "film": 3,
            "series": 3, "episode": 3, "podcast": 3, "music": 3,
            "audio": 2, "playlist": 3, "channel": 3, "subscribe": 3,
            "youtube": 5, "netflix": 5, "spotify": 5,
        },
        "domain_patterns": [
            r"youtube\.", r"netflix\.", r"twitch\.", r"spotify\.",
            r"vimeo\.", r"dailymotion\.", r"soundcloud\.",
        ],
        "domain_bonus": 10,
    },

    # ── Finans / Kripto ────────────────────────────────────────────
    "finance": {
        "icon": "💰",
        "keywords": {
            "finance": 4, "bank": 4, "investment": 4, "stock": 4,
            "crypto": 4, "bitcoin": 4, "trading": 4, "market": 3,
            "portfolio": 3, "forex": 4, "economy": 3, "wallet": 3,
            "blockchain": 4, "defi": 4, "nft": 3,
            "borsa": 4, "yatırım": 4, "kripto": 4,
        },
        "domain_patterns": [
            r"coinbase\.", r"binance\.", r"kraken\.", r"bloomberg\.",
            r"investing\.com", r"tradingview\.", r"yahoo.*finance",
        ],
        "domain_bonus": 8,
    },

    # ── Sağlık ─────────────────────────────────────────────────────
    "health": {
        "icon": "🏥",
        "keywords": {
            "health": 4, "medical": 4, "doctor": 4, "hospital": 4,
            "medicine": 3, "drug": 3, "symptom": 3, "treatment": 3,
            "nutrition": 3, "fitness": 3, "wellness": 3,
            "sağlık": 4, "doktor": 4, "ilaç": 3,
        },
        "domain_patterns": [
            r"webmd\.", r"mayoclinic\.", r"healthline\.",
            r"who\.int", r"nih\.gov",
        ],
        "domain_bonus": 8,
    },

    # ── Oyun ───────────────────────────────────────────────────────
    "gaming": {
        "icon": "🎮",
        "keywords": {
            "game": 4, "gaming": 4, "play": 3, "player": 3,
            "esport": 4, "console": 3, "xbox": 4, "playstation": 4,
            "steam": 4, "minecraft": 4, "fps": 3, "rpg": 3,
            "multiplayer": 3, "level": 2, "quest": 2,
            "oyun": 4, "oyna": 3,
        },
        "domain_patterns": [
            r"steam\.", r"epicgames\.", r"twitch\.",
            r"ign\.", r"gamespot\.", r"kotaku\.",
        ],
        "domain_bonus": 8,
    },

    # ── Hükümet / Resmi ────────────────────────────────────────────
    "government": {
        "icon": "🏛️",
        "keywords": {
            "government": 5, "official": 4, "policy": 4, "law": 4,
            "regulation": 4, "ministry": 4, "parliament": 4, "senate": 4,
            "federal": 4, "state": 3, "municipality": 3,
            "devlet": 5, "bakanlık": 5, "resmi": 4, "mevzuat": 4,
        },
        "domain_patterns": [
            r"\.gov$", r"\.gov\.", r"\.mil$",
            r"\.gov\.tr", r"tbmm\.gov\.tr",
        ],
        "domain_bonus": 12,
    },

    # ── Diğer ──────────────────────────────────────────────────────
    "other": {
        "icon": "🔗",
        "keywords": {},
        "domain_patterns": [],
        "domain_bonus": 0,
    },
}


# ──────────────────────────────────────────────────────────────────
# Puan sistemi ağırlıkları  (toplam maks ≈ 100)
# ──────────────────────────────────────────────────────────────────
SCORE_WEIGHTS: dict = {
    # Erişilebilirlik (25 puan)
    "status_200": 25,
    "status_redirect": 15,
    "status_other": 5,

    # Hız (20 puan)
    "speed_fast": 20,       # < 500 ms
    "speed_medium": 14,     # 500–1500 ms
    "speed_slow": 7,        # 1500–3000 ms
    "speed_veryslow": 2,    # > 3000 ms

    # SSL (15 puan)
    "ssl_valid": 15,

    # İçerik kalitesi (25 puan maks)
    "has_title": 7,
    "has_description": 7,
    "has_keywords": 4,
    "has_headings": 7,
    "content_max": 25,

    # Redirect cezası
    "redirect_penalty": 3,  # her redirect için -3 puan

    # Kategori güveni bonusu (15 puan maks)
    "confidence_max": 15,
}
