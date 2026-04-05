"""
analyzer.py — Link Analyzer ana modülü
NexaVista'nın asıl çekirdek görevi burada referanslanır.
Tüm tarama fonksiyonları datas/func/ altındaki modüllerden çekilir.
"""
# Bu modül datas/func altındaki scanner, manager, reporter vb. kullanır.
# Doğrudan NexaVista.py'den çağrılır, burada sadece referans.

from modules.scanner.manager import NexaVista
from modules.scanner.scanner import scan_single_url
from modules.scanner import reporter
from modules.scanner import check_tittle as ctl
from modules.scanner import notfoundlinks as nfl
from core.stealth import StealthConfig

__all__ = [
    "NexaVista",
    "scan_single_url",
    "reporter",
    "ctl",
    "nfl",
    "StealthConfig",
]
