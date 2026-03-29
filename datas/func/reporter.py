import os
import re
import json
import xml.etree.ElementTree as ET
from datetime import datetime
from urllib.parse import urlparse
from dataclasses import asdict

import clr
from datas.func.models import LinkResult
from datas.func.analyzer import score_color
from datas.func.config import OUTPUT_DIR
from datas.data.categories import CATEGORIES


def _strip_ansi(text: str) -> str:
    return re.sub(r'\033\[[0-9;]*m', '', text)


def print_report(results: list[LinkResult], log_file_path: str = None):
    report_lines = []

    def _out(text: str = ""):
        print(text)
        report_lines.append(text)

    _out(f"\n\n{clr.b}{clr.am3}{'═'*70}{clr.r}")
    _out(f"{clr.b}{clr.am3}  📊  NEXAVISTA RAPORU  •  {datetime.now().strftime('%d/%m/%Y %H:%M')}{clr.r}")
    _out(f"{clr.b}{clr.am3}{'═'*70}{clr.r}\n")

    total = len(results)
    reachable = [r for r in results if r.reachable]
    unreachable = [r for r in results if not r.reachable]
    reachable_count = max(len(reachable), 1)
    avg_score = sum(r.score for r in reachable) / reachable_count
    avg_time = sum(r.response_time_ms for r in reachable) / reachable_count
    ssl_count = sum(1 for r in results if r.ssl_valid)

    _out(f"  {'Toplam URL':<28} {clr.b}{total}{clr.r}")
    _out(f"  {'Erisilebilir':<28} {clr.y}{len(reachable)}{clr.r}")
    _out(f"  {'Erisilemeyen':<28} {clr.k}{len(unreachable)}{clr.r}")
    _out(f"  {'SSL/HTTPS':<28} {clr.am3}{ssl_count}{clr.r}")
    _out(f"  {'Ort. Yanit Suresi':<28} {clr.s}{avg_time:.0f} ms{clr.r}")
    _out(f"  {'Ort. Kalite Skoru':<28} {score_color(int(avg_score))}{avg_score:.1f}/100{clr.r}")

    _out(f"\n  {clr.b}── Kategori Dagilimi ──────────────────────────────────{clr.r}")
    cat_counts: dict[str, int] = {}
    for r in results:
        cat_counts[r.category] = cat_counts.get(r.category, 0) + 1
    for cat, cnt in sorted(cat_counts.items(), key=lambda x: -x[1]):
        icon = CATEGORIES.get(cat, {}).get("icon", "🔗")
        bar = "▓" * cnt + "░" * (total - cnt)
        pct = cnt / total * 100
        _out(f"  {icon} {cat:<16} {clr.am3}{cnt:>3}{clr.r}  [{bar[:30]}] {pct:.0f}%")

    _out(f"\n  {clr.b}── En Yuksek Skorlu Linkler ───────────────────────────{clr.r}")
    top5 = sorted(reachable, key=lambda r: r.score, reverse=True)[:5]
    for i, r in enumerate(top5, 1):
        sc = score_color(r.score)
        icon = CATEGORIES.get(r.category, {}).get("icon", "🔗")
        _out(f"  {i}. {sc}{r.score:>3}/100{clr.r}  {icon} {r.url[:55]}")
        if r.title:
            _out(f"       {clr.d}↳ {r.title[:60]}{clr.r}")

    if reachable:
        _out(f"\n  {clr.b}── En Yavas Yanit Verenler ────────────────────────────{clr.r}")
        slow3 = sorted(reachable, key=lambda r: r.response_time_ms, reverse=True)[:3]
        for r in slow3:
            _out(f"  {clr.k}{r.response_time_ms:.0f} ms{clr.r}  {r.url[:60]}")

    if unreachable:
        _out(f"\n  {clr.b}── Erisilemeyen URLler ────────────────────────────────{clr.r}")
        for r in unreachable:
            err = r.error or f"HTTP {r.status_code}"
            _out(f"  {clr.k}✗{clr.r}  {r.url[:55]}  {clr.d}[{err}]{clr.r}")

    _out(f"\n{clr.am3}{'═'*70}{clr.r}\n")

    domain_groups: dict[str, list[LinkResult]] = {}
    for r in results:
        d = urlparse(r.url).netloc.lower().lstrip('www.')
        domain_groups.setdefault(d, []).append(r)
    dupes = {d: rs for d, rs in domain_groups.items() if len(rs) > 1}
    if dupes:
        _out(f"  {clr.b}── Ayni Domain'e Ait Linkler (Duplikasyon) ────────────{clr.r}")
        for domain, rs in dupes.items():
            _out(f"\n  {clr.s}🔁 {domain}{clr.r} ({len(rs)} link):")
            for r in rs:
                _out(f"     {clr.d}→ {r.url}{clr.r}")
        _out(f"\n{clr.am3}{'═'*70}{clr.r}\n")

    if log_file_path:
        os.makedirs(os.path.dirname(log_file_path), exist_ok=True)
        with open(log_file_path, "w", encoding="utf-8") as f:
            f.write("\n".join(_strip_ansi(line) for line in report_lines))


