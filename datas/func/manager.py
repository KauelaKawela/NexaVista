import sys
import threading
from urllib.parse import urlparse
from concurrent.futures import ThreadPoolExecutor, as_completed

import clr
from datas.func.models import LinkResult
from datas.func.scanner import LinkScanner
from datas.func.analyzer import score_color
from datas.func.stealth import StealthConfig, STEALTH_OFF
from datas.data.categories import CATEGORIES


class NexaVista:
    def __init__(self, max_workers: int = 10, stealth_config: StealthConfig | None = None):
        self.max_workers = max_workers
        self.stealth = stealth_config or StealthConfig(level=STEALTH_OFF)
        self.scanner = LinkScanner(stealth_config=self.stealth)
        self.results: list[LinkResult] = []
        self._progress = 0
        self._total = 0
        self._lock = threading.Lock()

    def scan_urls(self, urls: list[str]) -> list[LinkResult]:
        self._total = len(urls)
        self._progress = 0
        results = []

        stealth_label = self._stealth_label()
        print(f"\n{clr.am3}  ▶ Tarama basliyor: {self._total} URL | {self.max_workers} thread | {stealth_label}{clr.r}\n")

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_map = {executor.submit(self._scan_one, url): url for url in urls}
            for future in as_completed(future_map):
                result = future.result()
                results.append(result)
                self._print_progress(result)

        url_order = {u: i for i, u in enumerate(urls)}
        results.sort(key=lambda r: url_order.get(r.url, 9999))
        self.results = results
        return results

    def _scan_one(self, url: str) -> LinkResult:
        result = self.scanner.fetch(url)
        result.score, result.score_breakdown = self.scanner.calculate_score(result)
        with self._lock:
            self._progress += 1
        return result

    def _stealth_label(self) -> str:
        labels = {
            0: f"{clr.d}Anonimlik: Kapali{clr.r}",
            1: f"{clr.s}Minimal Gizlilik{clr.r}",
            2: f"{clr.y}Standart Gizlilik{clr.r}",
            3: f"{clr.am6}Tam Gizlilik{clr.r}",
        }
        return labels.get(self.stealth.level, f"Seviye {self.stealth.level}")

    def _print_progress(self, r: LinkResult):
        with self._lock:
            pct = int((self._progress / self._total) * 40)
            bar = "█" * pct + "░" * (40 - pct)
            status_color = clr.y if r.reachable else clr.k
            status_icon = "✓" if r.reachable else "✗"
            sc = score_color(r.score)
            domain = urlparse(r.url).netloc[:35]
            sys.stdout.write(
                f"\r  [{bar}] {self._progress}/{self._total}  "
                f"{status_color}{status_icon}{clr.r} {domain:<36} "
                f"[{sc}Score:{r.score:>3}{clr.r}] "
                f"{clr.s}{r.category:<14}{clr.r} "
                f"{r.response_time_ms:>6.0f}ms"
            )
            sys.stdout.flush()
