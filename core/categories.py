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
            "cloud computing": 3, "cybersecurity": 4, "frontend": 3, "backend": 3, "fullstack": 3, "react": 3, "angular": 3, "vue": 3, "database": 2, "sql": 3, "nosql": 3, "agile": 2, "scrum": 2, "server": 2, "networking": 2, "automation": 3, "scripting": 3, "bash": 3, "powershell": 2, "mac": 2, "windows": 2, "git": 3, "bitbucket": 3, "gitlab": 3, "docker-compose": 3, "aws": 4, "azure": 4, "gcp": 4, "serverless": 3, "microservices": 3,
            "software": 3, "programming": 3, "developer": 3, "code": 3,
            "github": 4, "python": 3, "javascript": 3, "linux": 3,
            "api": 2, "framework": 2, "library": 2, "open source": 3,
            "tech": 2, "hardware": 2, "computer": 2, "ai": 2,
            "machine learning": 3, "data science": 3, "cloud": 2,
            "devops": 3, "docker": 3, "kubernetes": 3, "stack overflow": 4,
            "cyber": 3, "security": 3, "encryption": 3, "firewall": 3, "malware": 2, "penetration": 4, "vuln": 3,
            "yazılım": 3, "programlama": 3, "geliştirici": 3, "kod": 3, "veritabanı": 3, "sunucu": 2, "ağ": 2, "otomasyon": 3,
            "yapay zeka": 3, "veri bilimi": 3, "bulut": 2, "siber": 3, "güvenlik": 3, "şifreleme": 3, "saldırı": 2,
            "backend": 3, "frontend": 3, "fullstack": 4, "devops": 4, "sysadmin": 3, "container": 3, "microservices": 3,
            "react": 2, "angular": 2, "vue": 2, "django": 3, "flask": 3, "node": 3, "express": 3, "spring": 3,
            "mysql": 2, "postgres": 2, "mongodb": 2, "redis": 2, "elasticsearch": 3,
            "linux": 3, "unix": 3, "ubuntu": 2, "debian": 2, "centos": 2, "kali": 4, "parrot": 4,
            "hacking": 5, "exploit": 5, "payload": 4, "bruteforce": 4, "phishing": 4, "sqli": 5, "xss": 5,
            "metasploit": 5, "nmap": 4, "wireshark": 4, "burp": 4, "fuff": 3, "dirb": 3,
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
            "daily": 3, "journal": 3, "broadcast": 3, "briefing": 3, "coverage": 3, "interview": 2, "exclusive": 3, "investigation": 3, "columnist": 3, "publish": 2, "wire": 2, "gazete": 4, "sondakika": 4, "manşet": 3, "güncel": 3, "medya": 3, "basın": 3, "haberajansı": 4, "makale": 2, "köşeyazısı": 3, "analiz": 2,
            "news": 4, "breaking": 3, "headline": 3, "article": 2,
            "journalist": 3, "reporter": 3, "press": 2, "media": 2,
            "latest": 2, "update": 2, "world": 2, "politics": 3,
            "opinion": 2, "editorial": 3, "magazine": 2,
            "politics": 3, "economy": 3, "sports": 2, "entertainment": 2, "weather": 2, "local": 2, "international": 3,
            "siyaset": 3, "ekonomi": 3, "spor": 2, "magazin": 2, "hava durumu": 2, "yerel": 2, "uluslararası": 3, "manset": 3, "gazeteler": 3,
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
            "deal": 4, "promo": 4, "coupon": 4, "retail": 3, "wholesale": 3, "vendor": 2, "merchant": 2, "freight": 2, "refund": 3, "warranty": 2, "bestseller": 3, "wishlist": 3, "boutique": 3, "apparel": 3, "electronics": 3, "grocery": 3, "kampanya": 4, "fırsat": 4, "ucuz": 3, "kargo": 3, "bedava": 3, "iade": 2, "taksit": 3, "mağaza": 3, "market": 3, "katalog": 2,
            "buy": 4, "cart": 4, "checkout": 4, "shop": 4, "store": 3,
            "product": 3, "price": 3, "sale": 3, "discount": 3, "offer": 2,
            "order": 3, "shipping": 3, "delivery": 2, "payment": 3,
            "amazon": 5, "ebay": 5, "ecommerce": 4, "marketplace": 3,
            "satın al": 4, "sepet": 4, "indirim": 3, "fiyat": 3,
            "voucher": 4, "gift card": 3, "inventory": 2, "clearance": 3, "outlet": 3, "brand": 2, "loyalty": 2,
            "hediye kartı": 3, "stok": 2, "tasfiye": 3, "marka": 2, "sadakat": 2, "alisveris": 4, "ürünler": 3, "sipariş": 3, "ödeme": 3,
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
            "academy": 4, "college": 4, "campus": 3, "scholarship": 4, "syllabus": 3, "exam": 3, "quiz": 3, "assignment": 3, "diploma": 4, "alumni": 3, "faculty": 3, "professor": 3, "tutor": 3, "classroom": 3, "elearning": 4, "okul": 4, "üniversite": 4, "lise": 3, "öğrenci": 3, "öğretmen": 3, "sınav": 3, "burs": 4, "akademi": 4, "tez": 3, "kampüs": 3,
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
            "connect": 3, "timeline": 3, "status": 2, "friendrequest": 3, "follower": 3, "influencer": 3, "viral": 3, "trending": 3, "hashtag": 3, "comment": 2, "reply": 2, "retweet": 4, "upvote": 3, "downvote": 3, "group": 2, "paylaş": 3, "beğen": 3, "takip": 3, "yorum": 2, "fenomen": 3, "trend": 3, "sohbet": 3, "mesaj": 2,
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
            "cinema": 3, "theater": 2, "director": 3, "actor": 2, "actress": 2, "album": 3, "song": 3, "artist": 3, "concert": 3, "ticket": 2, "trailer": 3, "review": 2, "rating": 2, "gallery": 2, "photo": 2, "image": 2, "sinema": 3, "tiyatro": 2, "şarkı": 3, "müzik": 4, "konser": 3, "dizi": 3, "fragman": 3, "bölüm": 3, "sezon": 3, "albüm": 3,
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
            "money": 4, "currency": 3, "exchange": 3, "broker": 4, "dividend": 4, "equity": 4, "mortgage": 4, "loan": 4, "credit": 3, "debt": 3, "tax": 3, "audit": 3, "insurance": 4, "wealth": 3, "asset": 3, "para": 4, "kredi": 4, "döviz": 4, "faiz": 4, "hisse": 4, "sigorta": 4, "vergi": 3, "fon": 4, "kâr": 3, "zarar": 3,
            "finance": 4, "bank": 4, "investment": 4, "stock": 4,
            "crypto": 4, "bitcoin": 4, "trading": 4, "market": 3,
            "portfolio": 3, "forex": 4, "economy": 3, "wallet": 3,
            "blockchain": 4, "defi": 4, "nft": 3,
            "borsa": 4, "yatırım": 4, "kripto": 4,
            "banking": 4, "capital": 3, "venture": 3, "pension": 3, "retirement": 3, "budget": 3, "invoice": 3, "accounting": 4, "ledger": 3,
            "bankacılık": 4, "sermaye": 3, "emeklilik": 3, "bütçe": 3, "fatura": 3, "muhasebe": 4, "defter": 3, "mali": 3, "finansal": 3,
            "nasdaq": 4, "sp500": 4, "dow jones": 4, "bist100": 4, "altın": 3, "gümüş": 3, "petrol": 2, "mtia": 3,
            "gold": 3, "silver": 3, "oil": 2, "commodity": 3, "arbitrage": 4, "hedging": 4, "liquidity": 3,
            "tradingview": 3, "metatrader": 4, "binance": 4, "coinmarketcap": 3,
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
            "clinic": 4, "pharmacy": 4, "disease": 3, "virus": 3, "vaccine": 4, "therapy": 3, "surgery": 4, "patient": 3, "care": 2, "mental": 3, "dental": 4, "diet": 3, "workout": 3, "gym": 3, "yoga": 3, "hastane": 4, "klinik": 4, "eczane": 4, "hastalık": 3, "tedavi": 4, "ameliyat": 4, "hasta": 3, "diyet": 3, "spor": 2, "psikoloji": 3,
            "health": 4, "medical": 4, "doctor": 4, "hospital": 4,
            "medicine": 3, "drug": 3, "symptom": 3, "treatment": 3,
            "nutrition": 3, "fitness": 3, "wellness": 3,
            "sağlık": 4, "doktor": 4, "ilaç": 3,
            "dentist": 4, "mental health": 3, "psychology": 3, "symptom": 3, "diagnosis": 3, "prescription": 3, "rehab": 3,
            "diş hekimi": 4, "ruh sağlığı": 3, "teşhis": 3, "reçete": 3, "tedavi": 4, "hastane": 4, "klinik": 4, "muayene": 3,
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
            "gamer": 4, "joystick": 3, "controller": 3, "pcgaming": 4, "rpg": 4, "mmo": 4, "fps": 4, "moba": 4, "streamer": 3, "walkthrough": 3, "cheat": 2, "mod": 2, "patch": 2, "update": 2, "server": 2, "oyuncu": 4, "konsol": 4, "hile": 2, "yama": 2, "sunucu": 2, "espor": 4, "turnuva": 3, "yayın": 3,
            "game": 4, "gaming": 4, "play": 3, "player": 3,
            "esport": 4, "console": 3, "xbox": 4, "playstation": 4,
            "steam": 4, "minecraft": 4, "fps": 3, "rpg": 3,
            "multiplayer": 3, "level": 2, "quest": 2,
            "oyun": 4, "oyna": 3,
            "betting": 3, "casino": 3, "lottery": 3, "gambling": 3, "tournament": 3, "ranked": 3, "skins": 2,
            "bahis": 3, "kumar": 3, "piyango": 3, "şans oyunları": 3, "turnuva": 3, "sıralama": 3, "rekabet": 2,
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
            "public": 3, "citizen": 3, "vote": 4, "election": 4, "taxpayer": 4, "mayor": 4, "governor": 4, "president": 5, "prime minister": 5, "congress": 4, "legislation": 4, "statute": 3, "court": 4, "justice": 4, "police": 4, "kamu": 4, "vatandaş": 3, "seçim": 4, "oy": 3, "belediye": 4, "vali": 4, "başkan": 4, "yasa": 4, "kanun": 4, "mahkeme": 4, "polis": 4,
            "government": 5, "official": 4, "policy": 4, "law": 4,
            "regulation": 4, "ministry": 4, "parliament": 4, "senate": 4,
            "federal": 4, "state": 3, "municipality": 3,
            "devlet": 5, "bakanlık": 5, "resmi": 4, "mevzuat": 4,
            "consulate": 4, "embassy": 4, "citizen": 3, "passport": 4, "visa": 4, "notary": 4, "customs": 3,
            "konsolosluk": 4, "elçilik": 4, "vatandaşlık": 3, "pasaport": 4, "vize": 4, "noter": 4, "gümrük": 3, "vergi dairesi": 3, "e-devlet": 5,
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
