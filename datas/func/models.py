from dataclasses import dataclass, field


@dataclass
class LinkResult:
    url: str
    status_code: int = 0
    reachable: bool = False
    response_time_ms: float = 0.0
    content_type: str = ""
    title: str = ""
    description: str = ""
    keywords: list = field(default_factory=list)
    headings: list = field(default_factory=list)
    outbound_links: int = 0
    content_hash: str = ""
    category: str = "unknown"
    category_confidence: float = 0.0
    score: int = 0
    score_breakdown: dict = field(default_factory=dict)
    ssl_valid: bool = False
    redirect_count: int = 0
    final_url: str = ""
    scanned_at: str = ""
    error: str = ""
