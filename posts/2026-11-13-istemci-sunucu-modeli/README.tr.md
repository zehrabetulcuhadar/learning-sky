[🇬🇧 English](README.en.md) | 🇹🇷 **Türkçe**

# İstemci-sunucu modeli nedir? Frontend ve backend nasıl ayrılır?

> *Zehra tarafından araştırıldı ve yazıldı. Yapay zekâ yardımıyla taslağı hazırlandı, ben gözden geçirdim.*

**Kısa cevap:** İstemci-sunucu modelinde iki rol vardır: **istemci** (client) bir şey ister, **sunucu** (server) isteği işleyip cevap verir. Konuşmayı her zaman istemci başlatır. Web'de istemci genelde tarayıcıda çalışan **frontend** kodu (benim işimde Angular), sunucu ise veriyi ve iş kurallarını yöneten **backend** kodu (.NET API) ve onun arkasındaki veritabanıdır. Aradaki sınırın en önemli sonucu şudur: **istemci kullanıcının elindedir, ona güvenilmez.** Doğrulama, yetki ve iş kuralları mutlaka sunucuda olmalıdır.

## 1. Neyi araştırdım ve neden

Her gün hem Angular hem .NET tarafında çalışıyorum, yani bu sınırın iki yanında da kod yazıyorum. Ama "bir kural frontend'de mi yazılmalı, backend'de mi?" sorusunu çoğu zaman alışkanlıkla cevaplıyorum. Backend gezegeninin ilk ek yazısında, bu ayrımın neden var olduğunu ve neyi belirlediğini düzgünce yazmak istedim.

## 2. Üç ana çıkarım

1. **Rol, makineyle değil konuşmadaki yerle belirlenir.** "Sunucu" büyük bir bilgisayar demek değil; bir isteği dinleyip cevap veren program demek. Aynı makine bir konuşmada sunucu, başka bir konuşmada istemci olabiliyor: .NET API'm tarayıcıya karşı sunucu, ama veritabanına ya da bir ödeme servisine istek atarken istemci. Kendi bilgisayarımda `ng serve` çalıştırdığımda da bir sunucu çalıştırmış oluyorum (geliştirme sunucusu).

   Bir web sayfası açıldığında kabaca şu oluyor:
   1. Tarayıcı (istemci) sunucudan HTML, CSS ve JavaScript dosyalarını ister.
   2. Angular uygulaması tarayıcıda çalışmaya başlar.
   3. Veri gerektiğinde Angular, `HttpClient` ile .NET API'ye bir HTTP isteği atar: `GET /api/posts`.
   4. API isteği doğrular, veritabanından veriyi çeker, JSON olarak döner.
   5. Angular bu JSON'u ekrana çizer.

   Bu bir **istek-cevap** (request-response) döngüsü. Sunucu istemciye kendiliğinden bir şey gönderemez; bunun için WebSocket ya da Server-Sent Events gibi ek yollar gerekiyor (SignalR bunları kullanıyor).

2. **İstemciye güvenme, çünkü istemci kullanıcının elinde.** Öğrendiğim en önemli kural bu. Tarayıcıda çalışan her şey kullanıcının bilgisayarında çalışıyor: DevTools'u açıp JavaScript'i değiştirebilir, butonu gizleyen `*ngIf`'i kaldırabilir, Postman ile API'ye istediği isteği doğrudan atabilir. Bu yüzden:
   - **Frontend doğrulaması kullanıcı deneyimi içindir** (anında "e-posta geçersiz" uyarısı).
   - **Backend doğrulaması güvenlik ve veri bütünlüğü içindir.** Aynı kural backend'de mutlaka tekrar edilir.
   - "Admin butonu sadece adminlere görünüyor" bir güvenlik önlemi değildir. API'deki `[Authorize(Roles = "Admin")]` güvenlik önlemidir.
   - Gizli bilgiler (API anahtarları, connection string) asla frontend koduna girmez. Angular'ın `environment.ts` dosyası derlendikten sonra herkesin okuyabileceği bir JavaScript dosyasına dönüşür.
   - Fiyat, indirim, stok gibi hesaplar sunucuda yapılır. İstemciden gelen "toplam: 10 TL" bilgisine güvenilmez.

