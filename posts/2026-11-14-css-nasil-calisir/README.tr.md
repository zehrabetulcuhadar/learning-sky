[🇬🇧 English](README.en.md) | 🇹🇷 **Türkçe**

# CSS nasıl çalışır? Kaskad, özgüllük, Flexbox ve Grid

> *Zehra tarafından araştırıldı ve yazıldı. Yapay zekâ yardımıyla taslağı hazırlandı, ben gözden geçirdim.*

**Kısa cevap:** CSS, HTML elemanlarına **kurallar** (seçici + özellikler) uygular. Bir elemana aynı özellik için birden fazla kural uyduğunda hangisinin kazanacağını **kaskad** (cascade) belirler: önce kaynağa ve `!important`'a, sonra **katmana** (`@layer`), sonra **özgüllüğe** (specificity: id > class > etiket), en son da **sıraya** (sonra yazılan kazanır) bakılır. Bazı özellikler (yazı tipi, renk) ebeveynden çocuğa **kalıtılır**. Sayfa düzeni için iki modern araç var: tek eksende (satır ya da sütun) dizilim için **Flexbox**, satır ve sütunları birlikte yöneten iki boyutlu düzen için **Grid**.

## 1. Neyi araştırdım ve neden

Angular'da her component'in bir stil dosyası var ve çoğu zaman CSS'i deneme yanılmayla yazdığımı itiraf etmeliyim: bir şey çalışmayınca `!important` eklemek, sonra bir `div` daha sarmak. Kişisel sitemi yaparken bu yaklaşımın sınırına geldim: kartlar, gezegen çekmeceleri, telefon düzeni... CSS'in "neden bu kural kazandı?" sorusuna mantıklı bir cevabı olduğunu öğrenmek istedim.

## 2. Üç ana çıkarım

1. **Kaskad bir sıralama algoritması.** "Cascading Style Sheets" adındaki "kaskad" kelimesi tam olarak bu: bir özellik için yarışan kurallar şu sırayla elenir:
   1. **Köken ve önem:** tarayıcının varsayılanları < benim stillerim; `!important` bu sırayı tersine çeviriyor.
   2. **Katman (`@layer`):** katmanlara ayrılmış stillerde sonra tanımlanan katman kazanır, katmansız stiller hepsini yener.
   3. **Özgüllük:** daha "spesifik" seçici kazanır.
   4. **Sıra:** her şey eşitse dosyada sonra gelen kazanır.

   **Özgüllük** üç sayı gibi hesaplanıyor: `(id sayısı, class/öznitelik/pseudo-class sayısı, etiket sayısı)`.
   - `p` → (0, 0, 1)
   - `.card p` → (0, 1, 1)
   - `#header .title` → (1, 1, 0)
   - `style="..."` satır içi stil hepsinden güçlü, `!important` ondan da.

   Soldan sağa karşılaştırılıyor: tek bir id, on class'tan güçlü. `:is()` ve `:not()` içlerindeki en spesifik seçicinin değerini alıyor, `:where()` ise her zaman sıfır. Bu yüzden `:where()` varsayılan stiller yazmak için çok kullanışlı; üzerine yazmak kolay oluyor.

   Benim için asıl ders: `!important` bir çözüm değil, bir özgüllük savaşının başlangıcı. Sorun genelde seçicilerin gereksiz spesifik olması.

2. **Her şey bir kutu; düzen, kutuların nasıl dizildiği.** Her eleman bir **kutu modeli**: içerik + `padding` + `border` + `margin`. Klasik tuzak: `width: 200px` verip `padding` ekleyince kutunun 200 pikselden geniş olması. Çözüm neredeyse her projede ilk satırda: `*, *::before, *::after { box-sizing: border-box; }`. Böylece `width` kenarlığı ve iç boşluğu da kapsıyor.

   Kalıtım da kafa karıştırıyor: `color`, `font-family`, `line-height` gibi metin özellikleri çocuklara geçiyor; `margin`, `border`, `width` geçmiyor. `inherit`, `initial` ve `unset` anahtar kelimeleri bu davranışı elle değiştirmeyi sağlıyor.

   Angular burada bir şey daha ekliyor: **görünüm kapsülleme** (view encapsulation). Varsayılan modda Angular component'in stillerine `_ngcontent-xxx` gibi öznitelikler ekleyerek onları sadece o component'e uyguluyor. Bu da özgüllüğü bir öznitelik seçici kadar artırıyor. Global stillerin component içinde neden bazen işe yaramadığını bu açıklıyor.

