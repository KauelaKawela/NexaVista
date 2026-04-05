import re, json
from core import clr
from core import helper_func,formated
from datetime import datetime

def wltf(link, kategori, uzanti, durum=None):
    timestep = datetime.now().strftime("%Y%m%d_%H%M%S")
    try:
        if not link.startswith("http://") and not link.startswith("https://"):
            link = "https://" + link
        kategori = re.sub(r'[^\w\-_.]', '_', kategori)
        filename = f"outputs/{kategori}_{timestep}.{uzanti.lstrip('.')}"
        formatted = formated.formatla(link, uzanti, durum)
        with open(filename, "a", encoding="utf-8") as wf:
            if uzanti == "json":
                json.dump(formatted, wf, ensure_ascii=False)
                wf.write("\n")
            else:
                wf.write(f"{formatted}\n")
    except Exception as e:
        print(f"'{kategori}' {clr.k}kategorisine ait link dosyaya yazilamadi: {clr.r}{e}")
        helper_func.error_log_write(e)