def print_invalid_report(results: list[LinkResult], log_file_path: str = None):
    invalid = [r for r in results if not r.reachable]
    valid = [r for r in results if r.reachable]
    report_lines = []

    def _out(text: str = ""):
        print(text)
        report_lines.append(text)

    _out(f"\n\n{clr.b}{clr.k}{'═'*70}{clr.r}")
    _out(f"{clr.b}{clr.k}  🚫  GECERSIZ LINK RAPORU  •  {datetime.now().strftime('%d/%m/%Y %H:%M')}{clr.r}")
    _out(f"{clr.b}{clr.k}{'═'*70}{clr.r}\n")

    _out(f"  {'Toplam URL':<28} {clr.b}{len(results)}{clr.r}")
    _out(f"  {'Gecerli (Erisilebilir)':<28} {clr.y}{len(valid)}{clr.r}")
    _out(f"  {'Gecersiz (Erisilemez)':<28} {clr.k}{len(invalid)}{clr.r}")
    _out(f"  {'Gecersiz Orani':<28} {clr.k}{len(invalid)/max(len(results),1)*100:.1f}%{clr.r}")

    if invalid:
        _out(f"\n  {clr.b}── Gecersiz Linkler ───────────────────────────────────{clr.r}")
        for i, r in enumerate(invalid, 1):
            err = r.error or f"HTTP {r.status_code}"
            _out(f"  {clr.k}{i:>3}. ✗{clr.r}  {r.url}")
            _out(f"       {clr.d}Hata: {err}{clr.r}")
            if r.status_code:
                _out(f"       {clr.d}Durum Kodu: {r.status_code}{clr.r}")
    else:
        _out(f"\n  {clr.y}✔ Tum linkler gecerli! Hicbir kirik link bulunamadi.{clr.r}")

    _out(f"\n{clr.k}{'═'*70}{clr.r}\n")

    if log_file_path:
        os.makedirs(os.path.dirname(log_file_path), exist_ok=True)
        with open(log_file_path, "w", encoding="utf-8") as f:
            f.write("\n".join(_strip_ansi(line) for line in report_lines))


def save_results(results: list[LinkResult], scan_dir: str):
    os.makedirs(scan_dir, exist_ok=True)

    reachable_links = [r for r in results if r.reachable]
    reachable_count = len(reachable_links)

    payload = {
        "meta": {
            "tool": "NexaVista v3.0",
            "scanned_at": datetime.now().isoformat(),
            "total": len(results),
            "reachable": reachable_count,
            "avg_score": round(
                sum(r.score for r in reachable_links) / max(reachable_count, 1), 1
            ) if reachable_count > 0 else 0.0,
        },
        "results": [asdict(r) for r in results],
    }
    summary_file = os.path.join(scan_dir, "results.json")
    with open(summary_file, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

    print(f"  {clr.y}✔ Sonuclar kaydedildi:{clr.r} {scan_dir}\n")


def save_invalid_results(results: list[LinkResult], scan_dir: str):
    os.makedirs(scan_dir, exist_ok=True)
    invalid = [r for r in results if not r.reachable]
    payload = {
        "meta": {
            "tool": "NexaVista v3.0 - Invalid Links",
            "scanned_at": datetime.now().isoformat(),
            "total_scanned": len(results),
            "invalid_count": len(invalid),
        },
        "invalid_links": [asdict(r) for r in invalid],
    }
    out_file = os.path.join(scan_dir, "invalid_links.json")
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    print(f"  {clr.y}✔ Gecersiz linkler kaydedildi:{clr.r} {out_file}\n")


def export_results(results: list[LinkResult], scan_dir: str, formats: list[str]):
    for fmt in formats:
        fmt = fmt.strip().lower()
        if fmt == "md":
            _export_md(results, scan_dir)
        elif fmt == "txt":
            _export_txt(results, scan_dir)
        elif fmt == "html":
            _export_html(results, scan_dir)
        elif fmt == "xml":
            _export_xml(results, scan_dir)
        elif fmt == "js":
            _export_js(results, scan_dir)
        elif fmt == "json":
            pass
        else:
            print(f"  {clr.k}✗ Bilinmeyen format: {fmt}{clr.r}")


def _export_md(results: list[LinkResult], scan_dir: str):
    path = os.path.join(scan_dir, "results.md")
    lines = ["# NexaVista Tarama Raporu\n"]
    lines.append(f"**Tarih:** {datetime.now().strftime('%d/%m/%Y %H:%M')}  ")
    lines.append(f"**Toplam:** {len(results)} URL\n")

    cat_map: dict[str, list[LinkResult]] = {}
    for r in results:
        cat_map.setdefault(r.category, []).append(r)

    for cat, items in sorted(cat_map.items()):
        icon = CATEGORIES.get(cat, {}).get("icon", "🔗")
        lines.append(f"\n## {icon} {cat.title()} ({len(items)})\n")
        for r in items:
            status = "✅" if r.reachable else "❌"
            lines.append(f"- {status} **[{r.title or r.url}]({r.url})** — Skor: {r.score}/100, {r.response_time_ms:.0f}ms")
            if r.description:
                lines.append(f"  > {r.description[:120]}")

    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"  {clr.y}✔ MD disa aktarildi:{clr.r} {path}")


