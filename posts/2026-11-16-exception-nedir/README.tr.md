[🇬🇧 English](README.en.md) | 🇹🇷 **Türkçe**

# İstisna (exception) nedir? Hata yönetimi nasıl yapılır?

> *Zehra tarafından araştırıldı ve yazıldı. Yapay zekâ yardımıyla taslağı hazırlandı, ben gözden geçirdim.*

**Kısa cevap:** İstisna (exception), bir fonksiyonun **yapacağını söylediği işi yapamadığını** haber veren bir mekanizmadır. Exception fırlatıldığında (`throw`) normal akış durur ve çağrı yığını (call stack) geriye doğru, onu yakalayan (`catch`) ilk bloğa kadar çözülür. Hiçbir yer yakalamazsa program çöker. İyi hata yönetiminin özü üç kural: **yalnızca bir şey yapabileceğin yerde yakala**, **hatayı yutma** ve **beklenen durumlar için exception değil normal kontrol akışı kullan.**

## 1. Neyi araştırdım ve neden

Her gün `try/catch` yazıyorum, ama çoğu zaman refleksle: bir yerde hata olabilir, etrafını sar, `catch`'te logla, devam et. Basics gezegeninin bu ikinci ek yazısında bu refleksin doğru olup olmadığını sorgulamak istedim. Çünkü yapay zekânın ürettiği kodda da en sık gördüğüm kalıplardan biri her şeyi saran geniş `try/catch` blokları.

## 2. Üç ana çıkarım

