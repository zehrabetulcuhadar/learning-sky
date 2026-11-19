[🇬🇧 English](README.en.md) | 🇹🇷 **Türkçe**

# Büyük kesintilerden ne öğrendik? CrowdStrike, AWS ve Cloudflare

> *Zehra tarafından araştırıldı ve yazıldı. Yapay zekâ yardımıyla taslağı hazırlandı, ben gözden geçirdim.*

**Kısa cevap:** Son yılların internetin büyük bir kısmını etkileyen kesintilerinin çoğu bir saldırıdan değil, **şirketin kendi yaptığı bir değişiklikten** çıktı: hatalı bir içerik güncellemesi (CrowdStrike, Temmuz 2024), otomatik bir DNS sisteminde yarış durumu (AWS, Ekim 2025), boyutu beklenenden büyük bir yapılandırma dosyası (Cloudflare, Kasım 2025). Üçünün ortak dersleri: **değişiklikleri kademeli yay**, **kendi ürettiğin veriyi bile doğrula**, **bir hatanın etki alanını (blast radius) küçük tut** ve **paylaşılan bağımlılıklarını bil.**

## 1. Neyi araştırdım ve neden

Kasım 2026'da bir haftada Apple servisleri, ABD hava trafiği ve birkaç büyük banka çöktü; resmî açıklamaların ortak noktası "saldırı değil, iç güncelleme" oldu (ayrıntılar aylık haber yazımda). Sabah bültenimde bu haberleri okurken bir şeyi fark ettim: büyük kesintiler artık neredeyse rutin, ve en öğretici kaynakları şirketlerin olaydan sonra yayımladığı **postmortem** raporları. Bu yazıda son yılların üç büyük olayının resmî raporlarını okudum ve kendi işime (Angular, .NET) çıkan dersleri topladım.

## 2. Üç ana çıkarım

1. **CrowdStrike (19 Temmuz 2024): bir içerik güncellemesi, milyonlarca mavi ekran.** CrowdStrike'ın Falcon güvenlik yazılımı, Windows'ta çekirdek (kernel) seviyesinde çalışan bir sürücüye sahip. Şirket, yeni tehditleri tanımak için sürücüye "içerik" dosyaları (Channel File 291) gönderdi. Rapora göre yeni şablon türü 21 girdi alanı tanımlıyordu ama sürücünün bu dosyayı işleyen kodu yalnızca 20 değer sağlıyordu; 21. alana erişilmeye çalışılınca sınır dışı bellek okuması oldu. Kod çekirdekte çalıştığı için bu bir uygulama hatası değil, işletim sistemi çökmesiydi. Microsoft'un tahminine göre yaklaşık 8,5 milyon Windows cihazı etkilendi; havayolları, hastaneler, bankalar durdu. Bilgisayarlar açılırken çöktüğü için düzeltme çoğu yerde elle, tek tek yapıldı.
   - **Ders:** "içerik" ya da "yapılandırma" da koddur, onunla aynı titizlikle test edilmeli. Güncellemeler herkese aynı anda değil, önce küçük bir gruba gönderilmeli (kademeli yayın, canary). CrowdStrike raporunda da içerik güncellemeleri için kademeli dağıtım ve ek sınır kontrolleri sözü verildi.