def _export_txt(results: list[LinkResult], scan_dir: str):
    path = os.path.join(scan_dir, "results.txt")
    lines = ["NEXAVISTA TARAMA RAPORU", "=" * 50]
    lines.append(f"Tarih: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    lines.append(f"Toplam: {len(results)} URL\n")
    for r in results:
        status = "[OK]" if r.reachable else "[FAIL]"
        lines.append(f"{status} {r.url}")
        lines.append(f"    Baslik:    {r.title}")
        lines.append(f"    Kategori:  {r.category}")
        lines.append(f"    Skor:      {r.score}/100")
        lines.append(f"    Sure:      {r.response_time_ms:.0f}ms")
        lines.append("")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"  {clr.y}✔ TXT disa aktarildi:{clr.r} {path}")


def _export_html(results: list[LinkResult], scan_dir: str):
    path = os.path.join(scan_dir, "results.html")
    rows = ""

    cat_counts = {}
    for r in results:
        cat_counts[r.category] = cat_counts.get(r.category, 0) + 1
    cat_labels = list(cat_counts.keys())
    cat_data = list(cat_counts.values())

    scores = {"0-25": 0, "26-50": 0, "51-75": 0, "76-100": 0}
    for r in results:
        if r.score <= 25: scores["0-25"] += 1
        elif r.score <= 50: scores["26-50"] += 1
        elif r.score <= 75: scores["51-75"] += 1
        else: scores["76-100"] += 1
    score_data = list(scores.values())

    for r in results:
        sc = "#2ecc71" if r.score >= 75 else "#f39c12" if r.score >= 50 else "#e74c3c"
        status = "✅" if r.reachable else "❌"
        rows += f"""<tr>
            <td>{status}</td>
            <td><a href="{r.url}" target="_blank">{r.title or r.url}</a></td>
            <td>{r.category}</td>
            <td style="color:{sc};font-weight:bold">{r.score}/100</td>
            <td>{r.response_time_ms:.0f}ms</td>
        </tr>\n"""

    html = f"""<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="utf-8">
<title>NexaVista Kapsamli HTML Raporu</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<style>
  body {{ font-family: 'Segoe UI', system-ui, sans-serif; background: #0f111a; color: #e2e8f0; padding: 2em; margin: 0; }}
  .container {{ max-width: 1200px; margin: 0 auto; }}
  h1 {{ color: #38bdf8; text-align: center; font-size: 2.5em; text-transform: uppercase; letter-spacing: 2px; }}
  .meta {{ text-align:center; color: #94a3b8; margin-bottom: 2em; font-size: 1.1em; }}
  .dashboard {{ display: flex; gap: 20px; margin-bottom: 40px; justify-content: center; flex-wrap: wrap; }}
  .chart-card {{ background: #1e293b; padding: 20px; border-radius: 12px; width: 45%; box-shadow: 0 10px 15px -3px rgba(0,0,0,0.5); border: 1px solid #334155; }}
  table {{ width: 100%; border-collapse: collapse; background: #1e293b; border-radius: 12px; overflow: hidden; box-shadow: 0 10px 15px -3px rgba(0,0,0,0.5); border: 1px solid #334155; }}
  th, td {{ padding: 14px 20px; text-align: left; border-bottom: 1px solid #334155; }}
  th {{ background: #0f172a; color: #38bdf8; font-weight: 600; font-size: 1.1em; text-transform: uppercase; letter-spacing: 1px; }}
  tr:last-child td {{ border-bottom: none; }}
  tr:hover {{ background: #334155; transition: 0.2s ease-in-out; }}
  a {{ color: #fb7185; text-decoration: none; font-weight: 500; }}
  a:hover {{ text-decoration: underline; color: #f43f5e; }}
</style>
</head>
<body>
<div class="container">
    <h1>📊 NexaVista Analiz Raporu</h1>
    <p class="meta">Tarih: {datetime.now().strftime('%d/%m/%Y %H:%M')} &nbsp;|&nbsp; Toplam: {len(results)} URL</p>

    <div class="dashboard">
        <div class="chart-card">
            <canvas id="categoryChart"></canvas>
        </div>
        <div class="chart-card">
            <canvas id="scoreChart"></canvas>
        </div>
    </div>

    <table>
      <tr><th>Durum</th><th>URL Bilgisi</th><th>Kategori</th><th>Kalite Skoru</th><th>Yanit Suresi</th></tr>
      {rows}
    </table>
</div>

<script>
Chart.defaults.color = '#cbd5e1';
Chart.defaults.font.family = "'Segoe UI', system-ui, sans-serif";

const ctxCat = document.getElementById('categoryChart').getContext('2d');
new Chart(ctxCat, {{
    type: 'doughnut',
    data: {{
        labels: {cat_labels},
        datasets: [{{
            data: {cat_data},
            backgroundColor: ['#f43f5e', '#3b82f6', '#38bdf8', '#fbbf24', '#a855f7', '#22c55e', '#f97316', '#14b8a6'],
            borderWidth: 2,
            borderColor: '#1e293b'
        }}]
    }},
    options: {{
        responsive: true,
        plugins: {{
            title: {{ display: true, text: 'URL Kategori Dagilimi (AI)', color: '#f8fafc', font: {{ size: 18 }} }},
            legend: {{ position: 'right', labels: {{ padding: 20 }} }}
        }}
    }}
}});

const ctxScore = document.getElementById('scoreChart').getContext('2d');
new Chart(ctxScore, {{
    type: 'bar',
    data: {{
        labels: ['Kritik (0-25)', 'Zayif (26-50)', 'Iyi (51-75)', 'Mukemmel (76-100)'],
        datasets: [{{
            label: 'URL Adedi',
            data: {score_data},
            backgroundColor: ['#ef4444', '#f59e0b', '#eab308', '#10b981'],
            borderRadius: 6,
            barPercentage: 0.6
        }}]
    }},
    options: {{
        responsive: true,
        plugins: {{
            title: {{ display: true, text: 'Icerik Kalite Skorlari', color: '#f8fafc', font: {{ size: 18 }} }},
            legend: {{ display: false }}
        }},
        scales: {{
            y: {{ beginAtZero: true, ticks: {{ stepSize: 1 }}, grid: {{ color: '#334155', drawBorder: false }} }},
            x: {{ grid: {{ display: false }} }}
        }}
    }}
}});
</script>
</body>
</html>"""
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"  {clr.y}✔ HTML disa aktarildi:{clr.r} {path}")


