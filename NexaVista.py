import os
import re
import sys

import clr
from datas.func.config import setup_logging, log, OUTPUT_DIR, PROXY_LIST
from datas.func.manager import NexaVista
from datas.func.stealth import (
    StealthConfig, STEALTH_OFF, STEALTH_MINIMAL,
    STEALTH_STANDARD, STEALTH_FULL,
)
from datas.func import reporter
from datas.func import helper_func, extract, urlstus, csf, formated, usec, wltf
from datas.func import check_tittle as ctl
from datas.func import notfoundlinks as nfl
from datas.func import proxy_check


def banner():
    print(f"\n" + clr.am1)
    print(r"  _   _             __      ___     _   " + clr.am1)
    print(r" | \ | |            \ \    / (_)   | |      " + clr.am1)
    print(r" |  \| | _____  ____ \ \  / / _ ___| |_ __ _    " + clr.am2)
    print(r" | . ` |/ _ \ \/ / _` \ \/ / | / __| __/ _` |  ")
    print(r" | |\  |  __/>  < (_| |\  /  | \__ \ || (_| |")
    print(r" |_| \_|\___/_/\_\__,_| \/   |_|___/\__\__,_|")
    print("")
    print(f"{clr.am5}        NexaVista - v3.0 ")
    print(f"            Created by: github.com/KauelaKawela{clr.r}")


# ══════════════════════════════════════════════════════════════════
# 1 — Standart Tarama
# ══════════════════════════════════════════════════════════════════
def standart_tarama():
    print(rf"""{clr.am9}╠═════════════════════════════════════╗
{clr.am5}║         Standart Tarama             ║
{clr.am9}╠═════════════════════════════════════╣""")

    stealth_config = _anonimlik_sor()

    workers_input = input(f"{clr.am7}╠═══════ > Thread sayisi [10]: {clr.r}").strip()
    workers = int(workers_input) if workers_input.isdigit() else 10
    workers = max(1, min(workers, 100))

    urls = _url_girisi()
    if not urls:
        input(f"{clr.am6}║\n╚══════ > Menuye donmek icin bir tusa basin.. {clr.r}")
        main()
        return

    from datetime import datetime
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_dir = setup_logging(ts)

    nv = NexaVista(max_workers=workers, stealth_config=stealth_config)
    results = nv.scan_urls(urls)

    scan_output_dir = os.path.join(OUTPUT_DIR, f"scan_{ts}")
    result_log_path = os.path.join(log_dir, "result.log")

    reporter.print_report(results, log_file_path=result_log_path)
    reporter.save_results(results, scan_output_dir)

    print(f"{clr.am7}╠═══════ > Disa aktarma formatlari (virgulle ayirin) [md,txt,html,xml,js]:{clr.r}")
    fmt_input = input(f"{clr.am7}╠═══════ > {clr.r}").strip()
    if fmt_input:
        formats = [f.strip() for f in fmt_input.split(",")]
        reporter.export_results(results, scan_output_dir, formats)

    log.info(f"Scan complete: stealth={stealth_config.level}, {len(results)} URLs, output_dir={scan_output_dir}")

    input(f"{clr.am6}║\n╚══════ > Menuye donmek icin bir tusa basin.. {clr.r}")
    main()


# ══════════════════════════════════════════════════════════════════
# 2 — Gecersiz Link Tespiti
# ══════════════════════════════════════════════════════════════════
def gecersiz_tarama():
    print(rf"""{clr.am9}╠═════════════════════════════════════╗
{clr.am5}║       Gecersiz Link Tespiti         ║
{clr.am9}╠═════════════════════════════════════╣""")

    stealth_config = _anonimlik_sor()

    workers_input = input(f"{clr.am7}╠═══════ > Thread sayisi [10]: {clr.r}").strip()
    workers = int(workers_input) if workers_input.isdigit() else 10
    workers = max(1, min(workers, 100))

    urls = _url_girisi()
    if not urls:
        input(f"{clr.am6}║\n╚══════ > Menuye donmek icin bir tusa basin.. {clr.r}")
        main()
        return

    from datetime import datetime
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_dir = setup_logging(ts)

    nv = NexaVista(max_workers=workers, stealth_config=stealth_config)
    results = nv.scan_urls(urls)

    scan_output_dir = os.path.join(OUTPUT_DIR, f"scan_{ts}")
    result_log_path = os.path.join(log_dir, "result.log")

    reporter.print_invalid_report(results, log_file_path=result_log_path)
    reporter.save_invalid_results(results, scan_output_dir)

    log.info(f"Invalid scan complete: stealth={stealth_config.level}, {len(results)} URLs, output_dir={scan_output_dir}")

    input(f"{clr.am6}║\n╚══════ > Menuye donmek icin bir tusa basin.. {clr.r}")
    main()


