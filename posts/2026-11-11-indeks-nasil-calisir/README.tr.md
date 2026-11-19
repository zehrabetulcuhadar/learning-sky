[🇬🇧 English](README.en.md) | 🇹🇷 **Türkçe**

# Veritabanı indeksi nasıl çalışır? Ne zaman zarar verir?

> *Zehra tarafından araştırıldı ve yazıldı. Yapay zekâ yardımıyla taslağı hazırlandı, ben gözden geçirdim.*

**Kısa cevap:** İndeks, bir tablodaki bir ya da birkaç sütunun **sıralı bir kopyasıdır** ve her değerin yanında o satırın nerede olduğu yazar. Çoğu ilişkisel veritabanında bu kopya bir **B-ağacı** (B-tree) olarak tutulur. İndeks yoksa veritabanı aradığını bulmak için bütün tabloyu okur (*full table scan*); indeks varsa milyonlarca satır arasında bile birkaç adımda doğru yere iner. Bedeli: her `INSERT`, `UPDATE` ve `DELETE` indeksi de güncellemek zorunda kalır ve indeks diskte yer kaplar. Bu yüzden indeks "ne kadar çok o kadar iyi" değildir.

## 1. Neyi araştırdım ve neden

"Sorgu yavaş, indeks ekleyelim" cümlesini çok duydum. Ama indeksin içinde ne olduğunu, neden hızlandırdığını ve neden bazen hiç kullanılmadığını bilmiyordum. Bir de EF Core ile çalışırken üretilen SQL'i nadiren görüyorum. Yavaş bir sorgunun nedenini anlamak için indeksin mantığını bilmem gerekiyor.

## 2. Üç ana çıkarım

1. **İndeks, kitabın sonundaki dizin gibi.** 600 sayfalık bir kitapta "deadlock" kelimesini arıyorum. İki yol var: kitabı baştan sona okumak (tam tarama) ya da sondaki alfabetik dizine bakıp "s. 412" bilgisiyle doğrudan sayfaya gitmek (indeks). Dizin alfabetik sıralı olduğu için onu da baştan okumam gerekmez, "d" harfine atlarım.

   Veritabanı bu "atlamayı" **B-ağacı** ile yapıyor. B-ağacı, her düğümünde çok sayıda sıralı anahtar tutan, dengeli ve sığ bir ağaç. Bir düğüm tek bir disk sayfasına (genelde 8 KB) sığıyor ve içinde yüzlerce anahtar olabiliyor. Bu yüzden ağaç çok sığ kalıyor: kabaca, milyonlarca satırlık bir tabloda bile 3 ila 4 seviye. Aramak = kökten yaprağa 3-4 sayfa okumak. Tam tarama ise binlerce sayfa okumak demek. Fark buradan geliyor: O(n) yerine O(log n).

   Yapraklar da sıralı ve birbirine bağlı olduğu için B-ağacı sadece eşitlikte değil, **aralıkta** (`WHERE date BETWEEN ...`), **sıralamada** (`ORDER BY`) ve **ön ekte** (`LIKE 'abc%'`) da işe yarıyor.

