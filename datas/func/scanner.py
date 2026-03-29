import re
import time
import random
import threading
from datetime import datetime
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup

from datas.func.models import LinkResult
from datas.func.config import USER_AGENTS, TIMEOUT, MAX_CONTENT_BYTES, log
from datas.func.analyzer import categorize
from datas.func.stealth import (
    StealthConfig, STEALTH_OFF,
    stealth_ayarla,
)
from datas.data.categories import SCORE_WEIGHTS


class LinkScanner:
    def __init__(self, stealth_config: StealthConfig | None = None):
        self._lock = threading.Lock()
        self.stealth = stealth_config or StealthConfig(level=STEALTH_OFF)
        self._persistent_session = None
        self._persistent_engine = None

    def fetch(self, url: str) -> LinkResult:
        result = LinkResult(url=url, scanned_at=datetime.now().isoformat())
        try:
            headers, proxies, session, engine = stealth_ayarla(
                self.stealth,
                existing_session=self._persistent_session
            )

            if not self.stealth.fresh_session and self._persistent_session is None:
                self._persistent_session = session
                self._persistent_engine = engine

            t0 = time.perf_counter()

            if engine == "curl_cffi":
                resp = self._fetch_curl(session, url, headers, proxies)
            else:
                resp = self._fetch_requests(session, url, headers, proxies)

            result.response_time_ms = round((time.perf_counter() - t0) * 1000, 1)
            result.status_code = resp.status_code
            result.reachable = resp.status_code < 400
            result.content_type = resp.headers.get("Content-Type", "")
            result.ssl_valid = url.startswith("https://")
            result.redirect_count = len(resp.history) if hasattr(resp, 'history') and resp.history else 0
            result.final_url = str(resp.url) if hasattr(resp, 'url') else url

            if "text/html" in result.content_type and result.reachable:
                html = self._read_body(resp, engine)
                self._parse_html(result, html)

        except requests.exceptions.SSLError:
            result.error = "SSL Error"
            result.ssl_valid = False
        except requests.exceptions.ConnectionError:
            result.error = "Connection Error"
        except requests.exceptions.Timeout:
            result.error = "Timeout"
        except Exception as e:
            error_msg = str(e)[:120]
            if "SSL" in error_msg or "ssl" in error_msg:
                result.error = "SSL Error"
                result.ssl_valid = False
            elif "timed out" in error_msg.lower() or "timeout" in error_msg.lower():
                result.error = "Timeout"
            elif "connection" in error_msg.lower():
                result.error = "Connection Error"
            else:
                result.error = error_msg

        return result

    def _fetch_requests(self, session, url, headers, proxies):
        return session.get(
            url,
            headers=headers,
            timeout=TIMEOUT,
            allow_redirects=True,
            stream=True,
            proxies=proxies,
        )

    def _fetch_curl(self, session, url, headers, proxies):
        kwargs = {
            "headers": headers,
            "timeout": TIMEOUT,
            "allow_redirects": True,
        }
        if proxies:
            proxy_url = proxies.get("https") or proxies.get("http")
            if proxy_url:
                kwargs["proxy"] = proxy_url
        return session.get(url, **kwargs)

    def _read_body(self, resp, engine: str) -> str:
        if engine == "curl_cffi":
            text = resp.text
            if len(text) > MAX_CONTENT_BYTES:
                text = text[:MAX_CONTENT_BYTES]
            return text
        else:
            raw = b""
            for chunk in resp.iter_content(8192):
                raw += chunk
                if len(raw) >= MAX_CONTENT_BYTES:
                    break
            return raw.decode("utf-8", errors="replace")

    def _parse_html(self, result: LinkResult, html: str):
        soup = BeautifulSoup(html, "html.parser")

        title_tag = soup.find("title")
        result.title = title_tag.get_text(strip=True)[:200] if title_tag else ""

        meta_desc = soup.find("meta", attrs={"name": lambda x: x and x.lower() == "description"})
        if meta_desc and meta_desc.get("content"):
            result.description = meta_desc["content"][:400]

        meta_kw = soup.find("meta", attrs={"name": lambda x: x and x.lower() == "keywords"})
        if meta_kw and meta_kw.get("content"):
            result.keywords = [k.strip() for k in meta_kw["content"].split(",")][:20]

        headings = []
        for tag in soup.find_all(["h1", "h2", "h3"])[:15]:
            text = tag.get_text(strip=True)
            if text:
                headings.append(text[:100])
        result.headings = headings

        result.outbound_links = len(soup.find_all("a", href=True))

        parsed_url = urlparse(result.url)
        text_corpus = " ".join([
            result.title,
            result.description,
            " ".join(result.keywords),
            " ".join(result.headings),
            parsed_url.netloc,
            parsed_url.path,
        ]).lower()
        result.category, result.category_confidence = categorize(text_corpus, result.url)

    def calculate_score(self, r: LinkResult) -> tuple[int, dict]:
        bd: dict[str, int] = {}
        w = SCORE_WEIGHTS

        if r.reachable:
            if r.status_code == 200:
                bd["reachability"] = w["status_200"]
            elif r.status_code in (301, 302):
                bd["reachability"] = w["status_redirect"]
            else:
                bd["reachability"] = w["status_other"]
        else:
            bd["reachability"] = 0

        if r.response_time_ms > 0:
            if r.response_time_ms < 500:
                bd["speed"] = w["speed_fast"]
            elif r.response_time_ms < 1500:
                bd["speed"] = w["speed_medium"]
            elif r.response_time_ms < 3000:
                bd["speed"] = w["speed_slow"]
            else:
                bd["speed"] = w["speed_veryslow"]
        else:
            bd["speed"] = 0

        bd["ssl"] = w["ssl_valid"] if r.ssl_valid else 0

        content_score = 0
        if r.title:
            content_score += w["has_title"]
        if r.description:
            content_score += w["has_description"]
        if r.keywords:
            content_score += w["has_keywords"]
        if len(r.headings) >= 3:
            content_score += w["has_headings"]
        bd["content"] = min(content_score, w["content_max"])

        bd["redirect_penalty"] = -r.redirect_count * w["redirect_penalty"]
        bd["category_confidence"] = round(r.category_confidence * w["confidence_max"])

        total = min(100, max(0, sum(bd.values())))
        return total, bd
