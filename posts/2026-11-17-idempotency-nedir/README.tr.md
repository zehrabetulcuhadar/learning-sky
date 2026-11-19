[🇬🇧 English](README.en.md) | 🇹🇷 **Türkçe**

# Idempotency nedir? Aynı istek iki kez gelirse ne olur?

> *Zehra tarafından araştırıldı ve yazıldı. Yapay zekâ yardımıyla taslağı hazırlandı, ben gözden geçirdim.*

**Kısa cevap:** Bir işlem, **bir kez de yapılsa birçok kez de yapılsa sistemde aynı sonucu bırakıyorsa** idempotent'tir. Asansör düğmesi idempotent'tir: beş kez basmak asansörü beş kez çağırmaz. "Hesaptan 100 TL çek" idempotent değildir: iki kez çalışırsa 200 TL çekilir. Bu önemli, çünkü ağ güvenilmezdir: istemci cevap alamadığında isteğin sunucuya ulaşıp ulaşmadığını bilemez ve tekrar dener. HTTP'de `GET`, `PUT` ve `DELETE` tanım gereği idempotent'tir, `POST` değildir. `POST` gibi işlemleri güvenle tekrar denenebilir yapmanın yaygın yolu bir **idempotency anahtarı**dır: istemci her işlem için benzersiz bir anahtar gönderir, sunucu aynı anahtarı ikinci kez görünce işlemi tekrar yapmaz, ilk cevabı döner.

## 1. Neyi araştırdım ve neden

"Kullanıcı ödeme butonuna iki kez bastı, iki sipariş oluştu" türünden hataları hepimiz duymuşuzdur. İlk tepki genelde butonu tıklandıktan sonra pasif yapmak. Ama bu sadece bir kısmını çözüyor: kullanıcı butona bir kez bassa bile tarayıcı, mobil ağ, bir proxy ya da bizim kendi `retry` mantığımız isteği tekrarlayabilir. Backend gezegeninin ikinci ek yazısında, bunun asıl çözümünün sunucu tarafında olduğunu öğrendim.

## 2. Üç ana çıkarım

1. **Ağ "en az bir kez" teslim eder, "tam bir kez" değil.** Bir istemci istek gönderip cevap alamadığında üç ihtimal var:
   - İstek sunucuya hiç ulaşmadı.
   - İstek ulaştı, işlendi, ama cevap yolda kayboldu.
   - İstek hâlâ işleniyor, sadece yavaş.

   İstemci bunları birbirinden ayıramaz. Tek güvenli seçeneği tekrar denemek. Ama ikinci ihtimalde tekrar denemek, işlemi **iki kez** yapmak demek. Dağıtık sistemlerde "tam olarak bir kez" (exactly-once) teslimat pratikte garanti edilemiyor; yapılabilen şey, "en az bir kez" teslimatı **idempotent işleme** ile birleştirip **etkinin** bir kez olmasını sağlamak. Bu fikir sadece HTTP'de değil, mesaj kuyruklarında da (RabbitMQ, Kafka tüketicileri) karşıma çıktı: aynı mesaj iki kez gelebilir, tüketici buna hazır olmalı.

2. **HTTP metotlarının bir sözleşmesi var.** HTTP standardı (RFC 9110) metotları iki özellikle tanımlıyor:
   - **Güvenli (safe):** sunucuda bir şey değiştirmez. `GET`, `HEAD`, `OPTIONS`.
   - **Idempotent:** birden çok kez yapılması bir kez yapılmasıyla aynı etkiyi bırakır. Güvenli olanların hepsi, artı `PUT` ve `DELETE`.
   - `POST` ve `PATCH` idempotent değil (genel tanımla; belirli bir `PATCH` idempotent tasarlanabilir).

   Örnekler:
   - `PUT /users/42 { "name": "Zehra" }` → kaç kez gönderilirse gönderilsin, kullanıcı 42'nin adı "Zehra" olur. Idempotent.
   - `DELETE /posts/7` → ilk seferde siler, sonrakilerde zaten yok. Cevap kodu değişebilir (200, sonra 404), ama **sistemdeki etki** aynı. Idempotent, çünkü tanım cevaba değil etkiye bakıyor.
   - `POST /orders` → her çağrıda yeni bir sipariş oluşturur. Idempotent değil.
   - `PATCH /accounts/1 { "balance": "+100" }` → her çağrıda 100 ekler. Idempotent değil. Ama `{ "balance": 500 }` gibi mutlak bir değer idempotent olurdu.

   Bu sözleşme pratikte önemli: tarayıcılar, proxy'ler ve HTTP kütüphaneleri idempotent metotları kendiliğinden tekrar deneyebiliyor. Bir `GET` endpoint'i sunucuda veri değiştiriyorsa (örneğin `GET /delete-user?id=5`), bu sözleşmeyi bozuyor ve sürprizlere açık.

