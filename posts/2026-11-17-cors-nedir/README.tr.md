[🇬🇧 English](README.en.md) | 🇹🇷 **Türkçe**

# CORS nedir? Tarayıcı isteğimi neden engelledi?

> *Zehra tarafından araştırıldı ve yazıldı. Yapay zekâ yardımıyla taslağı hazırlandı, ben gözden geçirdim.*

**Kısa cevap:** Tarayıcılar, bir sayfadaki JavaScript'in **başka bir kökene** (origin: şema + alan adı + port, örneğin `http://localhost:4200`) ait bir sunucudan gelen cevabı okumasını varsayılan olarak engeller. Buna **aynı köken kuralı** (same-origin policy) denir. **CORS** (Cross-Origin Resource Sharing), sunucunun `Access-Control-Allow-Origin` gibi header'larla "bu kökene izin veriyorum" demesini sağlayan standarttır. Önemli nokta: CORS'u **tarayıcı uygular, ayarını sunucu yapar.** Bu yüzden CORS hatası frontend'de görünür ama çözümü backend'dedir; ve CORS sunucuyu korumaz, kullanıcıyı korur.

## 1. Neyi araştırdım ve neden

Angular ile .NET'i ayrı portlarda çalıştırdığım ilk günden beri tanıdığım bir kırmızı yazı var: *"Access to XMLHttpRequest at 'http://localhost:5000/api/...' from origin 'http://localhost:4200' has been blocked by CORS policy..."* Genelde Stack Overflow'dan bir satır kopyalayıp (`AllowAnyOrigin()`) geçiyordum. Postman'de aynı isteğin sorunsuz çalışması da kafamı karıştırıyordu. Frontend gezegeninin bu ek yazısında CORS'un neden var olduğunu ve doğru nasıl ayarlanacağını anlamak istedim.

## 2. Üç ana çıkarım

1. **Aynı köken kuralı kullanıcıyı korur, CORS onu kontrollü gevşetir.** Tarayıcıda oturum açtığım bankanın çerezleri tarayıcımda duruyor. Eğer aynı köken kuralı olmasaydı, açtığım herhangi bir kötü niyetli sayfa arka planda `fetch("https://banka.com/hesaplarim")` diyebilir, tarayıcı çerezlerimi ekleyip isteği gönderir ve sayfa cevabı **okuyabilirdi**. Aynı köken kuralı bunu engelliyor: istek gidebilir, ama başka kökenden gelen cevabı JavaScript okuyamaz.

   Köken üç parçadan oluşuyor ve **üçü de aynı olmalı**:
   - `http://localhost:4200` ile `http://localhost:5000` → port farklı, **farklı köken**.
   - `http://site.com` ile `https://site.com` → şema farklı, farklı köken.
   - `https://site.com` ile `https://api.site.com` → alan adı farklı, farklı köken.

   CORS, sunucunun bu kuralı bilinçli olarak gevşetmesi: "Evet, `http://localhost:4200` benim cevaplarımı okuyabilir." Bunu cevaba eklediği header ile söylüyor:
   ```
   Access-Control-Allow-Origin: http://localhost:4200
   ```

   **Postman'de neden çalışıyor?** Çünkü CORS bir tarayıcı kuralı. Postman, `curl` ya da başka bir sunucu bu kuralı uygulamıyor. Bu da önemli bir şeyi gösteriyor: **CORS bir güvenlik duvarı değil.** API'mi yetkisiz erişimden korumak için kimlik doğrulama ve yetkilendirme gerekiyor, CORS değil.

