[🇬🇧 English](README.en.md) | 🇹🇷 **Türkçe**

# Veritabanı nedir? İlişkisel model, tablo ve anahtar

> *Zehra tarafından araştırıldı ve yazıldı. Yapay zekâ yardımıyla taslağı hazırlandı, ben gözden geçirdim.*

**Kısa cevap:** Veritabanı, veriyi kalıcı olarak saklayan, aynı anda birçok kullanıcının güvenle okuyup yazabilmesini sağlayan ve verinin kurallara uygun (tutarlı) kalmasını garanti eden bir yazılımdır. İlişkisel veritabanları (SQL Server, PostgreSQL, MySQL, SQLite) veriyi **tablolarda** tutar; tablolar arasındaki bağı **anahtarlarla** kurar ve veriye **SQL** ile erişilir.

## 1. Neyi araştırdım ve neden

İşte her gün .NET ile bir veritabanına bağlanan kod yazıyorum, EF Core ile tablolara sınıf gibi davranıyorum. Ama "veritabanı aslında ne iş yapıyor, neden veriyi bir JSON dosyasına yazmıyoruz?" sorusuna net bir cevabım yoktu. Data gezegeninin ilk yazısı bu yüzden en temelden başlıyor.

Bir de kendi projemde ilginç bir durum var: Learning Sky'ın "veritabanı" aslında `posts/*/meta.json` dosyaları ve onlardan üretilen `sky.json`. Bu küçük bir proje için harika çalışıyor. Neden büyük bir sistem için çalışmayacağını anlamak, veritabanının neden var olduğunu anlamak demek.

## 2. Üç ana çıkarım

1. **Veritabanı, dosyanın çözemediği dört sorunu çözer.** Veriyi bir dosyaya yazmak kolay. Zor olan şunlar:
   - **Aynı anda erişim:** İki kişi aynı anda aynı dosyayı yazarsa biri diğerinin değişikliğini ezer. Veritabanı kilitler ve transaction'larla bunu yönetir.
   - **Tutarlılık:** "Her siparişin bir müşterisi olmalı" gibi kuralları veritabanı zorlar. Dosya hiçbir kuralı umursamaz.
   - **Çökmeye dayanıklılık:** Yazma yarıda kesilirse dosya bozulabilir. Veritabanı ya işin tamamını yapar ya hiçbirini (bunun adı atomiklik, ACID'in A'sı; Transaction yazısında derinleşeceğim).
   - **Hızlı arama:** Milyon satırlık dosyada bir kaydı bulmak için baştan sona okumak gerekir. Veritabanı indekslerle bunu milisaniyelere indirir.

2. **İlişkisel model: tablo, satır, sütun ve anahtar.** 1970'te Edgar F. Codd'un önerdiği model hâlâ en yaygın model. Temel fikir, veriyi tekrar etmeden tablolara bölmek:
   - **Tablo:** aynı türden kayıtlar (örneğin `posts`).
   - **Satır:** tek bir kayıt (bir yazı).
   - **Sütun:** kaydın bir özelliği (başlık, tarih). Her sütunun bir tipi var.
   - **Birincil anahtar (primary key):** bir satırı benzersiz tanımlayan sütun (`id`). Aynı değer iki kez olamaz, boş olamaz.
   - **Yabancı anahtar (foreign key):** başka bir tablonun birincil anahtarına işaret eden sütun. `posts.planet_id` → `planets.id`. Veritabanı, olmayan bir gezegene yazı bağlamana izin vermez. Buna **referans bütünlüğü** deniyor.

   İlişki türleri üç tane: **bire bir**, **bire çok** (bir gezegenin çok yazısı var) ve **çoka çok** (bir yazının çok etiketi, bir etiketin çok yazısı var). Çoka çok ilişki doğrudan kurulamıyor, araya bir **bağlantı tablosu** (`post_tags`) giriyor. EF Core'daki "navigation property"lerin altında yatan şey tam olarak bu.

3. **SQL "ne istediğimi" söyler, "nasıl bulacağını" değil.** SQL bildirimsel (declarative) bir dil. `SELECT ... WHERE ... JOIN ...` yazdığımda veritabanına sonucu tarif ediyorum, hangi sırayla hangi tabloyu okuyacağına veritabanının **sorgu planlayıcısı** karar veriyor. Bu yüzden aynı sorgu indeks eklenince yüz kat hızlanabiliyor, kodda tek satır değişmeden. LINQ'i sevmemin sebebi de bu fikir: o da ne istediğimi tarif ediyor.

## 3. Neyi yanlış anladım ya da hâlâ belirsiz

- "Veritabanı" ile "veritabanı yönetim sistemi"ni (DBMS) aynı şey sanıyordum. Teknik olarak veritabanı verinin kendisi, SQL Server ise onu yöneten yazılım. Günlük dilde ikisine de veritabanı deniyor.
- Neden her şeyi tek bir büyük tabloda tutmuyoruz? Cevap tekrarı önlemek: gezegenin adını her yazı satırına yazarsam, adını değiştirdiğimde yüzlerce satırı güncellemem gerekir ve birini unutursam veri tutarsızlaşır. Bunun adı normalizasyon, ayrı bir yazının konusu. Ama bazen performans için bilerek tekrar yapılıyormuş, bunu henüz tam kavramadım.
- NoSQL veritabanları bu kuralların bir kısmını neden bilerek gevşetiyor? Data gezegeninde ileride bu soruya döneceğim.

## 4. Örnek

[`example/`](example/) klasöründe Learning Sky'ı küçük bir ilişkisel veritabanı gibi modelledim: `planets`, `posts`, `tags` ve bağlantı tablosu `post_tags`. Script SQLite ile tabloları kurar, birkaç kayıt ekler, bir JOIN sorgusu çalıştırır ve sonra **olmayan bir gezegene yazı eklemeyi dener**. Veritabanı yabancı anahtar kuralı yüzünden buna izin vermez. Bir JSON dosyası bu hatayı sessizce kabul ederdi.

```
planets 1 ── * posts * ── * tags
              (post_tags bağlantı tablosu)
```

**Yapay zekâ notu:** Yapay zekâya tablo tasarlatırken iş kurallarını açıkça söylemem gerekiyor ("bir yazının tam olarak bir gezegeni var, birden çok etiketi olabilir"). Söylemezsem her şeyi tek tabloya koyan ya da gereksiz ilişkiler kuran şemalar üretebiliyor. Ürettiği şemada mutlaka şunlara bakıyorum: her tablonun birincil anahtarı var mı, yabancı anahtarlar tanımlı mı, `NOT NULL` ve `UNIQUE` kısıtları iş kurallarıyla uyuşuyor mu?

## 5. Kaynakça

_Bu yazıda yararlandığım kaynaklar. Bağlantılara son erişim: 18 Kasım 2026._

- E. F. Codd. "A Relational Model of Data for Large Shared Data Banks", *Communications of the ACM*, 1970.
- PostgreSQL Documentation, "Constraints" (birincil ve yabancı anahtar). https://www.postgresql.org/docs/current/ddl-constraints.html
- SQLite Documentation, "SQLite Foreign Key Support". https://www.sqlite.org/foreignkeys.html
- Martin Kleppmann. *Designing Data-Intensive Applications*, O'Reilly, Bölüm 2 (veri modelleri).
