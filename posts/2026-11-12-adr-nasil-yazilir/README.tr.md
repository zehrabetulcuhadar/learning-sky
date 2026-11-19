[🇬🇧 English](README.en.md) | 🇹🇷 **Türkçe**

# Mimari karar kaydı (ADR) nasıl yazılır?

> *Zehra tarafından araştırıldı ve yazıldı. Yapay zekâ yardımıyla taslağı hazırlandı, ben gözden geçirdim.*

**Kısa cevap:** Mimari karar kaydı (Architecture Decision Record, ADR), **tek bir** önemli kararı anlatan kısa bir metin dosyasıdır. Klasik biçimi beş başlıktan oluşur: **Başlık, Durum, Bağlam, Karar, Sonuçlar.** Kodun yanında (örneğin `docs/adr/0001-...md`) tutulur, numaralanır ve bir kez kabul edildikten sonra değiştirilmez; karar değişirse yeni bir ADR yazılır ve eskisi "yerini aldı" olarak işaretlenir. Amacı, altı ay sonra gelen birinin (çoğu zaman kendimin) "bunu neden böyle yaptık?" sorusuna cevap bulabilmesi.

## 1. Neyi araştırdım ve neden

İlk mimari yazımda "mimari, değiştirmesi pahalı kararların toplamıdır" demiştim. Ama kararları nereye yazıyoruz? Çoğu zaman hiçbir yere. Karar bir toplantıda verilir, gerekçe katılanların kafasında kalır, onlar ayrılınca kaybolur. Sonra yeni gelen biri kodu görüp "bu neden bu kadar garip?" diye sorar ve ya kararı körü körüne korur ya da nedenini bilmeden bozar.

ADR bu sorunu çok basit bir araçla çözüyor: bir markdown dosyası. Bunu öğrenmek için en iyi yol kendi projemde denemekti, o yüzden sitemin ilk mimari kararını ADR olarak yazdım.

## 2. Üç ana çıkarım

1. **Beş başlık yeterli.** Michael Nygard'ın 2011'de önerdiği biçim hâlâ en yaygını:
   - **Başlık:** kısa bir isim cümlesi, numarayla. "0001. Kişisel site için statik site üretici olarak Astro kullan."
   - **Durum (Status):** Önerildi, Kabul edildi, Reddedildi, Kullanımdan kalktı ya da "0007 tarafından yerini aldı".
   - **Bağlam (Context):** Kararı zorlayan durum. Hangi problem var, hangi kısıtlar ve hangi güçler (bütçe, ekip bilgisi, süre, performans hedefi) birbiriyle çekişiyor? Burada tarafsız olmak gerekiyor; çözüm değil, durum anlatılır.
   - **Karar (Decision):** Etken çatıyla, net bir cümle. "Astro kullanacağız." "Belki", "düşünüyoruz" yok.
   - **Sonuçlar (Consequences):** Kararın getirdiği **her şey**, sadece iyiler değil. Neyi kolaylaştırıyor, neyi zorlaştırıyor, hangi yeni riskleri ve işleri doğuruyor?

   En çok işe yarayan kısım bence Sonuçlar. Bir kararın kötü taraflarını da yazmak, onu dürüst yapıyor ve gelecekte "bunu biliyorduk, bilerek seçtik" diyebilmeyi sağlıyor.

2. **ADR'ler değişmez, birbirinin yerini alır.** Bir ADR kabul edildikten sonra düzenlenmiyor. Altı ay sonra fikir değişirse 0007 numaralı yeni bir ADR yazılıyor, eski ADR'nin durumu "0007 tarafından yerini aldı" oluyor. Böylece kararların tarihi kayboluyor değil, birikiyor: neyi, ne zaman, hangi bilgiyle düşündüğümüz görünüyor. Git commit geçmişine benziyor, ama kod satırları değil kararlar için.

   Pratik kurallar:
   - Dosyalar kodun yanında: `docs/adr/0001-kisa-isim.md`. Kod incelemesinde (pull request) ADR de incelenebilir.
   - Bir ADR = bir karar. "Frontend, veritabanı ve deploy kararlarımız" diye tek dosya olmaz.
   - Kısa tutulur. Bir iki sayfayı geçiyorsa muhtemelen birden fazla karar var.
   - Sadece mimari açıdan önemli kararlar için. "Değişken adı" ADR olmaz; "hangi veritabanı", "monolit mi", "kimlik doğrulama nasıl" olur.

