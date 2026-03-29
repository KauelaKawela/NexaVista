import traceback,os,requests,json,sys
import clr
from datetime import datetime

def output_folder():
    pass

def error_log_write(e):
    log_dir = "datas/log"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    anlik = datetime.now()
    filename = f"{log_dir}/error_log.txt"
    with open(filename, "a", encoding="utf-8") as er_file:
        if isinstance(e, Exception):
            tb = traceback.extract_tb(e.__traceback__)
            if tb:
                dosya, satir, fonksiyon, kod = tb[-1]
            else:
                dosya, satir, fonksiyon, kod = ("?", "?", "?", "?")
            er_file.write(
                f"[{anlik.strftime('%d-%m-%Y %H:%M:%S')}] "
                f"HATA: {repr(e)} | Tur: {type(e).__name__}\n"
                f"Dosya: {dosya}, Satir: {satir}, Fonksiyon: {fonksiyon}, Kod: {kod}\n"
                f"{traceback.format_exc()}\n"
            )
        else:
            er_file.write(
                f"[{anlik.strftime('%d-%m-%Y %H:%M:%S')}] HATA: {e}\n"
            )

def int_kontrol():
      try:
           requests.get("https://www.google.com",timeout=3)
      except requests.ConnectionError as e:
           print(f"{clr.am6}║\n║\n╚════════════╝ {clr.k}Internet baglantisi yok! Lutfen baglantinizi kontrol edin.{clr.r}")
           error_log_write(e)
           sys.exit()

def load_hata_code():
      try:
           with open("datas/data/hata_codes.json","r",encoding="utf-8") as hc:
                return json.load(hc)
      except FileNotFoundError as e:
           print(f"{clr.am6}║\n║\n╚════════════╝{clr.r} 'hata_codes.json' {clr.k}hata kodu dosyasi bulunamadi!{clr.r}")
           error_log_write(e)
           sys.exit()

def load_categori(file_categori):
       try:
           with open(file_categori,"r",encoding="utf-8") as fc:
                categories = [line.strip() for line in fc if line.strip()]
           return categories
       except FileNotFoundError as e:
            print(f"{clr.am6}║\n║\n╚════════════╝{clr.r} '{file_categori}'{clr.k} kategori dosyasi bulunamadi!{clr.r}")
            error_log_write(e)
            sys.exit()

def load_keywords(keys):
       try:
           with open(keys,"r",encoding="utf-8") as ky:
               return json.load(ky)
       except FileNotFoundError as e:
           print(f"{clr.am6}║\n║\n╚════════════╝{clr.r} '{keys}' {clr.k}dosyasi bulunamadi!{clr.r}")
           error_log_write(e)
           sys.exit()