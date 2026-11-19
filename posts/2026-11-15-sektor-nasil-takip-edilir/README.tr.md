[🇬🇧 English](README.en.md) | 🇹🇷 **Türkçe**

# Yazılım sektörü nasıl takip edilir? Haftalık okuma rutinim

> *Zehra tarafından araştırıldı ve yazıldı. Yapay zekâ yardımıyla taslağı hazırlandı, ben gözden geçirdim.*

**Kısa cevap:** Yazılım dünyasını takip etmenin yolu her şeyi okumak değil, **az sayıda güvenilir kaynağı**, **sabit bir zamanda** ve bir **filtreyle** okumak. Benim düzenim üç katmanlı: her gün 10 dakikalık bir özet (günlük bülten), haftada bir 30-45 dakikalık derin okuma (kullandığım araçların resmî blogları ve sürüm notları, bir iki seçilmiş bülten) ve ayda bir "ne öğrendim" notu (Learning Sky'daki haber yazıları). Filtre ise tek soru: **"Bu, önümüzdeki 6 ayda işimi ya da öğrenme planımı değiştirir mi?"** Cevap hayırsa başlığı okuyup geçiyorum.

## 1. Neyi araştırdım ve neden

Learning Sky'ın bir gezegeni haberlere ayrılmış, her dört haftada bir aylık özet yazıyorum. Ama ilk özetleri hazırlarken asıl sorunun haber bulmak değil, **haberde boğulmamak** olduğunu fark ettim. Her gün yeni bir yapay zekâ modeli, yeni bir framework sürümü, yeni bir "artık X öldü" yazısı çıkıyor. Hepsini takip etmeye çalışmak hem yorucu hem de öğrenme planımı sürekli dağıtıyor. Bu yazıda kendime bir rutin kurdum.

## 2. Üç ana çıkarım

1. **Kaynakları güvenilirliğe göre katmanla.** Her kaynak aynı değerde değil:
   - **Birincil kaynaklar (en güvenilir):** kullandığım araçların resmî blogları ve sürüm notları. Benim için: .NET Blog, Angular Blog, TypeScript sürüm notları, GitHub Changelog, kullandığım yapay zekâ araçlarının resmî duyuruları. Bir özelliğin gerçekten ne yaptığını burada okuyorum.
   - **Seçilmiş ikincil kaynaklar:** bir editörün süzdüğü bültenler ve yayınlar (InfoQ, ThoughtWorks Technology Radar, haftalık JavaScript ya da .NET bültenleri). Radar özellikle değerli: teknolojileri "Adopt, Trial, Assess, Hold" diye sınıflandırıyor ve yılda iki kez çıkıyor, yani gürültü az.
   - **Topluluk (en gürültülü):** Hacker News, Reddit, X, LinkedIn. Erken sinyal için iyi, ama doğruluk için değil. Buradan duyduğum bir şeyi birincil kaynaktan doğrulamadan "öğrendim" saymıyorum.
   - **Olay sonrası raporlar (postmortem):** büyük kesintilerden sonra şirketlerin yayımladığı teknik raporlar. Sektördeki en öğretici metinlerden bazıları bunlar, çünkü gerçek sistemlerin gerçek hatalarla nasıl çöktüğünü anlatıyorlar.

2. **Sabit zaman, sabit kutu: bir rutin bir akıştan iyidir.** Haberleri gün içinde rastgele okumak, dikkati sürekli bölüyor. Benim denediğim düzen:
   - **Her gün (10 dk):** sabah bülteni. Sadece başlıklar ve iki üç cümlelik özetler. Amaç "ne oluyor?" sorusuna genel bir cevap.
   - **Haftada bir (30-45 dk, cuma öğleden sonra):** RSS okuyucudaki birincil kaynaklar. Bu hafta kullandığım araçlarda ne değişti? Bir şeyi derinlemesine okumaya değer mi? Değerse "okuma listesi"ne ekliyorum.
   - **Ayda bir:** haber yazısı. Ayın en önemli 3-5 gelişmesini kendi cümlelerimle yazmak, haberi gerçekten anlayıp anlamadığımı test ediyor.
   - **Bildirimler kapalı.** Haber bana gelmiyor, ben belirlediğim zamanda habere gidiyorum.

   RSS burada çok işe yarıyor: algoritma yok, sadece seçtiğim kaynaklar, kronolojik sırayla. Bir RSS okuyucu (ya da küçük bir script) ile birincil kaynakları tek yerde topluyorum.

3. **Hype filtresi: "Bu beni ne kadar etkiler?"** Her habere aynı soruları soruyorum:
   - **Kullandığım bir şeyi mi etkiliyor?** (.NET, Angular, TypeScript, kullandığım yapay zekâ araçları) → Detaylı oku.
   - **Öğrenme planımdaki bir konuyla mı ilgili?** → Not al, o ders geldiğinde dön.
   - **Sadece yeni ve heyecan verici mi?** → Başlığı oku, geç. Gerçekten önemliyse altı ay sonra hâlâ konuşuluyor olacak.
   - **"X öldü" ya da "her şeyi değiştirecek" diyor mu?** → Şüpheyle yaklaş, birincil kaynağı ara.

   Bir de "FOMO"ya (bir şeyi kaçırma korkusu) karşı kendime hatırlattığım şey: temel bilgi (ağ, veritabanı, mimari) yavaş değişiyor, araçlar hızlı. Temeli öğrenmek, araç haberlerini anlamayı da kolaylaştırıyor.

## 3. Neyi yanlış anladım ya da hâlâ belirsiz

- Ne kadar çok kaynak takip edersem o kadar iyi bilgilendirileceğimi sanıyordum. Tersi oldu: kaynak sayısı arttıkça okuduğumu anlama oranım düştü. Şimdi kaynak eklerken bir tane çıkarmaya çalışıyorum.
- Yapay zekâ alanı o kadar hızlı ki haftalık rutin bile yetmiyor gibi hissettiriyor. Ama "her şeyi bilmek" zaten hedefim değil. Hedefim, işime yarayanı zamanında fark etmek.
- Türkçe kaynak tarafında hâlâ eksiğim var. Takip etmeye değer Türkçe teknik bültenler ve topluluklar arıyorum.

## 4. Örnek

[`example/`](example/) klasöründe standart kütüphaneyle yazılmış küçük bir Python RSS okuyucusu var. `feeds.txt` dosyasındaki kaynaklardan son 7 günün yazılarını çekip tarih sırasıyla listeliyor. Hem RSS hem Atom biçimini okuyor ve ulaşamadığı kaynağı atlayıp devam ediyor. Haftalık okuma saatimde bunu çalıştırıyorum; algoritma yok, sadece seçtiğim kaynaklar.

**Yapay zekâ notu:** Yapay zekâya "bu hafta yazılım dünyasında ne oldu?" diye sormak riskli: modelin bilgi kesim tarihi var ve web araması yapmıyorsa eski bilgiyi güncelmiş gibi anlatabiliyor. Web araması yapan araçlarda bile kaynak bağlantılarını açıp kontrol ediyorum. En iyi kullanım şekli bence şu: uzun bir sürüm notunu ya da postmortem raporunu ona verip "bir Angular/.NET geliştiricisini etkileyen kısımları özetle" demek. Yani haberi o bulmuyor, ben buluyorum; o sadece özetliyor.

## 5. Kaynakça

_Bu yazıda yararlandığım kaynaklar. Bağlantılara son erişim: 18 Kasım 2026._

- ThoughtWorks Technology Radar. https://www.thoughtworks.com/radar
- InfoQ. https://www.infoq.com/
- .NET Blog. https://devblogs.microsoft.com/dotnet/
- Angular Blog. https://blog.angular.dev/
- GitHub Changelog. https://github.blog/changelog/
- Cal Newport. *Deep Work*, 2016 (dikkat ve sabit zaman blokları üzerine).

---

© 2026 Zehra Betül Çuhadar. Bu yazının metni ve görselleri [CC BY-NC-ND 4.0](https://creativecommons.org/licenses/by-nc-nd/4.0/deed.tr) lisanslıdır: adımı ve bağlantıyı vererek, ticari olmayan amaçla ve değiştirmeden paylaşabilirsin. Kod örnekleri için tüm hakları saklıdır, bkz. [LICENSE-CODE](../../LICENSE-CODE).
