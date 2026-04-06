# 🌐 NexaVista v3.0

NexaVista, siber güvenlik araştırmacıları, ağ yöneticileri ve geliştiriciler için tasarlanmış, çok amaçlı ve kapsamlı bir terminal tabanlı analiz ve güvenlik test aracıdır. Toplu web bağlantılarını (URL) analiz etmek, durum kodlarını kontrol etmek, içeriklerini tarayarak akıllı kategorilere ayırmak ve erişilebilirlik, hız, TLS/SSL geçerliliğine göre puanlamak gibi gelişmiş özellikleri yüksek performansla sunar. Gelişmiş *Stealth (Gizlilik)* modları, çoklu iş parçacığı (multi-threading) desteği ve yeni eklenen sistem dayanıklılık testi araçlarıyla (DDoS & SMS) eksiksiz bir deneyim sağlar.

![NexaVista](https://img.shields.io/badge/version-3.0-blue) ![Python](https://img.shields.io/badge/python-3.8+-green)

> [!WARNING]
> **Yasal Uyarı / Sorumluluk Reddi (Disclaimer)**
> Bu yazılım (özellikle SMS Bomber ve DDoS Saldırı modülleri), yalnızca **eğitim amaçlı** ve sistem sahiplerinin kendi altyapılarının (sunucular, ağlar veya uygulamalar) dayanıklılığını (stress test) test etmeleri amacıyla geliştirilmiştir. NexaVista'nın size ait olmayan veya test edilmesi için yetkilendirilmediğiniz sistemler, ağlar veya bireyler üzerinde kullanılması kesinlikle yasa dışıdır ve suç teşkil eder. Bu aracın kötüye kullanılmasından doğabilecek her türlü doğrudan veya dolaylı maddi, manevi, hukuki veya cezai sonuçlardan tamamen **kullanıcı sorumludur**. Geliştirici(ler) veya projeye katkıda bulunanlar hiçbir şekilde sorumluluk kabul etmez. Bu yazılımı kullanarak bu şartları kabul etmiş sayılırsınız.

---

## 🚀 Öne Çıkan Özellikler

*   **⚡ Yüksek Performanslı Tarama (Multi-Threading)**: Aynı anda 100'e kadar iş parçacığı (thread) ile binlerce bağlantıyı saniyeler içinde tarama yeteneği.
*   **🛠️ Aktif Güvenlik ve Stres Testi Araçları (YENİ)**:
    *   **DDoS Saldırı Modülü**: Kendi sunucularınızın veya ağ yapınızın yüksek trafik altındaki tepkisini, sınırlarını ve dayanıklılığını ölçmek için tasarlanmış stres testi modülü.
    *   **SMS Bomber Modülü**: API rate-limit açıklarını ve SMS gateway sistemlerinin yük altındaki stabilitesini test etmek için geliştirilmiş otomatize SMS gönderim aracı.
*   **🕵️ Gelişmiş Gizlilik (Stealth) Modları**: 
    *   Sürekli rotasyonlu User-Agent kullanımı.
    *   Analiz engellemelerini aşmak için rastgele gecikme (Delay) süreleri.
    *   HTTP, HTTPS ve SOCKS5 proxy desteği.
    *   TLS impersonation (İsteğe bağlı, gelişmiş izinsiz tarama güvenlik duvarlarını sorunsuz atlatma).
*   **🧠 Akıllı Sınıflandırma ve Skorlama**: Alan adlarını içeriklerine (meta tags, title, keywords) bakarak teknoloji, alışveriş, haber gibi akıllı kategorilere ayırır. Yanıt süresine (ms) ve SSL sertifikası durumuna göre her siteye dinamik bir puan (Score) atar.
*   **📄 Kapsamlı Raporlama ve Dışa Aktarma**: Tarama sonuçlarını, kolay okunabilirlik ve diğer araçlarla entegrasyon için `MD`, `TXT`, `HTML`, `XML`, `JSON` veya `CSV` formatlarında dışa aktarma seçeneği.
*   **🛡️ Dahili Proxy Test Cihazı**: Elinizdeki proxy listelerinin yaşayıp yaşamadığını, HTTP/SOCKS türlerini ve mevcut IP adreslerini test etmenize olanak tanıyan entegre araç.
*   **📂 Düzenli Çalışma Alanı (Workspace)**: Herhangi bir kargaşaya mahal vermeden loglanan her dosya, operasyon çıktısı ve tarama işlemi düzenli bir şekilde `outputs/` klasöründe tutulurken uygulamanın bulunduğu ana dizin tamamen temiz kalır.

---

## 📦 Kurulum ve Sistem Gereksinimleri

NexaVista'nın tam performanslı çalışabilmesi için **Python 3.8 veya üzeri** bir sürüm gereklidir. Gerekli kütüphaneleri yüklemek ve aracı kurmak için sırasıyla aşağıdaki komutları terminal veya komut satırınızda çalıştırın:

```bash
git clone https://github.com/KauelaKawela/nexavista.git
cd nexavista
pip install -r requirements.txt
python3 NexaVista.py
```

---

## 🕹️ Menü Yapısı ve Kullanım

`NexaVista.py` çalıştırıldığında, interaktif ve profesyonel tasarımlı terminal menüsü sizi karşılar. Yapacağınız işleme göre numaralandırılmış menüyü kullanabilirsiniz:

1.  **Standart Tarama**: Linklistenizi veya dosya bazlı URL deponuzu yükleyerek yüksek hızlı tarama, skorlama ve kategorizasyon işlemini başlatır. Gizlilik seviyesi ve thread kapasitesi ayarlanabilir.
2.  **SMS Bomber**: Hedef test ortamında API limitlerini zorlamak için konfigüre edilebilir SMS gönderim işlemini başlatır. (Yalnızca stress testi için.)
3.  **DDoS Saldırı**: Tanımlanmış hedef ağda veya IP'de yük oluşturarak tepkime ve çökme dirençlerini (load test) belirlemeye yarayan arayüz.
4.  **Proxyleri Kontrol Et**: Harici proxy listelerinizi testlere sokarak canlılık ve anonimlik durumlarını denetler.
5.  **Kategori Sayılarını Göster**: Aktif çalışma klasöründe (`outputs/`) daha önce sınıflandırılması yapılmış verilerin adet bazında raporunu ve istatistiğini gösterir.
6.  **Hakkında / Yardım**: Araç ve alt sistemler (modüller) hakkında genel bilgi ve kullanımı anlatan dokümantasyon sayfası.
0.  **Çıkış**: Aracı güvenli bir biçimde kapatır.

---

# 🌐 NexaVista v3.0 (English)

**NexaVista** is a comprehensive, terminal-based analysis and security testing framework tailored for cybersecurity researchers, network administrators, and developers. It provides advanced capabilities such as mass-analyzing web URLs, checking status codes, smartly categorizing content, and generating health scores based on reachability, response time, and TLS/SSL validity. With cutting-edge *Stealth* modes, multi-threading, and newly added system stress-testing tools (DDoS & SMS), it delivers a complete and secure workflow environment.

> [!WARNING]
> **Legal Disclaimer**
> This software (specifically the SMS Bomber and DDoS Attack modules) is developed strictly for **educational purposes** and for system owners to conduct **stress tests/load tests** on their own authorized infrastructure (servers, networks, or applications). Using NexaVista against systems, networks, or individuals that you do not own or do not have explicit permission to test is illegal and strictly prohibited. The user assumes full responsibility for any direct, indirect, material, moral, legal, or criminal consequences that may arise from the misuse of this framework. The developer(s) or contributors hold absolutely no liability. By using this tool, you agree to these terms.

## 🚀 Core Features

*   **⚡ Multi-Threaded Scanning Engine**: Scan thousands of URLs within seconds using robust multi-threading architecture (up to 100 concurrent threads).
*   **🛠️ Active Security & Stress Testing Tools (NEW)**:
    *   **DDoS Attack Module**: Integrated stress testing module crafted to benchmark the limits, response times, and resilience of your own infrastructure under high traffic volume.
    *   **SMS Bomber Module**: Automated SMS dispatching tool to measure API rate limits and stability of internal SMS gateways.
*   **🕵️ Advanced Stealth Strategies**: 
    *   Continuous User-Agent rotations.
    *   Randomized execution delays to evade aggressive rate-limits.
    *   HTTP, HTTPS, and SOCKS5 proxy integration.
    *   TLS impersonation capabilities to seamlessly bypass strict WAFs.
*   **🧠 Intelligent Categorization & Dynamic Scoring**: Inspects meta content (title, tags) to allocate domains into categories like 'Tech', 'News', or 'Shopping'. Computes an overall health score factoring in TLS/SSL certification logic and TTFB (Time to First Byte) latency.
*   **📄 Comprehensive Export Options**: Painlessly export scan outcomes directly into parsed `MD`, `TXT`, `HTML`, `XML`, `JSON` or `CSV` formatted reports for external integrations.
*   **🛡️ Built-in Proxy Verification**: Evaluate the functionality, protocol (HTTP/SOCKS), and exact outgoing IPs of your proxy lists right within the native interface.
*   **📂 Tidy Workspace Administration**: Output structures, logged transactions, and scanning residues are strictly orchestrated inside the `outputs/` directory, keeping your root repository flawless.

## 📦 System Requirements & Installation

- **Python 3.8 or newer** is required to fully utilize the framework's mechanics.
- Setup via terminal:

```bash
git clone https://github.com/KauelaKawela/nexavista.git
cd nexavista
pip install -r requirements.txt
python3 NexaVista.py
```
