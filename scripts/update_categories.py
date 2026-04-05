import re
with open("core/categories.py", "r", encoding="utf-8") as f:
    text = f.read()

keywords_additions = {
    "technology": '"cloud computing": 3, "cybersecurity": 4, "frontend": 3, "backend": 3, "fullstack": 3, "react": 3, "angular": 3, "vue": 3, "database": 2, "sql": 3, "nosql": 3, "agile": 2, "scrum": 2, "server": 2, "networking": 2, "automation": 3, "scripting": 3, "bash": 3, "powershell": 2, "mac": 2, "windows": 2, "git": 3, "bitbucket": 3, "gitlab": 3, "docker-compose": 3, "aws": 4, "azure": 4, "gcp": 4, "serverless": 3, "microservices": 3,',
    "news": '"daily": 3, "journal": 3, "broadcast": 3, "briefing": 3, "coverage": 3, "interview": 2, "exclusive": 3, "investigation": 3, "columnist": 3, "publish": 2, "wire": 2, "gazete": 4, "sondakika": 4, "manşet": 3, "güncel": 3, "medya": 3, "basın": 3, "haberajansı": 4, "makale": 2, "köşeyazısı": 3, "analiz": 2,',
    "shopping": '"deal": 4, "promo": 4, "coupon": 4, "retail": 3, "wholesale": 3, "vendor": 2, "merchant": 2, "freight": 2, "refund": 3, "warranty": 2, "bestseller": 3, "wishlist": 3, "boutique": 3, "apparel": 3, "electronics": 3, "grocery": 3, "kampanya": 4, "fırsat": 4, "ucuz": 3, "kargo": 3, "bedava": 3, "iade": 2, "taksit": 3, "mağaza": 3, "market": 3, "katalog": 2,',
    "education": '"academy": 4, "college": 4, "campus": 3, "scholarship": 4, "syllabus": 3, "exam": 3, "quiz": 3, "assignment": 3, "diploma": 4, "alumni": 3, "faculty": 3, "professor": 3, "tutor": 3, "classroom": 3, "elearning": 4, "okul": 4, "üniversite": 4, "lise": 3, "öğrenci": 3, "öğretmen": 3, "sınav": 3, "burs": 4, "akademi": 4, "tez": 3, "kampüs": 3,',
    "social": '"connect": 3, "timeline": 3, "status": 2, "friendrequest": 3, "follower": 3, "influencer": 3, "viral": 3, "trending": 3, "hashtag": 3, "comment": 2, "reply": 2, "retweet": 4, "upvote": 3, "downvote": 3, "group": 2, "paylaş": 3, "beğen": 3, "takip": 3, "yorum": 2, "fenomen": 3, "trend": 3, "sohbet": 3, "mesaj": 2,',
    "media": '"cinema": 3, "theater": 2, "director": 3, "actor": 2, "actress": 2, "album": 3, "song": 3, "artist": 3, "concert": 3, "ticket": 2, "trailer": 3, "review": 2, "rating": 2, "gallery": 2, "photo": 2, "image": 2, "sinema": 3, "tiyatro": 2, "şarkı": 3, "müzik": 4, "konser": 3, "dizi": 3, "fragman": 3, "bölüm": 3, "sezon": 3, "albüm": 3,',
    "finance": '"money": 4, "currency": 3, "exchange": 3, "broker": 4, "dividend": 4, "equity": 4, "mortgage": 4, "loan": 4, "credit": 3, "debt": 3, "tax": 3, "audit": 3, "insurance": 4, "wealth": 3, "asset": 3, "para": 4, "kredi": 4, "döviz": 4, "faiz": 4, "hisse": 4, "sigorta": 4, "vergi": 3, "fon": 4, "kâr": 3, "zarar": 3,',
    "health": '"clinic": 4, "pharmacy": 4, "disease": 3, "virus": 3, "vaccine": 4, "therapy": 3, "surgery": 4, "patient": 3, "care": 2, "mental": 3, "dental": 4, "diet": 3, "workout": 3, "gym": 3, "yoga": 3, "hastane": 4, "klinik": 4, "eczane": 4, "hastalık": 3, "tedavi": 4, "ameliyat": 4, "hasta": 3, "diyet": 3, "spor": 2, "psikoloji": 3,',
    "gaming": '"gamer": 4, "joystick": 3, "controller": 3, "pcgaming": 4, "rpg": 4, "mmo": 4, "fps": 4, "moba": 4, "streamer": 3, "walkthrough": 3, "cheat": 2, "mod": 2, "patch": 2, "update": 2, "server": 2, "oyuncu": 4, "konsol": 4, "hile": 2, "yama": 2, "sunucu": 2, "espor": 4, "turnuva": 3, "yayın": 3,',
    "government": '"public": 3, "citizen": 3, "vote": 4, "election": 4, "taxpayer": 4, "mayor": 4, "governor": 4, "president": 5, "prime minister": 5, "congress": 4, "legislation": 4, "statute": 3, "court": 4, "justice": 4, "police": 4, "kamu": 4, "vatandaş": 3, "seçim": 4, "oy": 3, "belediye": 4, "vali": 4, "başkan": 4, "yasa": 4, "kanun": 4, "mahkeme": 4, "polis": 4,',
}

for cat, extra in keywords_additions.items():
    pattern = rf'("{cat}":\s*{{[^}}]*"keywords":\s*{{)'
    text = re.sub(pattern, rf'\1\n            {extra}', text)

with open("core/categories.py", "w", encoding="utf-8") as f:
    f.write(text)

print("Updated categories.py")