3. **Ayrım, ölçekleme ve ekip yapısını da belirler.** Frontend ile backend'i ayırmak (SPA + API) şunları kazandırıyor: iki taraf ayrı ayrı deploy edilebiliyor, aynı API'yi web, mobil uygulama ve başka servisler kullanabiliyor, sunucu tarafı yatayda çoğaltılabiliyor. Bedeli de var: iki ayrı proje, API sözleşmesi yönetimi, CORS ayarları, ağ gecikmesi ve "veri gelene kadar ne gösterelim?" (yükleniyor durumları) sorusu.

   İyi bir sunucu genellikle **durumsuz** (stateless) tasarlanıyor: her istek, onu işlemek için gereken her şeyi (örneğin bir token) kendisi taşıyor ve sunucu istekler arasında kullanıcıya özel bir şey hatırlamıyor. Böylece aynı API'den on kopya çalıştırıp önüne bir yük dengeleyici koymak mümkün oluyor; hangi kopyanın cevap verdiği fark etmiyor. Durum (state) veritabanında, cache'te ya da istemcide tutuluyor.

   Tek doğru model de değil. **Sunucu tarafı render** (SSR) ile sayfa HTML'i sunucuda üretilebiliyor; Learning Sky sitem gibi **statik siteler** ise derleme anında bir kez üretilip dosya olarak sunuluyor ve çalışma anında hiç backend kodu yok. Hangisinin seçileceği yine bir mimari karar.

## 3. Neyi yanlış anladım ya da hâlâ belirsiz

- "Backend = sunucu, frontend = tarayıcı" eşleşmesini kesin sanıyordum. SSR ile Angular kodunun bir kısmı sunucuda da çalışabiliyor (Angular SSR), Node.js ile JavaScript backend yazılabiliyor. Ayrım kodun dilinde değil, nerede çalıştığında ve kime güvenildiğinde.
- Peer-to-peer (eşler arası) modelde, örneğin torrent ya da WebRTC görüntülü görüşmede, herkes hem istemci hem sunucu. Bunu şimdilik sadece adıyla biliyorum.
- "Thin client" ve "thick client" farkı: iş mantığının ne kadarının istemcide olacağı. Angular uygulamaları giderek kalınlaşıyor; bu sınırın nerede olması gerektiğini mimari yazılarında tekrar düşüneceğim.

## 4. Örnek

[`example/`](example/) klasöründe bağımlılığı olmayan, tek dosyalık bir Node.js örneği var: küçük bir HTTP sunucusu (`server.mjs`) ve ona istek atan bir istemci (`client.mjs`). İstemci üç istek atıyor: biri geçerli, biri toplam tutarı kendisi "1 TL" diye gönderen hileli bir istek (sunucu bunu yok sayıp fiyatı kendisi hesaplıyor), biri de sunucunun reddettiği negatif adetli bir istek. Örneğin amacı şu cümleyi göstermek: istemci ne gönderirse göndersin, son sözü sunucu söyler.

**Yapay zekâ notu:** Yapay zekâya bir form özelliği yazdırdığımda bazen doğrulamayı sadece Angular tarafına koyuyor ya da yetki kontrolünü sadece butonu gizleyerek yapıyor. Ürettiği kodda her zaman şunu soruyorum: "Bu kuralı biri Postman'den API'ye doğrudan istek atarak aşabilir mi?" Cevap evetse, kontrol sunucuya da girmeli. Ona da açıkça söylüyorum: "Doğrulamayı hem frontend'de hem backend'de yaz, backend'deki zorunlu."

## 5. Kaynakça

_Bu yazıda yararlandığım kaynaklar. Bağlantılara son erişim: 18 Kasım 2026._

- MDN Web Docs, "Client-Server overview". https://developer.mozilla.org/en-US/docs/Learn_web_development/Extensions/Server-side/First_steps/Client-Server_overview
- MDN Web Docs, "An overview of HTTP". https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Overview
- Roy T. Fielding. *Architectural Styles and the Design of Network-based Software Architectures* (2000), Bölüm 5: client-server ve stateless kısıtları.
- OWASP, "Input Validation Cheat Sheet" (istemci tarafı doğrulamanın güvenlik sağlamadığı üzerine). https://cheatsheetseries.owasp.org/cheatsheets/Input_Validation_Cheat_Sheet.html
