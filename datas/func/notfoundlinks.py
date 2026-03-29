import clr,sys,os,json
from datas.func import usec,formated,helper_func,extract,urlstus

def gecersiz_links():
      print(rf"""{clr.am9}╠═════════════════════════════════════╗
{clr.am5}║      Gecersiz Linkleri Listele      ║
{clr.am9}╠═════════════════════════════════════╣""")
      link_file = input(f"{clr.am7}╠═══════ > Link dosya yolu: {clr.r}")
      if not os.path.exists(link_file):
          print(f"{clr.am6}║\n{clr.am4}║\n{clr.am3}╚════════════╝ '{link_file}' {clr.k}link dosyasi bulunamadi!{clr.r}")
          sys.exit()
      uzanti = usec.uzanti_sec()
      helper_func.int_kontrol()
      links = extract.extract_links(link_file)
      gecersiz_path = f"output/gecersiz_links.{uzanti}"
      with open(gecersiz_path, "a", encoding="utf-8") as outfile:
             for link in links:
                  durum = urlstus.url_status_cek(link)
                  if durum:
                      formatted = formated.formatla(link,uzanti,durum)
                      print(f"{clr.k}[{clr.r}{link}{clr.k}]{clr.r} >>> {durum}\n----")
                      if uzanti == "json":
                          json.dump(formatted,outfile,ensure_ascii=False)
                          outfile.write("\n")
                      else:
                          outfile.write(f"{formatted}\n")
      print(f"\n{clr.y}Gecersiz linkler '{gecersiz_path}' dosyasina kaydedildi{clr.r}")