2. **AWS us-east-1 (20 Ekim 2025): DNS kaydı boşaldı, yarım internet durdu.** AWS'nin raporuna göre DynamoDB'nin DNS kayıtlarını otomatik yöneten sistemde nadir bir **yarış durumu** (race condition) oldu: iki otomasyon bileşeninin zamanlaması üst üste binince `dynamodb.us-east-1.amazonaws.com` adresinin DNS kaydı boş kaldı. DynamoDB'ye ulaşılamayınca ona bağımlı AWS'nin kendi servisleri de (EC2'nin yeni sunucu başlatan sistemleri, ağ yük dengeleyicileri) zincirleme etkilendi. Etki saatlerce sürdü ve dünya genelinde birçok uygulama, oyun ve mesajlaşma servisi aksadı.
   - **Ders:** tek bir bölge (region) ve tek bir temel servis, fark edilmeden **tek hata noktası** olabiliyor. "Bulut asla çökmez" diye bir şey yok. Kendi sistemimde hangi servise doğrudan ya da dolaylı bağımlı olduğumu bilmem, ona ulaşılamazsa uygulamamın nasıl davranacağını düşünmem gerekiyor. Bir de yarış durumu konusu: eşzamanlılık derslerinde öğrendiğim "iki iş aynı anda çalışırsa" problemi, dünyanın en büyük bulutunu da durdurabiliyor.

3. **Cloudflare (18 Kasım 2025): iki katına çıkan bir dosya.** Cloudflare'in raporuna göre bir veritabanı (ClickHouse) izin değişikliği, bot yönetimi sisteminin "özellik dosyasını" üreten sorgunun yinelenen satırlar döndürmesine yol açtı. Dosya normalin yaklaşık iki katına çıktı ve trafiği işleyen yazılımın bu dosya için koyduğu sınırı (200 özellik) aştı. Yazılım bu durumu düzgün ele almak yerine hata verip durdu (raporda Rust kodundaki bir `unwrap()` çağrısı gösteriliyor). Dosya birkaç dakikada bir yeniden üretildiği için sistem bir düzelip bir bozuldu, bu yüzden ekip başta bir saldırıdan şüphelendi. Birkaç saat boyunca X, ChatGPT ve birçok büyük site hata verdi.
   - **Ders:** kendi sistemimizin ürettiği veriye de bir dış girdi gibi davranmak gerekiyor; "bu dosyayı biz üretiyoruz, hep doğrudur" varsayımı tehlikeli. Beklenmeyen bir girdide bütün süreci düşürmek yerine son iyi yapılandırmayla devam etmek (fail-safe) daha güvenli. Ve bir yapılandırma bütün dünyaya saniyeler içinde yayılıyorsa, hatası da saniyeler içinde yayılıyor.

## 3. Neyi yanlış anladım ya da hâlâ belirsiz

- Büyük kesintilerin çoğunu siber saldırı sanıyordum. Okuduğum raporların neredeyse hepsinde sebep bir iç değişiklik: güncelleme, yapılandırma, izin değişikliği.
- "Kademeli yayın" fikri basit görünüyor ama bir güvenlik ürünü için ikilemi var: yeni bir tehdide karşı korumayı yavaş yaymak da risk. Bu dengenin nasıl kurulduğunu henüz tam anlamış değilim.
- Raporlarda geçen bazı iç sistemleri (AWS'nin DNS otomasyon bileşenleri gibi) sadece raporların anlattığı kadar biliyorum. Ayrıntıların doğruluğu için asıl kaynak raporların kendisi.

## 4. Örnek

[`example/`](example/) klasöründe Cloudflare olayının küçük bir benzetimi var (Node.js, paket yok). Bir servis, birkaç saniyede bir yenilenen bir yapılandırma dosyasını okuyor. Dosya bir gün sınırı aşacak kadar büyüyor. Scriptin iki versiyonu var:
1. **Kırılgan:** sınır aşılınca hata fırlatıp duruyor.
2. **Dayanıklı:** yeni dosyayı doğruluyor, geçersizse uyarı yazıp **son iyi yapılandırmayla** devam ediyor.

Bu, kendi kodumda da uygulayabileceğim bir desen: .NET'te `IOptionsMonitor` ile yeniden yüklenen bir ayar ya da Angular'da uzaktan çekilen bir özellik bayrağı (feature flag) dosyası, bozuk geldiğinde uygulamayı çökertmemeli.

**Yapay zekâ notu:** Postmortem raporları uzun ve teknik. Yapay zekâya raporun tamamını verip "kök nedeni, zaman çizelgesini ve alınan önlemleri ayrı ayrı çıkar, sonra bir .NET geliştiricisi için üç ders yaz" demek çok işe yarıyor. Ama rakamları (etkilenen cihaz sayısı, süreler) mutlaka rapordan kendim doğruluyorum; yapay zekâ bu tür sayıları karıştırabiliyor ya da başka bir olayla birleştirebiliyor.

## 5. Kaynakça

_Bu yazıda yararlandığım kaynaklar. Bağlantılara son erişim: 18 Kasım 2026._

- CrowdStrike. "Channel File 291 Incident: Root Cause Analysis" (Ağustos 2024). https://www.crowdstrike.com/
- Microsoft. "Helping our customers through the CrowdStrike outage" (Temmuz 2024). https://blogs.microsoft.com/blog/2024/07/20/helping-our-customers-through-the-crowdstrike-outage/
- AWS. "Summary of the Amazon DynamoDB Service Disruption in the Northern Virginia (US-EAST-1) Region" (Ekim 2025). https://aws.amazon.com/message/101925/
- Cloudflare. "Cloudflare outage on November 18, 2025" (Kasım 2025). https://blog.cloudflare.com/18-november-2025-outage/
- Google SRE Book, "Postmortem Culture: Learning from Failure". https://sre.google/sre-book/postmortem-culture/

---

© 2026 Zehra Betül Çuhadar. Bu yazının metni ve görselleri [CC BY-NC-ND 4.0](https://creativecommons.org/licenses/by-nc-nd/4.0/deed.tr) lisanslıdır: adımı ve bağlantıyı vererek, ticari olmayan amaçla ve değiştirmeden paylaşabilirsin. Kod örnekleri için tüm hakları saklıdır, bkz. [LICENSE-CODE](../../LICENSE-CODE).
