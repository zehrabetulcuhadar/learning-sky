[🇬🇧 English](README.en.md) | 🇹🇷 **Türkçe**

# JSON, YAML ve XML nedir? Hangisi ne zaman kullanılır?

> *Zehra tarafından araştırıldı ve yazıldı. Yapay zekâ yardımıyla taslağı hazırlandı, ben gözden geçirdim.*

**Kısa cevap:** JSON, YAML ve XML, yapılandırılmış veriyi (nesneler, listeler, sayılar, metinler) **düz metin** olarak yazmanın üç farklı yoludur. Böylece bir program veriyi dosyaya kaydedebilir ya da ağ üzerinden başka bir programa gönderebilir; buna **serileştirme** (serialization) denir. Kabaca: **JSON** API'lerde ve programlar arası veri alışverişinde, **YAML** insanların elle yazdığı yapılandırma dosyalarında (GitHub Actions, Docker Compose, Kubernetes), **XML** ise şema doğrulaması, ad alanları ve belge yapısı gereken yerlerde (eski kurumsal servisler, SOAP, Office dosyaları, `.csproj`) öne çıkar.

## 1. Neyi araştırdım ve neden

Learning Sky'da üç formatı da her gün kullanıyorum ve hiç durup düşünmemiştim: her yazının `meta.json` dosyası var, GitHub Action'ı `sky.yml` dosyasında, `.NET` projelerimin `.csproj` dosyası XML. İşte de Angular'ın `angular.json`'u, .NET'in `appsettings.json`'u var. Basics gezegeninde "bilgisayar veriyi nasıl saklar" sorusunun bir sonraki adımı bu: veri bellekte nesne, diskte ya da ağda metin. Arada bir format var.

## 2. Üç ana çıkarım

