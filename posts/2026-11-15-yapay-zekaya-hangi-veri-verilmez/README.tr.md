[🇬🇧 English](README.en.md) | 🇹🇷 **Türkçe**

# Yapay zekâ kullanırken hangi veri paylaşılmaz? Gizlilik, KVKK ve şirket kuralları

> *Zehra tarafından araştırıldı ve yazıldı. Yapay zekâ yardımıyla taslağı hazırlandı, ben gözden geçirdim.*

**Kısa cevap:** Bir yapay zekâ aracına yapıştırdığın ya da yüklediğin her şey, başka bir şirketin sunucusuna giden veridir. Bu yüzden şunlar **asla** doğrudan paylaşılmaz: **sırlar** (şifre, API anahtarı, token, connection string, sertifika), **kişisel veriler** (ad soyad ile birlikte TC kimlik no, telefon, e-posta, adres, sağlık ya da finans bilgisi), **müşteri ve üretim verisi** ve şirketin **gizli iş bilgisi** (yayınlanmamış ürün planları, sözleşmeler, güvenlik açıkları). Paylaşmadan önce sorulacak üç soru: Bu aracı şirketim onayladı mı? Bu veri bu araçta nasıl saklanıyor ve eğitimde kullanılıyor mu? Aynı soruyu veriyi maskeleyerek ya da sahte veriyle sorabilir miyim?

## 1. Neyi araştırdım ve neden

Yapay zekâ izinin bu yazısı takvimde sona yakındı, ama bence en baştan bilinmesi gereken bir konu. Her gün bir yapay zekâya kod, hata mesajı, log yapıştırıyorum. Bir hata ayıklarken stack trace'in içinde bir connection string ya da bir müşterinin e-postası olabileceğini çoğu zaman düşünmüyorum. 2023'te bir büyük teknoloji şirketinde çalışanların gizli kaynak kodunu ve toplantı notlarını bir sohbet botuna yapıştırdığı haberleri çıktı ve şirket bir süre bu araçları yasakladı. Yani bu teorik bir risk değil.

## 2. Üç ana çıkarım

1. **Yapıştırdığın şey şirketin dışına çıkar ve nerede durduğunu sen kontrol etmezsin.** Bir sohbet aracına veri gönderdiğimde, sağlayıcıya ve kullandığım plana göre şunlar olabilir:
   - Konuşma sağlayıcının sunucularında belirli bir süre **saklanır** (kötüye kullanım denetimi, yasal yükümlülükler için).
   - Bireysel ve ücretsiz planlarda, ayarlara bağlı olarak verinin **model eğitiminde kullanılması** mümkün. Kurumsal planlar ve API kullanımı genelde varsayılan olarak eğitimde kullanılmıyor, ama bu sağlayıcıdan sağlayıcıya ve zamanla değişiyor. Kendi aracımın güncel veri politikasını ve ayarlarını kontrol etmem gerekiyor; varsayım yapmamalıyım.
   - Sunucular büyük ihtimalle **yurt dışında**.
   - Paylaşılan sohbet bağlantıları, eklentiler, entegrasyonlar veriyi başka yerlere de taşıyabilir.

   Pratik sonuç: kurumsal hesabı olan, şirketin onayladığı araçla kişisel hesabımdaki ücretsiz araç aynı şey değil. Şirketin bir yapay zekâ kullanım politikası varsa, o politika benim için bağlayıcı.

2. **KVKK açısından: kişisel veriyi yapay zekâya göndermek bir "veri aktarımı".** 6698 sayılı Kişisel Verilerin Korunması Kanunu'na göre kişisel veri, kimliği belirli ya da belirlenebilir bir gerçek kişiye ilişkin her türlü bilgi. Müşteri tablosundan birkaç satırı "bu sorguyu düzelt" diye yapıştırmak, o kişilerin verisini üçüncü bir tarafa, büyük ihtimalle yurt dışına aktarmak demek. Yurt dışına aktarım kanunun 9. maddesine tabi; 2024'teki değişiklikle yeterlilik kararı ya da standart sözleşme gibi uygun güvenceler gibi belirli şartlara bağlandı. Bir geliştirici olarak bu şartların sağlanıp sağlanmadığına tek başıma karar veremem; bu, şirketin hukuk ve bilgi güvenliği ekiplerinin işi. Benim işim, şüpheli durumda **göndermemek** ve verinin sahte ya da maskelenmiş halini kullanmak.

   Özel nitelikli kişisel veriler (sağlık, din, biyometrik veri, ceza mahkûmiyeti gibi) için kurallar daha da sıkı. Avrupa'da benzer yükümlülükler GDPR ile geliyor.

