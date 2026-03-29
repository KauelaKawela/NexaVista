# 🌐 NexaVista v3.0

NexaVista, toplu web bağlantılarını (URL) analiz etmek, durum kodlarını (HTTP status) kontrol etmek, içeriklerini tarayarak akıllı kategorilere ayırmak ve erişilebilirlik, hız, TLS/SSL geçerliliğine göre puanlamak için tasarlanmış kapsamlı, terminal tabanlı bir analiz aracıdır. Gelişmiş *Stealth (Gizlilik)* modları ve çoklu iş parçacığı (multi-threading) desteği ile yüksek performans ve güvenlik sunar.

![NexaVista](https://img.shields.io/badge/version-3.0-blue) ![Python](https://img.shields.io/badge/python-3.8+-green)

---

## 🚀 Öne Çıkan Özellikler

*   **⚡ Yüksek Performanslı Tarama (Multi-Threading)**: Aynı anda 100'e kadar iş parçacığı (thread) ile binlerce bağlantıyı çok kısa sürede tarama.
*   **🕵️ Gelişmiş Gizlilik (Stealth) Modları**: 
    *   Farklı User-Agent rotasyonları.
    *   Rastgele gecikme süreleri (Delay).
    *   HTTP/HTTPS ve SOCKS5 proxy desteği.
    *   TLS impersonation (İsteğe bağlı gelişmiş izinsiz tarama engellerini aşma).
*   **🧠 Akıllı Sınıflandırma ve Skorlama**: İçeriğe (meta tags, title, keywords) bakarak URL'leri teknoloji, alışveriş, haber vb. kategorilere ayırır. Yanıt süresine ve SSL durumuna göre puan (Score) ataması yapar.
*   **📄 Kapsamlı Raporlama ve Dışa Aktarma**: Tarama sonuçlarını `MD`, `TXT`, `HTML`, `XML`, `JSON` veya `CSV` formatlarında dışa aktarma seçeneği.
*   **☠️ Kırık Link (Dead Link) Tespiti**: Çalışmayan, "Not Found" döndüren veya "Domain Satışta" (Parked Domain) tarzı siteleri tespit etme.
*   **🛡️ Kendi Proxy Test Cihazı**: Elinizdeki proxylerin çalışıp çalışmadığını, HTTP/SOCKS türlerini test edebilirsiniz.
*   **📑 Başlık (Title) Çekici**: Sitelehttps://img.shields.io/badge/version-3.0-bluerin HTML yapısına girip `<title>` etiketlerini otomatik olarak çıkartır.
*   **📂 Düzenli Veri Yönetimi**: Loglanan her dosya, çıktı ve tarama işlemi düzenli bir şekilde `datas/output/` ve `datas/log/` klasöründe tutulurken uygulamanın bulunduğu ana dizin tamamen temiz kalır.

---

## 📦 Kurulum ve Gereksinimler

- Python 3.x
- Gerekli kütüphaneleri indirmek için:

```bash
git clone https://github.com/KauelaKawela/nexavista.git
cd nexavista
pip install -r requirements.txt
python3 NexaVista.py
```

---

## 🕹️ Menü ve Kullanım

NexaVista.py çalıştırıldığında kullanıcı dostu interaktif bir menü ile karşılaşırsınız:

1.  **Standart Tarama**: Linklerinizi girin, gizlilik seviyesini ve thread sayısını belirleyin, kapsamlı bir analiz alın.
2.  **Geçersiz Link Tespiti**: Sadece çalışmayan/ölü siteleri tespit etmek için kullanılan hızlı tarama.
3.  **Linklerden Başlık Çek**: Girilen URL'lerin sekme başlıklarını (title) çeker.
4.  **Proxyleri Kontrol Et**: Kendi proxy listelerinizi test edin.
5.  **Kategori Sayılarını Göster**: Daha önce sınıflandırması yapılmış (`datas/output/` içerisindeki) dosyaların istatistiklerini gösterir.
6.  **Yardım**: Modüller ve kullanım hakkında kısa ipuçları.

---

# 🌐 NexaVista v3.0 (English)

**NexaVista** is an advanced, terminal-based Python analysis tool designed to mass-analyze web links. It checks HTTP status codes, parses content to smartly categorize domains, and assigns scores based on reachability, response speed, and TLS/SSL validity. With cutting-edge *Stealth* modes and multi-threading, it delivers high performance and security combined.

## 🚀 Core Features

*   **⚡ Multi-Threaded Scanning**: Supports up to 100 concurrent threads to scan thousands of URLs in a matter of seconds.
*   **🕵️ Advanced Stealth Modes**: 
    *   User-Agent rotations.
    *   Random execution delays.
    *   HTTP/HTTPS and SOCKS5 Proxy integration.
    *   TLS impersonation capabilities.
*   **🧠 Intelligent Categorization & Scoring**: Divides URLs into precise categories (Tech, News, Shopping, etc.) by analyzing meta content. Calculates an overall health score based on SSL validity and response time MS.
*   **📄 Comprehensive Export Options**: Seamlessly export scan results into `MD`, `TXT`, `HTML`, `XML`, `JSON` or `CSV` formats directly to the categorized output directory.
*   **☠️ Dead Link Finder**: Specialized mode to isolate dead, unreachable, or parked domains rapidly.
*   **🛡️ Built-in Proxy Checker**: Test the functionality and anonymity of your proxy lists right within the application.
*   **📑 Mass Title Extractor**: Extracts `<title>` tags across multiple URLs out of the box.
*   **📂 Neat Workspace**: Output and logging structures are tightly coupled inside the `datas/` directory, keeping the project's root folder completely unpolluted.

## 📦 Requirements & Installation

- Python 3.x
- Required libraries:

```bash
git clone https://github.com/KauelaKawela/nexavista.git
cd nexavista
pip install -r requirements.txt
python3 NexaVista.py
```