# ══════════════════════════════════════════════════════════════════
# 3 — Linkleri Kategorize Et (v3 basit mod)
# ══════════════════════════════════════════════════════════════════
# → datas/func/docat.kategorize_et()


# ══════════════════════════════════════════════════════════════════
# 4 — Linklerden Baslik Cek
# ══════════════════════════════════════════════════════════════════
# → datas/func/check_tittle.baslık_cek()


# ══════════════════════════════════════════════════════════════════
# 5 — Proxyleri Kontrol Et
# ══════════════════════════════════════════════════════════════════
# → datas/func/proxy_check.check_proxy()


# ══════════════════════════════════════════════════════════════════
# 6 — Kategori Sayilarini Goster
# ══════════════════════════════════════════════════════════════════
def kategori_elementleri():
    print(rf"""{clr.am9}╠═════════════════════════════════════╗
{clr.am5}║     Kategori Sayilarini Goster      ║
{clr.am9}╠═════════════════════════════════════╣""")
    klasor = "datas/output"
    kategoriler = {}
    uzantilar = (".txt", ".json", ".csv", ".xml", ".html")
    if not os.path.isdir(klasor):
        print(f"{clr.am9}║\n║\n{clr.am5}╠════════════╝ {clr.k}Kategori klasoru bulunamadi!{clr.r}")
        helper_func.error_log_write("Kategori klasoru bulunamadi!")
        input(f"{clr.am6}║\n╚══════ > Menuye donmek icin bir tusa basin.. {clr.r}")
        main()
        return
    dosyalar = [dosya for dosya in os.listdir(klasor) if dosya.endswith(uzantilar)]
    if not dosyalar:
        print(f"{clr.am9}║\n║\n{clr.am5}╠════════════╝ {clr.k}Kategori klasoru bos!{clr.r}")
        helper_func.error_log_write("Kategori klasoru bos!")
        input(f"{clr.am6}║\n╚══════ > Menuye donmek icin bir tusa basin.. {clr.r}")
        main()
        return
    for dosya in dosyalar:
        kategori = "_".join(os.path.splitext(dosya)[0].split("_")[:-2])
        if not kategori:
            kategori = os.path.splitext(dosya)[0]
        yol = os.path.join(klasor, dosya)
        try:
            with open(yol, "r", encoding="utf-8") as f:
                satirlar = [satir.strip() for satir in f if satir.strip()]
                if kategori not in kategoriler:
                    kategoriler[kategori] = 0
                kategoriler[kategori] += len(satirlar)
        except Exception as e:
            print(f"{clr.k}Hata: {dosya} okunamadi -> {e}{clr.r}")
            helper_func.error_log_write(e)
    for kategori, sayi in kategoriler.items():
        print(f"{clr.am6}╠═ {kategori.upper():<20}{clr.r} ➜ {clr.am1}{sayi} link{clr.r}")
    input(f"{clr.am4}║\n╚══════ > Menuye donmek icin bir tusa basin.. {clr.r}")
    main()


# ══════════════════════════════════════════════════════════════════
# 7 — Yardim
# ══════════════════════════════════════════════════════════════════
def yardim():
    print(rf"""{clr.am9}╠═════════════════ Yardim Menusu ═════════════════╗
{clr.am9}║ 1 - Standart Tarama (Thread + Stealth + Skor)
{clr.am5}║ 2 - Gecersiz Link Tespiti (Thread + Stealth)
{clr.am7}║ 3 - Linkleri kategorize et (basit mod)
{clr.am6}║ 4 - Linklerden <title> basligini ceker
{clr.am4}║ 5 - Proxy dosyasindan proxy kontrol
{clr.am3}║ 6 - Her kategoride kac link oldugunu gosterir
{clr.am2}║ 7 - Bu yardim menusunu gosterir
{clr.am8}╠═════════════════════════════════════════════════╝""")
    input(f"{clr.am3}║\n╚══════ > Menuye donmek icin tuslayın.. {clr.r}")
    main()


# ══════════════════════════════════════════════════════════════════
# 0 — Cikis
# ══════════════════════════════════════════════════════════════════
def cikis():
    print(f"{clr.am9}║\n║\n{clr.am5}╚════════════╝ {clr.k}Cikis yapiliyor..{clr.r}")
    sys.exit()


