[🇬🇧 English](README.en.md) | 🇹🇷 **Türkçe**

# Test neden yazılır? Test piramidi nedir?

> *Zehra tarafından araştırıldı ve yazıldı. Yapay zekâ yardımıyla taslağı hazırlandı, ben gözden geçirdim.*

**Kısa cevap:** Otomatik testler, kodun beklenen şekilde çalıştığını **her değişiklikten sonra saniyeler içinde** kontrol eden kodlardır. Asıl değerleri hatayı bir kez bulmak değil, kodu **korkmadan değiştirebilmeyi** sağlamaktır. **Test piramidi**, Mike Cohn'un önerdiği ve Martin Fowler'ın yaygınlaştırdığı bir dengedir: tabanda çok sayıda hızlı ve ucuz **unit test**, ortada daha az **integration test**, tepede çok az sayıda yavaş ve kırılgan **uçtan uca (e2e) test**. Mantık basit: test ne kadar yukarıdaysa o kadar gerçekçi ama o kadar yavaş, pahalı ve bakımı zor.

## 1. Neyi araştırdım ve neden

Quality gezegeninde araçlardan (terminal, Git) sonra en çok merak ettiğim konu test. Dürüst olmak gerekirse, test yazmayı çoğu zaman "zaman kalırsa" yapılan bir iş olarak gördüm. Ama yapay zekâ kod yazmaya başlayınca bakışım değişti: kodu ben yazmıyorsam, doğru çalıştığını nasıl bileceğim? Her seferinde elle tıklayarak mı? Testler, yapay zekânın yazdığı kodun güvenlik ağı gibi görünüyor.

## 2. Üç ana çıkarım

1. **Testin asıl faydası değişiklik yapma cesareti.** Testsiz bir kod tabanında her değişiklik bir kumar: "bunu düzeltirsem başka bir yeri bozar mıyım?" Bu korku insanları değişiklikten kaçındırıyor, kod çürüyor. Testler şunları sağlıyor:
   - **Regresyon güvenliği:** dün çalışan bir şeyin bugün bozulduğunu hemen fark etmek.
   - **Refactoring güvencesi:** yapıyı değiştirirken davranışın aynı kaldığını kanıtlamak.
   - **Yaşayan dokümantasyon:** iyi isimlendirilmiş bir test (`Should_reject_order_when_quantity_is_negative`) kodun ne yapması gerektiğini anlatıyor ve eskimiyor, çünkü eskirse kırmızı yanıyor.
   - **Tasarım geri bildirimi:** test etmesi zor bir kod, genelde fazla bağımlılığı olan, fazla iş yapan bir koddur. Testi yazmak zorlaşıyorsa tasarım bir şey söylüyor.

2. **Piramit, katmanların maliyetini dengeler.**

   ```
          /\        e2e (az): gerçek tarayıcı, gerçek API, gerçek veritabanı
         /  \
        /----\      integration (orta): birkaç parça birlikte, örn. API + veritabanı
       /      \
      /--------\    unit (çok): tek bir fonksiyon ya da sınıf, bağımlılıklar sahte
   ```

   - **Unit test:** tek bir birimi (bir fonksiyon, bir sınıf) yalıtarak test eder. Milisaniyeler sürer, binlercesi saniyeler içinde çalışır. Kırıldığında sorunun yeri bellidir. .NET'te xUnit/NUnit, Angular'da Jasmine/Karma ya da Vitest/Jest.
   - **Integration test:** birden fazla parçanın birlikte çalıştığını test eder: API'nin gerçekten veritabanına yazabildiğini, servisin gerçek HTTP isteğini doğru çözdüğünü. Daha yavaştır, kurulum ister. .NET'te `WebApplicationFactory` ile bütün API'yi bellek içinde ayağa kaldırıp test etmek yaygın; veritabanı için Testcontainers ile gerçek bir SQL Server'ı Docker'da çalıştırmak mümkün.
   - **E2E test:** kullanıcı gibi davranır: tarayıcıyı açar, butona tıklar, sonucu görür. En gerçekçi ama en yavaş ve en kırılgan (bir buton yer değiştirince, ağ yavaşlayınca bozulabilir). Playwright, Cypress. Sadece en kritik akışlar için: giriş, ödeme, kayıt.

   Ters piramit, yani çoğu testin e2e olduğu durum, "dondurma külahı" anti-deseni olarak anılıyor: test paketi saatlerce sürüyor, sık sık sebepsiz kırılıyor ve ekip testlere güvenmemeye başlıyor.