3. **Seçenekleri yazmak, kararı kendi kendine sorgulamaktır.** Nygard'ın biçiminde seçenekler bağlamın içinde geçiyor. MADR (Markdown Any Decision Records) gibi daha yeni şablonlar ise ayrı bir **"Değerlendirilen seçenekler"** bölümü ve her seçenek için artılar ve eksiler ekliyor. Kendi ADR'mi yazarken fark ettim: Astro'yu Angular, Next.js ve bir blog platformuyla yan yana yazmak zorunda kalınca, kararımın bir kısmının aslında "yeni bir şey öğrenmek istiyorum" isteğinden geldiğini gördüm. Bu da meşru bir gerekçe, ama artık açıkça yazılı.

## 3. Neyi yanlış anladım ya da hâlâ belirsiz

- ADR'yi büyük şirketlere özgü, ağır bir süreç sanıyordum. Aslında tek kişilik bir proje için bile beş dakikalık bir iş ve en çok da kendime faydası var.
- Hangi kararın ADR'yi "hak ettiği" hâlâ bir yargı meselesi. Şimdilik kuralım şu: "Bunu geri almak bir günden uzun sürerse ADR yaz."
- Kararlar yazıldıktan sonra gerçekten okunuyor mu? Araştırdığım kaynaklar, ADR'lerin en çok yeni gelen birine projeyi anlatırken ve bir kararı yeniden tartışırken işe yaradığını söylüyor. Bunu kendi projemde zamanla göreceğim.

## 4. Örnek

[`example/`](example/) klasöründe sitemin gerçek ilk ADR'si var: **"0001. Kişisel site için Astro kullan"**. Klasik beş başlığı ve ayrıca değerlendirilen seçenekleri içeriyor. Bir de boş şablon (`template.md`) koydum, yeni bir karar için kopyalanabilir.

**Yapay zekâ notu:** Yapay zekâ ADR taslağı yazmakta çok iyi, çünkü biçim çok net. Ama bağlamı ona vermem gerekiyor; vermezsem genel ve herkese uyan bir bağlam uyduruyor. İşe yarayan yol: kararı ve kısıtları birkaç maddeyle ben yazıyorum, ondan "Sonuçlar bölümünde olumsuz sonuçları da eksiksiz say" diye istiyorum. Olumsuz sonuçları bulmakta benden hızlı, ama hangisinin bu projede gerçekten önemli olduğuna ben karar veriyorum. Bir de ADR'leri bağlam dosyası olarak yapay zekâya vermek, ona "bu projede neden böyle yapıyoruz"u anlatmanın en kısa yolu.

## 5. Kaynakça

_Bu yazıda yararlandığım kaynaklar. Bağlantılara son erişim: 18 Kasım 2026._

- Michael Nygard. "Documenting Architecture Decisions" (2011). https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions
- ADR GitHub organizasyonu, şablonlar ve araçlar. https://adr.github.io/
- MADR, Markdown Any Decision Records. https://adr.github.io/madr/
- Joel Parker Henderson, "Architecture decision record" örnek koleksiyonu. https://github.com/joelparkerhenderson/architecture-decision-record
- ThoughtWorks Technology Radar, "Lightweight Architecture Decision Records" (Adopt).

---

© 2026 Zehra Betül Çuhadar. Bu yazının metni ve görselleri [CC BY-NC-ND 4.0](https://creativecommons.org/licenses/by-nc-nd/4.0/deed.tr) lisanslıdır: adımı ve bağlantıyı vererek, ticari olmayan amaçla ve değiştirmeden paylaşabilirsin. Kod örnekleri için tüm hakları saklıdır, bkz. [LICENSE-CODE](../../LICENSE-CODE).