# ══════════════════════════════════════════════════════════════════
# Anonimlik — sadece tarama icinde sorulan adim
# ══════════════════════════════════════════════════════════════════
def _anonimlik_sor() -> StealthConfig:
    print(f"{clr.am6}║")
    print(f"{clr.am6}║  {clr.am3}[1]{clr.r} Standart Gizlilik {clr.d}(Proxy + rastgele baslik + gecikme){clr.r}")
    print(f"{clr.am6}║  {clr.am3}[2]{clr.r} Minimal {clr.d}(Rastgele baslik + gecikme){clr.r}")
    print(f"{clr.am6}║  {clr.am3}[3]{clr.r} Kapali {clr.d}(Eski davranis){clr.r}")

    choice = input(f"{clr.am7}╠═══════ > Anonimlik seviyesi [3]: {clr.r}").strip()

    level_map = {"1": STEALTH_STANDARD, "2": STEALTH_MINIMAL, "3": STEALTH_OFF}
    level = level_map.get(choice, STEALTH_OFF)
    config = StealthConfig.from_level(level)

    if level >= STEALTH_STANDARD:
        if not PROXY_LIST:
            print(f"{clr.am6}║  {clr.s}⚠ Proxy listesi bos.{clr.r}")
            ekle = input(f"{clr.am7}╠═══════ > Proxy eklemek ister misin? [e/H]: {clr.r}").strip().lower()
            if ekle in ("e", "evet", "y", "yes"):
                _proxy_menu()
                if not PROXY_LIST:
                    print(f"{clr.am6}║  {clr.d}→ Proxy olmadan devam ediliyor.{clr.r}")
                    config.use_proxy = False
            else:
                print(f"{clr.am6}║  {clr.d}→ Proxy olmadan devam ediliyor.{clr.r}")
                config.use_proxy = False
        else:
            print(f"{clr.am6}║  {clr.y}✔ {len(PROXY_LIST)} proxy yuklu.{clr.r}")

    labels = {
        STEALTH_OFF: "Kapali",
        STEALTH_MINIMAL: "Minimal",
        STEALTH_STANDARD: "Standart",
    }
    print(f"{clr.am6}║  {clr.am3}► Secilen: {labels.get(level, '?')}{clr.r}")
    return config


# ══════════════════════════════════════════════════════════════════
# URL Girisi — v2 tarzi (yapistir / dosya / regex ayiklama)
# ══════════════════════════════════════════════════════════════════
def _url_girisi() -> list[str]:
    print(f"{clr.am6}║")
    print(f"{clr.am6}║  {clr.s}URL listenizi yapistirin veya dosya yolu girin:{clr.r}")
    print(f"{clr.am6}║  {clr.d}(Bos satirda Enter = bitir, Ctrl+D = bitir){clr.r}")

    lines = []
    try:
        while True:
            line = input(f"  {clr.am3}➤ {clr.r}")
            if not line and lines:
                break
            if not line and not lines:
                continue
            lines.append(line)
    except EOFError:
        pass

    url_input = "\n".join(lines).strip()

    if not url_input:
        print(f"{clr.am6}║  {clr.k}✗ Herhangi bir icerik girilmedi.{clr.r}")
        return []

    if "\n" not in url_input and os.path.isfile(url_input):
        try:
            filepath = url_input
            with open(filepath, 'r', encoding='utf-8') as f:
                url_input = f.read()
            print(f"{clr.am6}║  {clr.d}Dosya okundu: {os.path.basename(filepath)}{clr.r}")
        except Exception as e:
            print(f"{clr.am6}║  {clr.k}✗ Dosya okuma hatasi: {e}{clr.r}")

    full_url_pattern = r'https?://[^\s\)\]"\'<>]+'
    found_urls = re.findall(full_url_pattern, url_input)

    domain_pattern = r'(?<![/\w])(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}(?:/[^\s\)\]"\'<>]*)?'
    potential_domains = re.findall(domain_pattern, url_input)

    existing_endpoints = {re.sub(r'^https?://', '', u).rstrip('/') for u in found_urls}

    for d in potential_domains:
        d_clean = d.rstrip('/')
        if d_clean not in existing_endpoints:
            found_urls.append("https://" + d)
            existing_endpoints.add(d_clean)

    urls = list(dict.fromkeys(found_urls))

    if not urls:
        print(f"{clr.am6}║  {clr.k}✗ Gecerli bir URL bulunamadi.{clr.r}")
        return []

    print(f"{clr.am6}║  {clr.y}✔ {len(urls)} benzersiz URL ayiklandi.{clr.r}")
    return urls