3. **Kural: önce maskele, sahte veriyle sor, bağlamı küçült.** Çoğu soru gerçek veri olmadan da sorulabiliyor:
   - **Sırlar:** kodda zaten olmamalı (user secrets, ortam değişkenleri, Key Vault). Yapıştırmadan önce `Password=...` gibi değerleri `***` yap.
   - **Kişisel veri:** gerçek müşteri satırları yerine şemayı ve birkaç sahte satırı ver. "Ahmet Yılmaz, 12345678901" yerine "Kullanıcı A, 00000000000".
   - **Loglar ve stack trace'ler:** içinde e-posta, IP, token, istek gövdesi olabiliyor. Göndermeden önce oku.
   - **Kod:** şirketin kodunu paylaşmanın kuralı şirkete bağlı. Onaylı bir kurumsal araç yoksa, problemi küçük ve genel bir örneğe indirgemek (minimal reproducible example) hem daha güvenli hem de genelde daha iyi cevap getiriyor.
   - **Ekran görüntüleri:** metinden daha kolay unutuluyor. Görüntüdeki müşteri adı, tarayıcı sekmeleri, bildirimler de veri.
   - **Yanlışlıkla bir sır paylaştıysan:** sohbeti silmek yetmez, o anahtarı ya da şifreyi **hemen değiştir** (rotate).

## 3. Neyi yanlış anladım ya da hâlâ belirsiz

- "Sohbeti sildim, veri gitti" sanıyordum. Silmenin sağlayıcı tarafında ne anlama geldiği (ne kadar süre saklandığı, yedekler) politikaya bağlı. Bir sırrın sızdığını varsaymak ve değiştirmek daha güvenli.
- Kodun kendisinin "gizli" olup olmadığı şirketten şirkete değişiyor. Bazı şirketler kurumsal yapay zekâ araçlarına bütün kod tabanını açıyor, bazıları tamamen yasaklıyor. Kural koyan ben değilim, kurala uyan benim.
- Yerelde çalışan modeller (veri bilgisayardan çıkmaz) bu sorunun bir kısmını çözüyor gibi görünüyor, ama kalite ve donanım bedeli var. Bunu "Yerelde model çalıştırmak" yazısında açacağım.
- Bu yazı hukuki tavsiye değil; KVKK'nın ayrıntıları için şirketin hukuk ekibi ve Kişisel Verileri Koruma Kurumu'nun rehberleri asıl kaynak.

## 4. Örnek

[`example/`](example/) klasöründe yapay zekâya bir şey yapıştırmadan önce kullanılabilecek küçük bir **maskeleme scripti** var (Python, standart kütüphane). Bir metni alıp şunları maskeliyor: e-posta adresleri, geçerli TC kimlik numaraları (sağlama algoritmasıyla kontrol ederek, rastgele 11 haneli sayıları değil), TR IBAN'lar, telefon numaraları, `Password=` ve `ApiKey` gibi değerler, `Bearer` token'lar ve AWS tarzı erişim anahtarları. Mükemmel değil (bir regex listesi asla mükemmel olmaz), ama "yapıştırmadan önce bir kez durup bak" alışkanlığını otomatikleştiriyor.

**Yapay zekâ notu:** İronik ama bu konuda da yapay zekâya soru sorarken dikkatli olmak gerekiyor: "Bu log'da hassas veri var mı?" diye sormak için log'u ona yapıştırmam gerekir. Önce kendi gözümle ve maskeleme scriptiyle bakıyorum. Bir de yapay zekâ kod yazarken sırları koda gömebiliyor (örneğin örnek bir connection string'i `appsettings.json`'a gerçek şifreyle koymak). Ürettiği kodda sırların ortam değişkeninden ya da secret store'dan okunduğunu kontrol ediyorum.

## 5. Kaynakça

_Bu yazıda yararlandığım kaynaklar. Bağlantılara son erişim: 18 Kasım 2026._

- 6698 sayılı Kişisel Verilerin Korunması Kanunu ve 2024 değişiklikleri (7499 sayılı Kanun). https://www.mevzuat.gov.tr/
- Kişisel Verileri Koruma Kurumu, rehberler ve yurt dışına aktarım duyuruları. https://www.kvkk.gov.tr/
- OWASP, "Top 10 for Large Language Model Applications" (hassas bilgi ifşası). https://genai.owasp.org/
- OWASP, "Secrets Management Cheat Sheet". https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html
- Microsoft Learn, "Safe storage of app secrets in development in ASP.NET Core". https://learn.microsoft.com/aspnet/core/security/app-secrets
- Kullandığın yapay zekâ sağlayıcısının güncel gizlilik ve veri kullanım politikası (tarih notu: bu yazı Kasım 2026'da yazıldı, politikalar değişebilir).

---

© 2026 Zehra Betül Çuhadar. Bu yazının metni ve görselleri [CC BY-NC-ND 4.0](https://creativecommons.org/licenses/by-nc-nd/4.0/deed.tr) lisanslıdır: adımı ve bağlantıyı vererek, ticari olmayan amaçla ve değiştirmeden paylaşabilirsin. Kod örnekleri için tüm hakları saklıdır, bkz. [LICENSE-CODE](../../LICENSE-CODE).
