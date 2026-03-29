import requests
import clr,os,sys
from datas.func import helper_func,extract

def check_proxy():
      online_proxies = []
      print(rf"""{clr.am9}╠═════════════════════════════════════╗
{clr.am5}║      Proxyleri Kontrol Et           ║
{clr.am9}╠═════════════════════════════════════╣""")
      link_file = input(f"{clr.am7}╠═══════ > Link dosya yolu: {clr.r}")
      if not os.path.exists(link_file):
          print(f"{clr.am6}║\n{clr.am4}║\n{clr.am3}╚════════════╝ '{link_file}' {clr.k}link dosyasi bulunamadi!{clr.r}")
          sys.exit()
      helper_func.int_kontrol()
      proxys = extract.extract_links(link_file)
      for index, line in enumerate(proxys, start=0):
          try:
              control = requests.get(
                   "http://ipinfo.io/json",
                   proxies={
                        "http" : line,
                        "https" : line,
           },
           timeout=10
     )

          except:
              continue

          if control.status_code == 200:
                online_proxies.append(line)
                print(f"{clr.y}Proxy online: {line.strip()}{clr.r}")
      print(f"\n{clr.y}Toplam {len(online_proxies)} aktif proxy bulundu.{clr.r}")