2. **İndeks var diye kullanılacağı garanti değil.** Öğrendiğim en şaşırtıcı kısım bu. İndeksin işe yaramadığı tipik durumlar:
   - **Sütunu fonksiyona sokmak:** `WHERE YEAR(created_at) = 2026` ya da `WHERE LOWER(email) = ...`. İndeks `created_at`'in kendisine göre sıralı, `YEAR(created_at)`'e göre değil. Çözüm: `WHERE created_at >= '2026-01-01' AND created_at < '2027-01-01'`.
   - **Baştaki joker karakter:** `LIKE '%sky'`. Dizinde "sonu sky ile bitenleri" bulamazsın.
   - **Bileşik indekste sıra:** `(planet_id, date)` indeksi `WHERE planet_id = ...` için ve ikisi birlikte için çalışır, ama sadece `WHERE date = ...` için genelde çalışmaz. Telefon rehberi soyada göre sıralıysa sadece adla arama yapamazsın. Buna **en soldaki ön ek kuralı** deniyor.
   - **Seçiciliği düşük sütun:** `WHERE is_active = 1` ve satırların yüzde 95'i aktifse, planlayıcı indeksle tek tek atlamak yerine tabloyu taramayı daha ucuz bulabilir.
   - **Örtük tip dönüşümü:** sütun `varchar` iken parametreyi `nvarchar` göndermek gibi durumlarda (SQL Server'da klasik bir tuzak) indeks kullanılamayabiliyor.

3. **Her indeks yazmayı yavaşlatır, o yüzden indeks bir trade-off.** Tabloya bir satır eklediğimde veritabanı o tablodaki **her** indeksi de güncellemek zorunda. Beş indeksli bir tabloya bir satır eklemek, altı yapıyı güncellemek demek. Ayrıca indeksler diskte ve bellekte yer kaplıyor. Okuma ağırlıklı tablolarda (ürün kataloğu) bol indeks iyi; yazma ağırlıklı tablolarda (log, olay kaydı) her indeksi gerekçelendirmek gerekiyor. Mimari yazımdaki trade-off fikri burada da karşıma çıktı.

   Birkaç terim daha:
   - **Kümelenmiş indeks (clustered):** tablonun kendisi bu sırada saklanır, tabloda sadece bir tane olabilir. SQL Server'da birincil anahtar varsayılan olarak kümelenmiş indekstir.
   - **Kümelenmemiş indeks (nonclustered):** ayrı bir yapı, yaprakta satıra işaret eder.
   - **Kapsayan indeks (covering index):** sorgunun istediği tüm sütunlar indeksin içinde olduğu için tabloya hiç gitmeye gerek kalmaz.

## 3. Neyi yanlış anladım ya da hâlâ belirsiz

- Yabancı anahtar tanımlamanın otomatik olarak indeks oluşturduğunu sanıyordum. SQL Server ve PostgreSQL'de **oluşturmuyor** (MySQL'in InnoDB motoru oluşturuyor). EF Core ise migration'larda yabancı anahtar sütunlarına genelde kendisi indeks ekliyor. Yani "var mı?" sorusunun cevabı araca göre değişiyor, kontrol etmek gerekiyor.
- Planlayıcı indeksi kullanıp kullanmayacağına istatistiklere bakarak karar veriyor. İstatistikler eskiyince kötü plan seçebiliyormuş. Bu kısmı, sorgu planı okumayı öğrenince derinleştireceğim.
- Hash indeks, GIN, full-text gibi başka indeks türleri de var. Şimdilik B-ağacında kaldım.

## 4. Örnek

[`example/`](example/) klasöründe Python ve SQLite ile 300.000 satırlık bir tablo kurup aynı sorguyu indeksli ve indekssiz çalıştırıyorum. Script iki şey gösteriyor:

1. `EXPLAIN QUERY PLAN` çıktısı: indeks yokken `SCAN posts` (tam tarama), indeks varken `SEARCH posts USING INDEX ...`.
2. Süre farkı ve `WHERE substr(date, 1, 4) = '2026'` gibi sütunu fonksiyona sokan bir sorgunun indeks olsa bile yine tarama yaptığı.

Kendi makinemde indeksli sorgu, indekssiz olandan yüzlerce kat hızlıydı. Sayılar makineye göre değişir, ama plan çıktısındaki SCAN ve SEARCH farkı her yerde aynı.

**Yapay zekâ notu:** "Bu sorgu yavaş, indeks öner" dediğimde yapay zekâ genelde WHERE'deki her sütuna indeks öneriyor. Bunun yerine ona sorguyu, tablonun yaklaşık satır sayısını, okuma-yazma oranını ve mümkünse sorgu planını veriyorum. Önerisini de iki soruyla kontrol ediyorum: Bu indeks hangi yazma işlemlerini yavaşlatır? Bu sorguda sütun bir fonksiyona giriyor mu? Son söz her zaman gerçek sorgu planında.

## 5. Kaynakça

_Bu yazıda yararlandığım kaynaklar. Bağlantılara son erişim: 18 Kasım 2026._

- Markus Winand. *Use The Index, Luke!* (SQL indeksleme rehberi). https://use-the-index-luke.com/
- PostgreSQL Documentation, "Indexes". https://www.postgresql.org/docs/current/indexes.html
- Microsoft Learn, "SQL Server index architecture and design guide". https://learn.microsoft.com/sql/relational-databases/sql-server-index-design-guide
- SQLite Documentation, "EXPLAIN QUERY PLAN". https://www.sqlite.org/eqp.html
- Microsoft Learn, EF Core "Indexes". https://learn.microsoft.com/ef/core/modeling/indexes

---

© 2026 Zehra Betül Çuhadar. Bu yazının metni ve görselleri [CC BY-NC-ND 4.0](https://creativecommons.org/licenses/by-nc-nd/4.0/deed.tr) lisanslıdır: adımı ve bağlantıyı vererek, ticari olmayan amaçla ve değiştirmeden paylaşabilirsin. Kod örnekleri için tüm hakları saklıdır, bkz. [LICENSE-CODE](../../LICENSE-CODE).