1. **Aynı veri, üç farklı yazım.** Bir yazının bilgisi üç formatta şöyle görünüyor:

   ```json
   { "title": "Veritabanı nedir?", "topic": "data", "tags": ["sql", "basics"], "draft": true }
   ```

   ```yaml
   title: Veritabanı nedir?
   topic: data
   tags: [sql, basics]
   draft: true
   ```

   ```xml
   <post draft="true">
     <title>Veritabanı nedir?</title>
     <topic>data</topic>
     <tags><tag>sql</tag><tag>basics</tag></tags>
   </post>
   ```

   - **JSON** (JavaScript Object Notation): altı tip var: nesne, dizi, metin, sayı, `true/false`, `null`. Yorum satırı yok, sondaki virgüle izin yok, anahtarlar çift tırnaklı. Sade ve katı olduğu için her dilde hızlı ve aynı şekilde ayrıştırılıyor. Bugün REST API'lerin ortak dili.
   - **YAML** ("YAML Ain't Markup Language"): girintiyle yapı kuruyor, yorum (`#`) destekliyor, tırnak çoğu zaman gerekmiyor. İnsanın okuması ve yazması için tasarlanmış. YAML 1.2 aslında JSON'un bir üst kümesi: geçerli her JSON, geçerli bir YAML.
   - **XML** (eXtensible Markup Language): etiketler ve öznitelikler. Daha uzun, ama **şema** (XSD) ile verinin yapısını resmi olarak tanımlayıp doğrulayabiliyor, ad alanları (namespace) ile farklı sözlükleri karıştırabiliyor. Karışık içerik de taşıyabiliyor (metnin içinde etiket, HTML'e benzer şekilde).

2. **Her formatın kendine has tuzakları var.**
   - **YAML'ın sihri bazen kötü sürpriz.** YAML 1.1 kurallarında `no`, `yes`, `on`, `off` gibi kelimeler boolean'a dönüşüyordu. Ünlü "Norveç problemi": ülke kodları listesinde `NO` yazınca Norveç `false` oluyordu. `version: 1.10` yazınca sayı `1.1` olabiliyor, `22:22` gibi değerler bazı ayrıştırıcılarda altmışlık sayıya dönüşebiliyor. Bir de girinti: bir boşluk kayınca yapı tamamen değişiyor. Kural: emin olmadığın metni tırnağa al (`version: "1.10"`).
   - **JSON'ın sınırları:** yorum yok (bu yüzden `tsconfig.json` gibi dosyalar aslında yorumlara izin veren "JSONC" kullanıyor), tarih tipi yok (tarihler metin olarak, genelde ISO 8601: `"2026-12-12"`), ve büyük sayılarda dikkat: JavaScript tüm sayıları `double` tuttuğu için 2^53'ten büyük tam sayılar (örneğin bazı ID'ler) hassasiyet kaybediyor. Bu yüzden bazı API'ler büyük ID'leri metin olarak gönderiyor.
   - **XML'in güvenlik tarafı:** XML ayrıştırıcıları dış varlıkları (external entity) yüklemeye izin verirse **XXE** saldırısı mümkün oluyor; saldırgan sunucudaki bir dosyayı okutabiliyor. Modern .NET'te varsayılanlar güvenli, ama eski kodda dikkat etmek gerekiyor.

3. **Seçim, kimin okuyup yazdığına bağlı.** Burada da bir trade-off var:

   | | JSON | YAML | XML |
   |---|---|---|---|
   | Kim yazar? | Çoğunlukla program | Çoğunlukla insan | İkisi de |
   | Yorum | Yok | Var | Var |
   | Okunabilirlik | İyi | Çok iyi | Orta (uzun) |
   | Ayrıştırma güvenilirliği | Çok yüksek, katı | Sürprizli, gevşek | Yüksek, şemayla doğrulanır |
   | Tipik yer | API, `package.json`, `appsettings.json` | CI/CD, Docker Compose, Kubernetes | SOAP, `.csproj`, SVG, RSS, Office |

   Kendi projemde de bu mantık doğal olarak oluşmuş: `meta.json` hem benim yazdığım hem programın okuduğu bir dosya, katı olması iyi. `sky.yml`'yi sadece ben yazıyorum ve yorum eklemek istiyorum. `sky.json` tamamen program üretiyor ve site okuyor. SVG gezegenlerim de aslında XML.

## 3. Neyi yanlış anladım ya da hâlâ belirsiz

- XML'i "eski ve ölü" sanıyordum. Değil: `.csproj`, SVG, RSS, `.docx` (içi XML dosyalarıyla dolu bir zip) her yerde. Sadece yeni API'lerde JSON'a yerini bıraktı.
- JSON'ı JavaScript'e özel sandım, aslında dilden bağımsız bir standart (RFC 8259). C#'ta `System.Text.Json`, Python'da `json` modülü aynı formatı okuyor.
- Protobuf, MessagePack gibi ikili (binary) formatlar da var, gRPC bunları kullanıyor. İnsan okuyamıyor ama çok daha küçük ve hızlı. Bunu ileride API yazılarında açacağım.

## 4. Örnek

[`example/`](example/) klasöründe aynı yazı bilgisi üç formatta duruyor ve küçük bir Python scripti JSON ile XML'i standart kütüphaneyle okuyup aynı nesneye çeviriyor. Script bir de JavaScript'in büyük sayı sorununu ve `NO` kelimesinin YAML 1.1'de neden tehlikeli olduğunu bir notla gösteriyor.

**Yapay zekâ notu:** Yapay zekâya bir GitHub Actions ya da Docker Compose YAML'ı yazdırdığımda girintiyi ve anahtar adlarını mutlaka kontrol ediyorum: eski sürümden kalma anahtarlar ya da var olmayan seçenekler uydurabiliyor. YAML'ı bir doğrulayıcıdan geçirmek (`actionlint`, editördeki şema desteği) bu hataları hemen yakalıyor. JSON üretmesini istediğimde ise "sadece geçerli JSON, açıklama yok" demem gerekiyor; yoksa başına "İşte JSON'unuz:" gibi metin ekleyip ayrıştırmayı bozabiliyor.

## 5. Kaynakça

_Bu yazıda yararlandığım kaynaklar. Bağlantılara son erişim: 18 Kasım 2026._

- RFC 8259, The JavaScript Object Notation (JSON) Data Interchange Format. https://www.rfc-editor.org/rfc/rfc8259
- YAML 1.2.2 Specification. https://yaml.org/spec/1.2.2/
- W3C, Extensible Markup Language (XML) 1.0. https://www.w3.org/TR/xml/
- "The Norway Problem" (YAML 1.1 boolean sorunu üzerine yaygın yazılar), örneğin https://hitchdev.com/strictyaml/why/implicit-typing-removed/
- OWASP, "XML External Entity Prevention Cheat Sheet". https://cheatsheetseries.owasp.org/cheatsheets/XML_External_Entity_Prevention_Cheat_Sheet.html

---

© 2026 Zehra Betül Çuhadar. Bu yazının metni ve görselleri [CC BY-NC-ND 4.0](https://creativecommons.org/licenses/by-nc-nd/4.0/deed.tr) lisanslıdır: adımı ve bağlantıyı vererek, ticari olmayan amaçla ve değiştirmeden paylaşabilirsin. Kod örnekleri için tüm hakları saklıdır, bkz. [LICENSE-CODE](../../LICENSE-CODE).
