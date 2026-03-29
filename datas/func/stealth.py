import random
import time
from dataclasses import dataclass, field

from datas.func.config import (
    ACCEPT_LANGUAGES, ACCEPT_ENCODINGS, REFERERS,
    ACCEPT_HEADERS, DNT_VALUES, UPGRADE_INSECURE_VALUES, SEC_FETCH_MODES,
    SEC_FETCH_SITES, SEC_FETCH_DESTS,
    SEC_CH_UA_PLATFORMS, SEC_CH_UA_MOBILE,
    CACHE_CONTROLS, PRAGMA_VALUES, CONNECTION_VALUES,
    PROXY_LIST,
    DELAY_MIN, DELAY_MAX,
    USER_AGENTS, TIMEOUT,
    log,
)


STEALTH_OFF = 0
STEALTH_MINIMAL = 1
STEALTH_STANDARD = 2
STEALTH_FULL = 3


@dataclass
class StealthConfig:
    level: int = STEALTH_OFF
    random_headers: bool = True
    random_delay: bool = False
    use_proxy: bool = False
    use_tls_impersonation: bool = False
    fresh_session: bool = False
    _request_counter: int = field(default=0, repr=False)

    @classmethod
    def from_level(cls, level: int) -> "StealthConfig":
        cfg = cls(level=level)
        if level >= STEALTH_MINIMAL:
            cfg.random_delay = True
        if level >= STEALTH_STANDARD:
            cfg.use_proxy = True
        if level >= STEALTH_FULL:
            cfg.use_tls_impersonation = True
            cfg.fresh_session = True
        return cfg


def rastgele_basliklar() -> dict:
    ua = random.choice(USER_AGENTS)
    headers = {
        "User-Agent": ua,
        "Accept": random.choice(ACCEPT_HEADERS),
        "Accept-Language": random.choice(ACCEPT_LANGUAGES),
        "Accept-Encoding": random.choice(ACCEPT_ENCODINGS),
        "DNT": random.choice(DNT_VALUES),
        "Upgrade-Insecure-Requests": random.choice(UPGRADE_INSECURE_VALUES),
        "Sec-Fetch-Mode": random.choice(SEC_FETCH_MODES),
        "Sec-Fetch-Site": random.choice(SEC_FETCH_SITES),
        "Sec-Fetch-Dest": random.choice(SEC_FETCH_DESTS),
        "Connection": random.choice(CONNECTION_VALUES),
    }

    if random.random() < 0.6:
        ref = random.choice(REFERERS)
        if ref:
            headers["Referer"] = ref

    if random.random() < 0.5:
        cc = random.choice(CACHE_CONTROLS)
        if cc:
            headers["Cache-Control"] = cc

    if random.random() < 0.3:
        pg = random.choice(PRAGMA_VALUES)
        if pg:
            headers["Pragma"] = pg

    if "Chrome" in ua and "Safari" in ua:
        platform = random.choice(SEC_CH_UA_PLATFORMS)
        mobile = random.choice(SEC_CH_UA_MOBILE)
        chrome_ver = "124"
        if "Chrome/" in ua:
            try:
                chrome_ver = ua.split("Chrome/")[1].split(".")[0]
            except (IndexError, ValueError):
                pass
        headers["Sec-Ch-Ua"] = f'"Chromium";v="{chrome_ver}", "Google Chrome";v="{chrome_ver}", "Not A(Brand";v="99"'
        headers["Sec-Ch-Ua-Mobile"] = mobile
        headers["Sec-Ch-Ua-Platform"] = platform

    return headers


def rastgele_gecikme():
    sure = random.uniform(DELAY_MIN, DELAY_MAX)
    time.sleep(sure)


def proxy_sec() -> dict | None:
    if not PROXY_LIST:
        return None
    proxy = random.choice(PROXY_LIST)
    return {"http": proxy, "https": proxy}


def taze_oturum(tls_impersonation: bool = False, existing_session=None):
    if existing_session and not tls_impersonation:
        return existing_session, "requests"

    if tls_impersonation:
        try:
            from curl_cffi.requests import Session as CurlSession
            tarayici_listesi = (
                "chrome110", "chrome116", "chrome119", "chrome120", "chrome124", "chrome131",
                "safari17_0", "firefox117", "firefox120", "edge101"
            )
            session = CurlSession(impersonate=random.choice(tarayici_listesi))
            return session, "curl_cffi"
        except ImportError:
            log.warning("curl_cffi yuklu degil, requests'e geciliyor.")

    import requests
    session = requests.Session()
    return session, "requests"


def stealth_ayarla(config: StealthConfig, existing_session=None) -> tuple[dict, dict | None, object, str]:
    headers = rastgele_basliklar()

    proxies = None
    if config.use_proxy:
        proxies = proxy_sec()

    session, engine = taze_oturum(
        tls_impersonation=config.use_tls_impersonation,
        existing_session=existing_session if not config.fresh_session else None
    )

    if config.random_delay:
        rastgele_gecikme()

    return headers, proxies, session, engine