3. **Tek eksen için Flexbox, iki eksen için Grid.**
   - **Flexbox** öğeleri tek bir eksende diziyor: bir navigasyon menüsü, bir buton grubu, ikon + metin. Ana eksende `justify-content`, çapraz eksende `align-items`; öğelerin büyüyüp küçülmesi `flex: 1` gibi değerlerle. Yıllarca zor olan "bir şeyi dikey ortala" işi artık üç satır: `display: flex; align-items: center; justify-content: center;`.
   - **Grid** satırları ve sütunları birlikte tanımlıyor: sayfa iskeleti, kart galerisi, form düzeni. `grid-template-columns: repeat(auto-fill, minmax(220px, 1fr))` tek satırla, ekran genişledikçe kendiliğinden sütun ekleyen bir galeri kuruyor, medya sorgusu yazmadan. `grid-template-areas` ile düzeni neredeyse bir çizim gibi yazmak mümkün.
   - İkisi rakip değil, birlikte kullanılıyor: sayfa iskeleti Grid, her kartın içindeki başlık ve buton satırı Flexbox.

   Bir de `gap` özelliği: öğeler arasına boşluk koymak için artık `margin` hilelerine gerek yok, hem Flexbox hem Grid'de çalışıyor.

## 3. Neyi yanlış anladım ya da hâlâ belirsiz

- Özgüllüğü "daha uzun seçici kazanır" diye düşünüyordum. Değil: `div div div div p` (0,0,5), tek bir `.x` (0,1,0) karşısında kaybediyor.
- `margin` çökmesi (margin collapse): alt alta iki bloğun dikey margin'leri toplanmıyor, büyük olan kazanıyor. Hâlâ bazen şaşırıyorum. Flex ve grid kapsayıcılarının içinde bu çökme olmuyor, bu da biraz rahatlatıcı.
- Container queries (`@container`) ile bir component'in ekrana değil, kendi kapsayıcısının genişliğine göre stil alabileceğini öğrendim. Angular component'leri için çok mantıklı görünüyor, ama henüz bir projede denemedim.
- `@layer` yeni ve güçlü görünüyor, ama mevcut büyük bir projeye nasıl eklenir, emin değilim.

## 4. Örnek

[`example/index.html`](example/index.html) tek bir HTML dosyası, tarayıcıda açmak yeterli. Üç bölümü var:
1. **Özgüllük yarışı:** aynı paragrafa dört kural uyuyor; hangisinin neden kazandığı yanında yazıyor.
2. **Flexbox:** bir menü çubuğu ve tam ortalanmış bir kutu.
3. **Grid:** pencereyi daralttıkça sütun sayısı kendiliğinden azalan bir kart galerisi, medya sorgusu olmadan.

**Yapay zekâ notu:** Yapay zekâ CSS'i çok hızlı yazıyor ama bir sorun çıkınca genelde `!important` ekliyor ya da bir sarmalayıcı `div` daha öneriyor; yani benim eski deneme yanılma alışkanlığımı tekrarlıyor. Daha iyi soru: "Bu kural neden uygulanmıyor? Kaskadda hangi kural onu yeniyor, özgüllük değerleri ne?" Bir de eski teknikler öneriyor olabilir (float ile düzen, ortalama için `position` hileleri); "Flexbox ya da Grid ile, modern CSS kullanarak" demek işe yarıyor. Son kontrol her zaman DevTools'taki Styles panelinde: üstü çizili kural, kaybeden kuraldır.

## 5. Kaynakça

_Bu yazıda yararlandığım kaynaklar. Bağlantılara son erişim: 18 Kasım 2026._

- MDN Web Docs, "Cascade, specificity, and inheritance". https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Styling_basics/Handling_conflicts
- MDN Web Docs, "Specificity". https://developer.mozilla.org/en-US/docs/Web/CSS/Specificity
- MDN Web Docs, "Flexbox" ve "CSS grid layout". https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_grid_layout
- web.dev, "Learn CSS" kursu. https://web.dev/learn/css
- Angular Docs, "Styling components" (view encapsulation). https://angular.dev/guide/components/styling

---

© 2026 Zehra Betül Çuhadar. Bu yazının metni ve görselleri [CC BY-NC-ND 4.0](https://creativecommons.org/licenses/by-nc-nd/4.0/deed.tr) lisanslıdır: adımı ve bağlantıyı vererek, ticari olmayan amaçla ve değiştirmeden paylaşabilirsin. Kod örnekleri için tüm hakları saklıdır, bkz. [LICENSE-CODE](../../LICENSE-CODE).
