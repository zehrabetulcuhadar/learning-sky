[🇬🇧 English](README.en.md) | 🇹🇷 **Türkçe**

# Code review nasıl yapılır? Neye, hangi sırayla bakılır?

> *Zehra tarafından araştırıldı ve yazıldı. Yapay zekâ yardımıyla taslağı hazırlandı, ben gözden geçirdim.*

**Kısa cevap:** Code review, bir değişikliğin ana koda girmeden önce başka biri tarafından okunmasıdır. Amacı sadece hata bulmak değil: **kod tabanının sağlığını korumak**, **bilgiyi ekibe yaymak** ve **ortak standartları korumak**. İyi bir review büyükten küçüğe bakar: önce **değişiklik doğru problemi mi çözüyor ve tasarım mantıklı mı**, sonra **doğru çalışıyor mu** (kenar durumlar, hatalar, güvenlik), sonra **testler**, sonra **okunabilirlik**, en son **stil**. Stil (girinti, tırnak, sıralama) insanların değil, formatter ve linter'ların işi. Google'ın review rehberindeki ölçüt de güzel: değişiklik mükemmel olmak zorunda değil, **kod tabanının genel sağlığını iyileştiriyorsa** onaylanmalı.

## 1. Neyi araştırdım ve neden

İngilizce gezegeninde review yorumlarının **nasıl yazılacağını** anlatmıştım. Bu yazı işin diğer yarısı: review'da **neye bakılacağı**. Yapay zekâ çağında bu soru daha önemli hale geldi. Kodun giderek daha büyük kısmını yapay zekâ yazarken, mühendisin işinin önemli bir parçası okumak, sorgulamak ve onaylamak. Yani review yapmak, artık neredeyse kod yazmak kadar temel bir beceri.

## 2. Üç ana çıkarım

1. **Büyükten küçüğe bak: piramidin tepesinden başla.** Stil yorumlarıyla başlayan bir review, asıl sorunları kaçırabiliyor ya da yazarı yoruyor. Benim sıram:
   1. **Amaç:** PR açıklamasını ve bağlı işi oku. Bu değişiklik neden var? Doğru problemi mi çözüyor? Bazen en değerli yorum "Buna gerçekten ihtiyacımız var mı?" oluyor.
   2. **Tasarım:** Değişiklik doğru yerde mi? Mevcut mimariye uyuyor mu, yoksa yeni bir yol mu açıyor? Gereksiz karmaşık mı (ileride lazım olur diye eklenmiş soyutlamalar)? Bu aşamada büyük bir sorun varsa, satır satır yorum yapmadan önce bunu konuşmak gerekiyor.
   3. **Doğruluk:** Kod söylediği şeyi yapıyor mu? Kenar durumlar (boş liste, `null`, sıfır, çok büyük girdi), hata yönetimi (hata yutuluyor mu?), eşzamanlılık (iki istek aynı anda gelirse?), güvenlik (kullanıcı girdisi doğrulanıyor mu, yetki kontrolü var mı, bir sır koda girmiş mi?), performans (döngü içinde veritabanı sorgusu, N+1).
   4. **Testler:** Yeni davranış test edilmiş mi? Testler gerçekten bir şey doğruluyor mu? Hata düzeltmesiyse, hatayı yakalayan bir test eklenmiş mi?
   5. **Okunabilirlik:** İsimler anlamlı mı? Bir yorum gerekiyorsa, bu kodun daha açık yazılabileceğinin işareti mi? Altı ay sonra bu kodu ilk kez gören biri anlar mı?
   6. **Stil:** Burada insan yorumu neredeyse olmamalı. Prettier, ESLint, `dotnet format` ve .NET analyzer'ları bunu CI'da otomatik kontrol etmeli. Makinenin yakalayabildiği bir şey için bir insanın dikkatini harcamamak gerekiyor.

2. **Küçük PR, hızlı review.** Araştırmaların ve şirket deneyimlerinin ortak bulgusu: review'un etkinliği PR büyüdükçe hızla düşüyor. SmartBear'ın Cisco'daki çalışmasına göre bir seferde 200-400 satırdan fazla kod incelendiğinde hata bulma oranı belirgin şekilde azalıyor; Google'ın rehberi de küçük değişiklikleri (small CLs) öneriyor. 50 satırlık bir PR'a on yorum gelir, 1500 satırlık bir PR'a "LGTM" gelir.
   - **Yazar olarak:** değişikliği mantıklı parçalara böl (önce refactoring, sonra yeni özellik), iyi bir PR açıklaması yaz (ne, neden, nasıl test edildi, ekran görüntüsü), göndermeden önce kendi diff'ini bir kez kendin incele.
   - **Reviewer olarak:** hızlı ol. Google'ın rehberi, bir review isteğine en geç bir iş günü içinde cevap vermeyi öneriyor. Bekleyen bir PR, yazarı bağlam değiştirmeye zorluyor ve çatışmaları (merge conflict) büyütüyor. Hızlı olmak, her şeyi hemen onaylamak değil; ilk geri bildirimi hızlı vermek demek.