2. **Bazı isteklerden önce tarayıcı izin sorar: preflight.** "Basit" istekler (sadece `GET`, `HEAD` ya da belirli içerik türleriyle `POST`, özel header'sız) doğrudan gönderiliyor; tarayıcı cevaptaki header'a bakıp JavaScript'in okumasına izin veriyor ya da vermiyor. Ama şu durumlarda istek "basit" sayılmıyor:
   - `PUT`, `DELETE`, `PATCH` gibi metotlar,
   - `Content-Type: application/json` (evet, Angular'ın her `POST`'u),
   - `Authorization` gibi özel header'lar.

   Bu durumda tarayıcı asıl istekten önce bir **`OPTIONS` isteği** (preflight) gönderip soruyor:
   ```
   OPTIONS /api/posts
   Origin: http://localhost:4200
   Access-Control-Request-Method: POST
   Access-Control-Request-Headers: content-type, authorization
   ```
   Sunucu izin veriyorsa şöyle cevaplıyor:
   ```
   Access-Control-Allow-Origin: http://localhost:4200
   Access-Control-Allow-Methods: GET, POST, PUT, DELETE
   Access-Control-Allow-Headers: content-type, authorization
   Access-Control-Max-Age: 600
   ```
   Ancak bundan sonra asıl istek gidiyor. DevTools'un Network sekmesinde iki istek görmemin sebebi bu. `Max-Age`, tarayıcının bu izni ne kadar süre önbelleğe alacağını söylüyor; her istekte tekrar sormasını engelliyor. Sık karşılaştığım bir hata da şu: sunucuda kimlik doğrulama middleware'i `OPTIONS` isteğini token olmadığı için `401` ile reddediyor ve preflight başarısız oluyor. ASP.NET Core'da `UseCors()`'un, `UseAuthentication()` ve `UseAuthorization()`'dan **önce** gelmesi gerekiyor.

3. **Doğru ayar: izin listesi, joker değil.** ASP.NET Core'da:
   ```csharp
   builder.Services.AddCors(o => o.AddPolicy("Frontend", p => p
       .WithOrigins("http://localhost:4200", "https://app.sirket.com")
       .WithMethods("GET", "POST", "PUT", "DELETE")
       .WithHeaders("Content-Type", "Authorization")));
   // ...
   app.UseCors("Frontend");
   ```
   Dikkat edilecekler:
   - **`AllowAnyOrigin()` (`*`) kolay ama genelde yanlış.** Herkese açık, kimlik doğrulaması olmayan bir API için (örneğin halka açık bir veri servisi) uygun olabilir, başka durumda değil.
   - **Çerezli istekler** (`withCredentials: true`) için `*` zaten çalışmıyor; standart, kimlik bilgisi taşıyan isteklerde açık bir köken ve `Access-Control-Allow-Credentials: true` istiyor.
   - **Gelen `Origin` header'ını olduğu gibi geri yansıtmak** (her isteğe "sen de izinlisin" demek) `*`'dan bile tehlikeli, çünkü çerezlerle birlikte çalışıyor. Güvenlik denetimlerinde sık bulunan bir açık.
   - Geliştirmede bir alternatif: Angular CLI'ın **proxy** ayarı (`proxy.conf.json`). Tarayıcı isteği `localhost:4200/api`'ye atıyor, geliştirme sunucusu onu `localhost:5000`'e iletiyor. Tarayıcı açısından aynı köken, CORS hiç devreye girmiyor. Canlıda da frontend ve API aynı alan adı altında (bir reverse proxy arkasında) sunulursa CORS'a gerek kalmayabiliyor.

## 3. Neyi yanlış anladım ya da hâlâ belirsiz

- CORS hatası alınca isteğin sunucuya hiç gitmediğini sanıyordum. Basit isteklerde istek **gidiyor ve işleniyor**, sadece cevabı JavaScript okuyamıyor. Yani CORS, bir `POST`'un sunucuda yan etki yaratmasını tek başına engellemiyor. Bu, CSRF denen saldırının neden ayrı bir koruma gerektirdiğini de açıklıyor (ayrı bir yazının konusu).
- CORS'u "backend'in frontend'i engellemesi" gibi düşünüyordum. Aslında tarayıcının kullanıcıyı koruması; backend sadece "bu köken güvenilir" diye izin veriyor.
- `SameSite` çerez ayarlarının CORS'la nasıl birlikte çalıştığı hâlâ bana biraz karışık geliyor.

## 4. Örnek

[`example/`](example/) klasöründe paketsiz bir Node.js örneği var: `4200` portunda basit bir "frontend" sayfası ve `5000` portunda bir "API". API'nin CORS'u bir ortam değişkeniyle açılıp kapatılabiliyor. Sayfayı tarayıcıda açıp DevTools'ta şunları görebiliyorum:
- CORS kapalıyken: konsolda tanıdık kırmızı hata, ama sunucu logunda isteğin geldiği.
- CORS açıkken: `POST` öncesinde `OPTIONS` preflight isteği ve ardından asıl istek.
- Aynı API'ye terminalden `curl` ile her durumda erişilebildiği (CORS'un bir güvenlik duvarı olmadığının kanıtı).

**Yapay zekâ notu:** CORS hatasını yapay zekâya yapıştırınca en sık aldığım cevap `AllowAnyOrigin().AllowAnyHeader().AllowAnyMethod()`. Hata gidiyor, ama bu canlıya giderse API her siteye açık oluyor. Daha iyi soru: "Frontend'im `https://app.sirket.com`, API'm `https://api.sirket.com`, çerez kullanmıyorum, `Authorization` header'ı gönderiyorum. En dar CORS politikası ne olmalı ve middleware sırası nasıl olmalı?" Bir de geliştirme için Angular proxy'si gibi CORS'u hiç gerektirmeyen yolları da önermesini istiyorum.

## 5. Kaynakça

_Bu yazıda yararlandığım kaynaklar. Bağlantılara son erişim: 18 Kasım 2026._

- MDN Web Docs, "Cross-Origin Resource Sharing (CORS)". https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/CORS
- MDN Web Docs, "Same-origin policy". https://developer.mozilla.org/en-US/docs/Web/Security/Same-origin_policy
- WHATWG Fetch Standard, "CORS protocol". https://fetch.spec.whatwg.org/#http-cors-protocol
- Microsoft Learn, "Enable Cross-Origin Requests (CORS) in ASP.NET Core". https://learn.microsoft.com/aspnet/core/security/cors
- Angular Docs, "Proxying to a backend server". https://angular.dev/tools/cli/serve#proxying-to-a-backend-server
- PortSwigger Web Security Academy, "CORS" (yaygın yanlış yapılandırmalar). https://portswigger.net/web-security/cors

---

© 2026 Zehra Betül Çuhadar. Bu yazının metni ve görselleri [CC BY-NC-ND 4.0](https://creativecommons.org/licenses/by-nc-nd/4.0/deed.tr) lisanslıdır: adımı ve bağlantıyı vererek, ticari olmayan amaçla ve değiştirmeden paylaşabilirsin. Kod örnekleri için tüm hakları saklıdır, bkz. [LICENSE-CODE](../../LICENSE-CODE).