# ══════════════════════════════════════════════════════════════════
# Proxy Menusu — tarama icinde cagirilir
# ══════════════════════════════════════════════════════════════════
def _proxy_menu():
    while True:
        print(rf"""{clr.am9}╠═════════════════════════════════════╗
{clr.am5}║          Proxy Ayarlari             ║
{clr.am9}╠═════════════════════════════════════╣
{clr.am6}║  {clr.am3}[1]{clr.r} Proxy ekle
{clr.am6}║  {clr.am3}[2]{clr.r} Toplu proxy ekle (dosyadan)
{clr.am6}║  {clr.am3}[3]{clr.r} Mevcut proxyleri listele
{clr.am6}║  {clr.am3}[4]{clr.r} Proxy sil
{clr.am6}║  {clr.am3}[5]{clr.r} Proxy baglanti testi
{clr.am6}║  {clr.am3}[6]{clr.r} Tum proxyleri temizle
{clr.am6}║  {clr.d}[0]{clr.r} Geri don""")

        secim = input(f"{clr.am7}╠═══════ > Secim: {clr.r}").strip()

        if secim == "1":
            _proxy_ekle(PROXY_LIST)
        elif secim == "2":
            _proxy_dosyadan_ekle(PROXY_LIST)
        elif secim == "3":
            _proxy_listele(PROXY_LIST)
        elif secim == "4":
            _proxy_sil(PROXY_LIST)
        elif secim == "5":
            _proxy_test(PROXY_LIST)
        elif secim == "6":
            PROXY_LIST.clear()
            print(f"{clr.am6}║  {clr.y}✔ Tum proxyler temizlendi.{clr.r}")
        elif secim == "0" or secim == "":
            break


def _proxy_ekle(proxy_list: list):
    print(f"{clr.am6}║  {clr.d}HTTP   → http://ip:port  veya  http://user:pass@ip:port{clr.r}")
    print(f"{clr.am6}║  {clr.d}SOCKS5 → socks5://ip:port  veya  socks5h://ip:port{clr.r}")
    print(f"{clr.am6}║  {clr.d}(Bos birak = cik){clr.r}")

    while True:
        proxy = input(f"{clr.am7}╠═══════ > Proxy: {clr.r}").strip()
        if not proxy:
            break
        if _proxy_gecerli_mi(proxy):
            if proxy not in proxy_list:
                proxy_list.append(proxy)
                print(f"{clr.am6}║  {clr.y}✔ Eklendi: {proxy}{clr.r}")
            else:
                print(f"{clr.am6}║  {clr.s}⚠ Zaten listede.{clr.r}")
        else:
            print(f"{clr.am6}║  {clr.k}✗ Gecersiz format.{clr.r}")

    print(f"{clr.am6}║  {clr.d}Toplam: {len(proxy_list)} proxy{clr.r}")


def _proxy_dosyadan_ekle(proxy_list: list):
    dosya = input(f"{clr.am7}╠═══════ > Proxy dosya yolu: {clr.r}").strip()
    if not dosya or not os.path.isfile(dosya):
        print(f"{clr.am6}║  {clr.k}✗ Dosya bulunamadi.{clr.r}")
        return

    eklenen = 0
    try:
        with open(dosya, 'r', encoding='utf-8') as f:
            for line in f:
                proxy = line.strip()
                if proxy and not proxy.startswith("#"):
                    if _proxy_gecerli_mi(proxy):
                        if proxy not in proxy_list:
                            proxy_list.append(proxy)
                            eklenen += 1
        print(f"{clr.am6}║  {clr.y}✔ {eklenen} proxy eklendi. Toplam: {len(proxy_list)}{clr.r}")
    except Exception as e:
        print(f"{clr.am6}║  {clr.k}✗ Dosya okuma hatasi: {e}{clr.r}")


def _proxy_listele(proxy_list: list):
    if not proxy_list:
        print(f"{clr.am6}║  {clr.d}Proxy listesi bos.{clr.r}")
        return
    print(f"{clr.am6}║  {clr.b}Mevcut Proxyler ({len(proxy_list)}):{clr.r}")
    for i, p in enumerate(proxy_list, 1):
        tip = "SOCKS5" if "socks" in p else "HTTP"
        gizli = _proxy_gizle(p)
        print(f"{clr.am6}║  {clr.d}[{i}]{clr.r} {clr.am3}{tip:<7}{clr.r} {gizli}")


def _proxy_sil(proxy_list: list):
    if not proxy_list:
        print(f"{clr.am6}║  {clr.d}Proxy listesi bos.{clr.r}")
        return
    _proxy_listele(proxy_list)
    try:
        num = int(input(f"{clr.am7}╠═══════ > Silinecek numara: {clr.r}").strip())
        if 1 <= num <= len(proxy_list):
            silinen = proxy_list.pop(num - 1)
            print(f"{clr.am6}║  {clr.y}✔ Silindi: {_proxy_gizle(silinen)}{clr.r}")
        else:
            print(f"{clr.am6}║  {clr.k}✗ Gecersiz numara.{clr.r}")
    except ValueError:
        print(f"{clr.am6}║  {clr.k}✗ Sayi giriniz.{clr.r}")