3. **Review bir sohbet, bir kapı bekçiliği değil.** İyi bir review kültürünün özellikleri:
   - **Kişiyi değil kodu konuş** (İngilizce yazımda ayrıntılı anlatmıştım).
   - **Ağırlığı belirt:** engelleyen bir sorun mu, öneri mi, küçük bir not mu? (`nit:`, `suggestion:`, `issue:`)
   - **Övgüyü de yaz.** İyi bir çözümü fark etmek, öğrenmenin bir parçası.
   - **Yazar haklı olabilir.** Reviewer'ın tercihi, kural değil. Ekipte bir standart yoksa ve iki yol da makul ise, yazarın tercihi kalabilir.
   - **Uzayan tartışmayı yüz yüze çöz.** On mesajlık bir yorum zinciri, beş dakikalık bir görüşmeyle çözülebiliyor; sonucu PR'a not düşmek yeterli.
   - **Review bir öğrenme aracı.** Yeni birinin kıdemli birinin kodunu incelemesi de çok değerli: hem öğreniyor hem de "bunu anlamadım" demesi, kodun açık olmadığının sinyali.

## 3. Neyi yanlış anladım ya da hâlâ belirsiz

- Review'un amacını "hata bulmak" sanıyordum. Microsoft'un bir araştırmasında (Bacchelli ve Bird, 2013) geliştiricilerin review'dan en çok hata bulmayı beklediği, ama pratikte review'un daha çok bilgi paylaşımı, alternatif çözümler ve kod iyileştirmesi sağladığı görülmüş. Hata bulmak önemli ama tek fayda değil.
- Kıdemli birinin kodunu incelerken "ben kimim ki yorum yapayım?" hissi. Okuduğum her kaynak tersini söylüyor: soru sormak, en değerli review yorumlarından biri.
- Yapay zekâ ile yapılan otomatik review araçlarının insan review'unu ne kadar değiştireceği belirsiz. Şimdilik bana mantıklı gelen: yapay zekâ ilk taramayı yapsın (bariz hatalar, eksik testler), insan tasarıma ve bağlama baksın.

## 4. Örnek

[`example/`](example/) klasöründe iki şey var:
- **`pull_request_template.md`**: kendi projelerimde kullanmak için hazırladığım PR şablonu (ne, neden, nasıl test edildi, kontrol listesi). GitHub bu dosyayı `.github/` klasörüne konduğunda her yeni PR'a otomatik ekliyor.
- **`review-exercise.md`**: içine bilerek 6 sorun yerleştirdiğim küçük bir .NET controller diff'i ve en altta cevapları. Önce kendi kendine incelemek, sonra cevaplara bakmak için.

**Yapay zekâ notu:** Yapay zekâ ilk review taraması için çok iyi: diff'i verip "doğruluk, güvenlik, eksik test ve performans açısından incele, sadece gerçek sorunları yaz, stil yorumu yapma" dediğimde işe yarar şeyler buluyor. Ama iki zaafı var: projenin bağlamını bilmiyor (neden böyle bir karar verildiğini, ekibin kurallarını) ve bazen var olmayan sorunlar uyduruyor ya da her şeye bir yorum yazıyor. Ayrıca yapay zekânın yazdığı kodu yine yapay zekâya inceletmek, aynı kör noktaları paylaşabilir. Son onayı, bağlamı bilen bir insan vermeli.

## 5. Kaynakça

_Bu yazıda yararlandığım kaynaklar. Bağlantılara son erişim: 18 Kasım 2026._

- Google Engineering Practices, "The Code Reviewer's Guide". https://google.github.io/eng-practices/review/reviewer/
- Google Engineering Practices, "Small CLs". https://google.github.io/eng-practices/review/developer/small-cls.html
- SmartBear, "Best Practices for Code Review" (Cisco çalışması). https://smartbear.com/learn/code-review/best-practices-for-peer-code-review/
- Alberto Bacchelli, Christian Bird. "Expectations, Outcomes, and Challenges of Modern Code Review", ICSE 2013.
- GitHub Docs, "Creating a pull request template for your repository". https://docs.github.com/communities/using-templates-to-encourage-useful-issues-and-pull-requests/creating-a-pull-request-template-for-your-repository
