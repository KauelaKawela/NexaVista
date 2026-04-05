import sys
from core import clr

def formatla(link, uzanti, durum=None):
    if uzanti.lower().strip() == "json":
        return {"link": link, "durum": durum}
    elif uzanti.lower().strip() == "csv":
        return f"{link},{durum if durum else ''}"
    elif uzanti.lower().strip() == "html":
        return f"<li><a href='{link}'>{link}</a> ({durum if durum else ''})</li>"
    elif uzanti.lower().strip() == "xml":
        return f"<link><url>{link}</url><durum>{durum}</durum></link>"
    elif uzanti.lower().strip() == "txt":
        return f"{link} ({durum})" if durum else f"{link}"
    else:
        print(f"{clr.am9}║\n║\n{clr.am5}╚═══════════╝ {clr.k}Hatali secim turu! Gecerli uzanti girin{clr.r}")
        sys.exit()