3. **POST'u güvenli hale getirmek: idempotency anahtarı.** Stripe gibi ödeme API'lerinin kullandığı ve IETF'de standartlaşma sürecinde olan yöntem:
   1. İstemci, kullanıcı "Öde"ye bastığında bir kez benzersiz bir anahtar üretir (genelde bir UUID).
   2. İsteği bu anahtarla gönderir: `Idempotency-Key: 8e03978e-40d5-43e8-bc93-6894a57f9324`.
   3. Sunucu anahtarı ilk kez görüyorsa işlemi yapar ve **anahtarı cevapla birlikte saklar**.
   4. Aynı anahtarla tekrar istek gelirse işlemi tekrar yapmaz, saklanan cevabı döner.
   5. Aynı anahtar farklı bir istek gövdesiyle gelirse hata döner (anahtar yanlışlıkla tekrar kullanılmış).

   Dikkat edilecekler: anahtar her **tekrar denemede aynı**, her **yeni işlemde farklı** olmalı (bu yüzden istemcide, işlem başladığında üretilir, her istekte değil). İki aynı istek tam aynı anda gelirse bir yarış durumu olabilir; anahtarı veritabanında benzersiz (unique) bir kısıtla saklamak bunu çözüyor. Anahtarlar sonsuza kadar saklanmaz, belirli bir süre sonra (örneğin 24 saat) silinir.

   Daha basit durumlarda **doğal anahtar** da iş görüyor: sipariş numarasını istemci üretip benzersiz kısıt koymak, ya da "varsa güncelle, yoksa ekle" (upsert) kullanmak.

## 3. Neyi yanlış anladım ya da hâlâ belirsiz

- Idempotent'i "her seferinde aynı cevabı döner" sanıyordum. Değil: `DELETE` örneğindeki gibi cevap değişebilir; önemli olan sistemdeki etki. Bir `GET` de her seferinde farklı veri dönebilir (veri değişmişse) ve yine idempotent'tir.
- Butonu pasif yapmanın yeterli olduğunu düşünüyordum. Kullanıcı deneyimi için iyi bir önlem, ama tek başına garanti değil; asıl güvence sunucu tarafında.
- İşlemin yarısında çöken bir sunucuda anahtarın durumunu ("işleniyor" mu, "bitti" mi) nasıl yöneteceğim sorusu karmaşık görünüyor. Transaction ve outbox deseni gibi konularda buna döneceğim.

## 4. Örnek

[`example/`](example/) klasöründe paketsiz bir Node.js örneği var. Küçük bir "ödeme" sunucusu ve ağ hatasını taklit eden bir istemci: ilk isteğin cevabı "kayboluyor", istemci tekrar deniyor.
- **Anahtarsız** endpoint'te müşteriden iki kez para çekiliyor.
- **Idempotency anahtarlı** endpoint'te ikinci istek aynı cevabı alıyor, para bir kez çekiliyor.
- Aynı anahtarın farklı bir tutarla tekrar kullanılması `422` ile reddediliyor.

.NET tarafında aynı mantık bir middleware ya da action filter ile kurulabiliyor: anahtarı header'dan okuyup bir tabloda (benzersiz kısıtla) saklamak.

**Yapay zekâ notu:** Yapay zekâya "bu endpoint'e retry ekle" dediğimde, endpoint'in idempotent olup olmadığını sormadan `Polly` ya da RxJS `retry` ekleyebiliyor. `GET` için sorun yok, ama bir `POST /payments`'a körü körüne retry eklemek çift ödeme demek. Bu yüzden önce soruyorum: "Bu işlem iki kez çalışırsa ne olur?" Cevap "kötü bir şey" ise, önce idempotency, sonra retry. Ürettiği idempotency kodunda da şuna bakıyorum: anahtar her denemede aynı mı kalıyor, yoksa yanlışlıkla her istekte yeniden mi üretiliyor?

## 5. Kaynakça

_Bu yazıda yararlandığım kaynaklar. Bağlantılara son erişim: 18 Kasım 2026._

- RFC 9110, HTTP Semantics, Bölüm 9.2: Common Method Properties (safe ve idempotent metotlar). https://www.rfc-editor.org/rfc/rfc9110#section-9.2
- IETF HTTPAPI, "The Idempotency-Key HTTP Header Field" (taslak). https://datatracker.ietf.org/doc/draft-ietf-httpapi-idempotency-key-header/
- Stripe API Reference, "Idempotent requests". https://docs.stripe.com/api/idempotent_requests
- Brandur Leach. "Implementing Stripe-like Idempotency Keys in Postgres". https://brandur.org/idempotency-keys
- Martin Kleppmann. *Designing Data-Intensive Applications*, O'Reilly, Bölüm 11 (exactly-once ve idempotence).

---

© 2026 Zehra Betül Çuhadar. Bu yazının metni ve görselleri [CC BY-NC-ND 4.0](https://creativecommons.org/licenses/by-nc-nd/4.0/deed.tr) lisanslıdır: adımı ve bağlantıyı vererek, ticari olmayan amaçla ve değiştirmeden paylaşabilirsin. Kod örnekleri için tüm hakları saklıdır, bkz. [LICENSE-CODE](../../LICENSE-CODE).
