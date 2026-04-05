def classify(link, categories_dict):
    for kategori, data in categories_dict.items():
        if "keywords" in data:
            for kelime in data["keywords"]:
                if kelime.lower() in link.lower():
                    return kategori
    return "Bilinmiyor"