def _proxy_test(proxy_list: list):
    if not proxy_list:
        print(f"{clr.am6}║  {clr.d}Proxy listesi bos.{clr.r}")
        return

    import requests as req

    print(f"{clr.am6}║  {clr.d}Test ediliyor...{clr.r}")
    for i, p in enumerate(proxy_list, 1):
        tip = "SOCKS5" if "socks" in p else "HTTP"
        gizli = _proxy_gizle(p)
        try:
            proxies = {"http": p, "https": p}
            resp = req.get("https://httpbin.org/ip", proxies=proxies, timeout=10)
            if resp.status_code == 200:
                ip = resp.json().get("origin", "?")
                print(f"{clr.am6}║  {clr.y}✔ [{i}] {tip} {gizli} → IP: {ip}{clr.r}")
            else:
                print(f"{clr.am6}║  {clr.k}✗ [{i}] {tip} {gizli} → HTTP {resp.status_code}{clr.r}")
        except Exception as e:
            hata = str(e)[:60]
            print(f"{clr.am6}║  {clr.k}✗ [{i}] {tip} {gizli} → {hata}{clr.r}")


def _proxy_gecerli_mi(proxy: str) -> bool:
    gecerli = ("http://", "https://", "socks4://", "socks5://", "socks5h://", "socks4a://")
    return proxy.lower().startswith(gecerli)


def _proxy_gizle(proxy: str) -> str:
    if "@" in proxy:
        protokol, rest = proxy.split("://", 1)
        auth, host = rest.rsplit("@", 1)
        return f"{protokol}://***@{host}"
    return proxy


# ══════════════════════════════════════════════════════════════════
# Menu Yonlendirme
# ══════════════════════════════════════════════════════════════════
def MENU(secilmis):
    secim_haritasi = {
        "0": cikis,
        "1": standart_tarama,
        "2": gecersiz_tarama,
        "3": ctl.baslık_cek,
        "4": proxy_check.check_proxy,
        "5": kategori_elementleri,
        "6": yardim,
    }
    func = secim_haritasi.get(secilmis)
    if func:
        func()
    else:
        print(f"{clr.am9}║\n║\n{clr.am5}╚═══════════╝ {clr.k}Hatali girdi turu! Gecerli bir deger girin{clr.r}")
        helper_func.error_log_write("Hatali girdi turu! Gecerli bir deger girin")


def main():
    helper_func.output_folder()
    os.system("clear" if os.name == "posix" else "cls")
    banner()
    try:
        menu = input(f"""{clr.am1}╔═════════════════════════════════════╗
{clr.am1}║          NexaVista - Menu           ║
{clr.am3}╠═════════════════════════════════════╣
{clr.am3}║ 1 - Standart Tarama                 ║
{clr.am4}║ 2 - Gecersiz Link Tespiti           ║
{clr.am5}║ 3 - Linklerden Baslik Cek           ║
{clr.am5}║ 4 - Proxyleri Kontrol Et            ║
{clr.am6}║ 5 - Kategori Sayilarini Goster      ║
{clr.am7}║ 6 - Hakkinda / Yardim               ║
{clr.am5}║ 0 - Cikis                           ║
{clr.am9}║
{clr.am9}║
{clr.am9}╠═══════╝ $ {clr.r}""")
        MENU(menu)
    except KeyboardInterrupt:
        print(f"{clr.am9}\n║\n║\n{clr.am5}╚════════════╝ {clr.k}Islem sonlandirildi{clr.r}")
    except AttributeError as e:
        print(f"{clr.am9}\n║\n║\n{clr.am5}╚═══════════╝ {clr.k}Hatali girdi turu! Gecerli bir deger girin{clr.r}")
        helper_func.error_log_write(e)
    except TypeError as e:
        print(f"{clr.am9}\n║\n║\n{clr.am5}╚═══════════╝ {clr.k}Hatali girdi turu! Gecerli bir deger girin{clr.r}")
        helper_func.error_log_write(e)
    except Exception as e:
        print(f"{clr.am9}\n║\n║\n{clr.am5}╚════════════╝ {clr.k}Hata: {e}{clr.r}")
        helper_func.error_log_write(e)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n  {clr.s}Cikiliyor...{clr.r}")
        sys.exit(0)