def _export_xml(results: list[LinkResult], scan_dir: str):
    path = os.path.join(scan_dir, "results.xml")
    root = ET.Element("nexavista")
    meta = ET.SubElement(root, "meta")
    ET.SubElement(meta, "tool").text = "NexaVista v3.0"
    ET.SubElement(meta, "scanned_at").text = datetime.now().isoformat()
    ET.SubElement(meta, "total").text = str(len(results))

    items = ET.SubElement(root, "results")
    for r in results:
        item = ET.SubElement(items, "link")
        ET.SubElement(item, "url").text = r.url
        ET.SubElement(item, "title").text = r.title
        ET.SubElement(item, "category").text = r.category
        ET.SubElement(item, "score").text = str(r.score)
        ET.SubElement(item, "reachable").text = str(r.reachable)
        ET.SubElement(item, "response_time_ms").text = str(r.response_time_ms)
        ET.SubElement(item, "status_code").text = str(r.status_code)
        ET.SubElement(item, "description").text = r.description

    tree = ET.ElementTree(root)
    ET.indent(tree, space="  ")
    tree.write(path, encoding="unicode", xml_declaration=True)
    print(f"  {clr.y}✔ XML disa aktarildi:{clr.r} {path}")


def _export_js(results: list[LinkResult], scan_dir: str):
    path = os.path.join(scan_dir, "results.js")
    data = json.dumps([asdict(r) for r in results], ensure_ascii=False, indent=2)
    js_content = f"// NexaVista Tarama Sonuclari\n// Tarih: {datetime.now().isoformat()}\nconst nexavistaResults = {data};\n"
    with open(path, "w", encoding="utf-8") as f:
        f.write(js_content)
    print(f"  {clr.y}✔ JS disa aktarildi:{clr.r} {path}")
