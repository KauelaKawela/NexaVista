import os, sys
from core import clr
from modules.scanner import usec,extract,urlstus,csf,wltf
from core import helper_func

def kategorize_et():
      print(rf"""{clr.am9}╠═════════════════════════════════════╗
{clr.am5}║       Linkleri Kategorize Et        ║
{clr.am9}╠═════════════════════════════════════╣""")
      link_file = input(f"{clr.am7}╠═══════ > Link dosya yolu: {clr.r}")
      if not os.path.exists(link_file):
          print(f"{clr.am6}║\n{clr.am4}║\n{clr.am3}╚════════════╝ '{link_file}' {clr.k}link dosyasi bulunamadi{clr.r}")
          helper_func.error_log_write("link dosyasi bulunamadi")
          sys.exit()
      uzanti = usec.uzanti_sec()
      helper_func.int_kontrol()
      from core.categories import CATEGORIES
      keywords = CATEGORIES
      links = extract.extract_links(link_file)
      for link in links:
            durum = urlstus.url_status_cek(link)
            kategori = csf.classify(link, keywords)
            wltf.wltf(link, kategori,uzanti,durum)
            if durum:
                print(f"{clr.k}[{clr.r}{kategori}{clr.k}]{clr.r} >>> {link} >>> {durum}\n----")
            else:
                print(f"{clr.k}[{clr.r}{kategori}{clr.k}]{clr.r} >>> {link}\n----")
      input(f"{clr.am6}║\n║\n╚════════════╝Menuye donmek icin herhangi bir tusa basin")