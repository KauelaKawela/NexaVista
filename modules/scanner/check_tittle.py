import requests, os, sys, json
from core import clr
from modules.scanner import usec, extract
from core import formated, helper_func
from bs4 import BeautifulSoup

def baslik_getir(url):
    try:
        response = requests.get(url, timeout=5)
        soup = BeautifulSoup(response.text, "html.parser")
        return soup.title.string.strip() if soup.title else "(baslik yok)"
    except Exception as e:
        return f"(hata: {e})"

def baslık_cek():
      print(rf"""{clr.am9}╠═════════════════════════════════════╗
{clr.am5}║       Linklerden Baslik Cek        ║
{clr.am9}╠═════════════════════════════════════╣""")
      link_file = input(f"{clr.am7}╠═══════ > Link dosya yolu: {clr.r}")
      if not os.path.exists(link_file):
          print(f"{clr.am6}║\n{clr.am4}║\n{clr.am3}╚════════════╝ '{link_file}' {clr.k}link dosyasi bulunamadi{clr.r}")
          sys.exit()
      uzanti = usec.uzanti_sec()
      helper_func.int_kontrol()
      title_yolu = f"outputs/titles.{uzanti}"
      links = extract.extract_links(link_file)
      with open(title_yolu,"a",encoding="utf-8") as cikti_file:
           for link in links:
                 baslik = baslik_getir(link)
                 formatted = formated.formatla(link,uzanti,baslik)
                 print(f"{clr.k}[{clr.r}{link}{clr.k}]{clr.r} >>> {baslik}\n----")
                 if uzanti == "json":
                     json.dump(formatted,cikti_file,ensure_ascii=False)
                     cikti_file.write("\n")
                 else:
                     cikti_file.write(f"{formatted}\n")