1. **Exception, dönüş değerinin taşıyamadığı bir mesajdır.** Eski C kodunda hatalar dönüş değeriyle bildirilirdi (`-1` dönerse hata var). Sorun: çağıran kontrol etmeyi unutabilir ve hata sessizce ilerler. Exception ise görmezden gelinemez; ya biri yakalar ya program durur. Fırlatıldığında olanlar:
   - Fonksiyon o noktada durur, kalan satırlar çalışmaz.
   - Çağrı yığını geriye çözülür (stack unwinding): her seviyede `catch` aranır.
   - Yolda `finally` blokları (ve C#'ta `using` ile açılan kaynakların `Dispose`'u) çalışır; dosyalar, bağlantılar kapanır.
   - Eşleşen bir `catch` bulunursa akış orada devam eder. Bulunmazsa uygulama çöker (.NET'te "unhandled exception", tarayıcıda konsolda kırmızı hata).

   Exception nesnesi, mesajın yanında **stack trace**'i de taşır: hatanın hangi dosyada, hangi satırda, hangi çağrı zinciriyle oluştuğunu. Hata ayıklarken en değerli bilgi bu.

2. **Yakalama yeri: hatayla bir şey yapabilen yer.** Her fonksiyon kendi exception'ını yakalamak zorunda değil, hatta yakalamamalı. Bir fonksiyon hatayla anlamlı bir şey yapamıyorsa, yukarı bırakmalı. Anlamlı şeyler şunlar:
   - **Kurtarmak:** başka bir yol denemek (yedek kaynak, varsayılan değer, tekrar deneme).
   - **Anlam eklemek:** düşük seviyeli hatayı daha anlamlı bir hataya sarıp yeniden fırlatmak. C#'ta `throw new OrderException("Sipariş kaydedilemedi", ex);` ile orijinal hata `InnerException` olarak korunur.
   - **Sınırda karşılamak:** uygulamanın en dış katmanında (ASP.NET Core'da global exception handler ve `ProblemDetails`, Angular'da `ErrorHandler` ve HTTP interceptor) kullanıcıya anlaşılır bir mesaj göstermek ve hatayı loglamak.

   Kaçınılması gerekenler:
   - **Hatayı yutmak:** `catch { }` ya da `catch (Exception) { return null; }`. Hata kayboluyor, program yanlış veriyle devam ediyor ve gerçek sorun çok sonra, çok uzakta ortaya çıkıyor. En tehlikeli kalıp bu.
   - **Stack trace'i silmek:** C#'ta `catch (Exception ex) { throw ex; }` stack trace'i o satırdan yeniden başlatır, hatanın asıl yeri kaybolur. Doğrusu sadece `throw;`.
   - **Her şeyi `Exception` ile yakalamak:** `NullReferenceException` gibi programlama hatalarını da yakalayıp gizliyor. Mümkün olduğunca spesifik tipi yakalamak gerekiyor (`HttpRequestException`, `DbUpdateException`).

3. **Beklenen durum exception değildir.** "Kullanıcı bulunamadı", "form geçersiz", "stok yetersiz" gibi durumlar programın normal akışının bir parçası. Bunları exception ile yönetmek hem yavaş (exception fırlatmak, stack trace topladığı için normal bir `return`'den çok daha pahalı) hem de okuması zor. .NET'in kendi tasarım rehberi de bunu söylüyor: sık gerçekleşen durumlar için `TryParse` gibi desenler kullan.
   - `int.Parse("abc")` exception fırlatır; `int.TryParse("abc", out var n)` `false` döner. Kullanıcı girdisi için ikincisi doğru.
   - API'de bulunamayan bir kayıt için exception fırlatıp yakalamak yerine `null` / `NotFound()` dönmek.
   - Bazı ekipler bunun için **Result deseni** kullanıyor: fonksiyon ya başarılı bir değer ya da bir hata nesnesi dönüyor, çağıran ikisini de ele almak zorunda kalıyor.

   Kabaca ayrım şöyle: **exception, gerçekten istisnai olan için** (veritabanı erişilemiyor, disk dolu, programlama hatası); **dönüş değeri, beklenen bir sonuç için** (bulunamadı, geçersiz).

## 3. Neyi yanlış anladım ya da hâlâ belirsiz

- `try/catch` eklemenin kodu "daha güvenli" yaptığını sanıyordum. Çoğu zaman tersi: hatayı yutan bir `catch`, uygulamanın çökmesinden daha kötü, çünkü sorunu gizliyor.
- Asenkron kodda hata akışı farklı: C#'ta `async void` metotlarda fırlatılan exception yakalanamıyor ve uygulamayı çökertebiliyor. JavaScript'te `await` edilmeyen bir Promise'in hatası "unhandled rejection" olarak kayboluyor. Bunu async/await yazılarında derinleştireceğim.
- Result deseni ile exception arasında ne zaman hangisini seçeceğim konusunda topluluk ikiye bölünmüş görünüyor. Go ve Rust gibi diller exception yerine hata değerleri kullanıyor. Henüz bir tarafı seçecek kadar tecrübem yok.

## 4. Örnek

[`example/`](example/) klasöründe Node.js ile yazılmış küçük bir örnek var (C# karşılıkları yorum satırlarında). Aynı "dosyadan ayar oku" işini üç şekilde yapıyor:
1. **Hatayı yutan** versiyon: sessizce `null` dönüyor ve program çok sonra, alakasız bir yerde patlıyor.
2. **Anlam ekleyip yeniden fırlatan** versiyon: orijinal hatayı `cause` olarak koruyor.
3. **Beklenen durum için dönüş değeri** kullanan versiyon: dosya yoksa varsayılan ayarla devam ediyor, ama dosya bozuksa hatayı yukarı bırakıyor.

**Yapay zekâ notu:** Yapay zekânın yazdığı kodda en çok kontrol ettiğim şeylerden biri `catch` blokları. Sık gördüğüm hatalar: her metodu `try/catch (Exception)` ile sarmak, `catch` içinde sadece `Console.WriteLine` yapıp devam etmek, `throw ex;` yazmak. Ona açıkça söylüyorum: "Hataları yutma, sadece kurtarabileceğin yerde yakala, diğerlerini global handler'a bırak." Bir de ürettiği koda "bu satır exception fırlatırsa ne olur?" sorusunu soruyorum; cevap "kullanıcı yanlış veri görür ve kimse fark etmez" ise orada bir sorun var.

## 5. Kaynakça

_Bu yazıda yararlandığım kaynaklar. Bağlantılara son erişim: 18 Kasım 2026._

- Microsoft Learn, "Best practices for exceptions" (.NET). https://learn.microsoft.com/dotnet/standard/exceptions/best-practices-for-exceptions
- Microsoft Learn, "Handle errors in ASP.NET Core" (global exception handler, ProblemDetails). https://learn.microsoft.com/aspnet/core/fundamentals/error-handling
- MDN Web Docs, "try...catch" ve "Error: cause". https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Error/cause
- Angular Docs, "ErrorHandler". https://angular.dev/api/core/ErrorHandler
- Krzysztof Cwalina, Brad Abrams. *Framework Design Guidelines*, Addison-Wesley (exception bölümü).