3. **İyi bir unit test: AAA, tek davranış, hızlı ve bağımsız.** Testin iskeleti **Arrange-Act-Assert**: hazırla, çalıştır, doğrula. İyi bir unit test:
   - **Tek bir davranışı** test eder (bir testte tek bir "neden kırılabilir" olmalı).
   - **Hızlıdır ve bağımsızdır:** veritabanına, ağa, saate, rastgele sayıya bağlı değildir; bunlar sahteleriyle (fake/mock) değiştirilir.
   - **Uygulamayı değil, davranışı test eder:** özel metotların içini değil, dışarıdan görünen sonucu. Böylece refactoring testleri kırmaz.
   - **Kenar durumları kapsar:** boş liste, sıfır, negatif sayı, `null`, çok büyük girdi.

   Kod kapsama (coverage) yüzdesi faydalı bir sinyal ama hedef değil: yüzde 100 kapsama, testlerin doğru şeyi kontrol ettiğini garanti etmiyor. Hiçbir şeyi doğrulamayan (assert'siz) bir test de satırları "kapsıyor".

## 3. Neyi yanlış anladım ya da hâlâ belirsiz

- Piramidin oranlarını kesin bir kural sanıyordum (örneğin %70/%20/%10). Aslında bir yön gösterici. Kent C. Dodds'un "Testing Trophy" modeli frontend için integration testleri merkeze alıyor; Spotify'ın "honeycomb" modeli mikroservisler için yine integration ağırlıklı. Piramit tartışılmaz değil, ama "yavaş testten az, hızlı testten çok" fikri her modelde ortak.
- Unit ve integration arasındaki çizgi tartışmalı. "Unit" tek bir sınıf mı, yoksa bir davranış birimi mi? İki farklı okul var (London ve Classic/Detroit). Mock'ların ne kadar kullanılacağı da buna bağlı. Bunu "Mock, stub, fake farkı" yazısında açacağım.
- TDD'yi (önce testi yazmak) henüz gerçekten denemedim.

## 4. Örnek

[`example/`](example/) klasöründe Node.js'in yerleşik test koşucusuyla (`node --test`, paket yok) küçük bir örnek var: bir sepet indirimi fonksiyonu ve onun için AAA biçiminde yazılmış unit testler, bir de fonksiyonu "sahte bir depo" ile birlikte çalıştıran küçük bir integration testi. Testlerden biri bilerek bir kenar durumu (negatif adet) yakalıyor.

**Yapay zekâ notu:** Yapay zekâ test yazmakta çok hızlı ama iki tuzağı var. Birincisi, mevcut kodun **ne yaptığını** test ediyor, **ne yapması gerektiğini** değil; kodda hata varsa, hatayı "doğru" kabul eden bir test yazabiliyor. İkincisi, her şeyi mock'layıp hiçbir şeyi gerçekten test etmeyen testler üretebiliyor. Bu yüzden önce davranışı kendim tarif ediyorum ("negatif adet reddedilmeli, 1000 TL üstüne %10 indirim"), testleri ondan yazdırıyorum. Sonra test çalışırken kodu bilerek bozup testin kırmızıya döndüğünü kontrol ediyorum. Kırmızıya dönmeyen test, test değildir.

## 5. Kaynakça

_Bu yazıda yararlandığım kaynaklar. Bağlantılara son erişim: 18 Kasım 2026._

- Martin Fowler. "Test Pyramid" (2012). https://martinfowler.com/bliki/TestPyramid.html
- Ham Vocke. "The Practical Test Pyramid", martinfowler.com (2018). https://martinfowler.com/articles/practical-test-pyramid.html
- Mike Cohn. *Succeeding with Agile*, Addison-Wesley, 2009 (piramidin kaynağı).
- Kent C. Dodds. "The Testing Trophy and Testing Classifications". https://kentcdodds.com/blog/the-testing-trophy-and-testing-classifications
- Microsoft Learn, "Integration tests in ASP.NET Core". https://learn.microsoft.com/aspnet/core/test/integration-tests
- Vladimir Khorikov. *Unit Testing: Principles, Practices, and Patterns*, Manning, 2020.

---

© 2026 Zehra Betül Çuhadar. Bu yazının metni ve görselleri [CC BY-NC-ND 4.0](https://creativecommons.org/licenses/by-nc-nd/4.0/deed.tr) lisanslıdır: adımı ve bağlantıyı vererek, ticari olmayan amaçla ve değiştirmeden paylaşabilirsin. Kod örnekleri için tüm hakları saklıdır, bkz. [LICENSE-CODE](../../LICENSE-CODE).
