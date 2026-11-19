[🇬🇧 English](README.en.md) | 🇹🇷 **Türkçe**

# Yapay zekâ yazılımcının işini nasıl değiştiriyor?

> *Zehra tarafından araştırıldı ve yazıldı. Yapay zekâ yardımıyla taslağı hazırlandı, ben gözden geçirdim.*

**Kısa cevap:** Yapay zekâ, kod **yazmanın** maliyetini hızla düşürüyor; ama doğru kodu **seçmenin**, **doğrulamanın** ve **sistemin bütününe uydurmanın** maliyeti düşmüyor, hatta artıyor. Bu yüzden yazılımcının işi, satır satır kod üretmekten şunlara kayıyor: problemi net **tarif etmek** (spesifikasyon ve bağlam), üretilen kodu **incelemek ve test etmek**, mimari ve teknik **kararları vermek** ve sonuçların **sorumluluğunu almak**. Araştırmalar tablonun karışık olduğunu gösteriyor: yapay zekâ kullanımı neredeyse evrensel hale geldi, ama doğruluğuna güven düşük ve verimlilik kazancı her zaman hissedildiği kadar büyük değil.

## 1. Neyi araştırdım ve neden

Learning Sky'ın bütün çıkış noktası bu soru. Bilgisayarı en baştan öğrenmeye karar vermemin nedeni, yapay zekânın kodun büyük kısmını yazdığı bir dünyada **neyi bilmem gerektiğini** sorgulamamdı. Yapay zekâ gezegeninin bu ek yazısında kendi sezgimi verilerle karşılaştırmak istedim: gerçekten ne değişiyor, ne değişmiyor?

## 2. Üç ana çıkarım

1. **Kullanım evrensel, güven değil.** Stack Overflow'un 2025 geliştirici anketinde katılımcıların yaklaşık yüzde 84'ü yapay zekâ araçlarını kullandığını ya da kullanmayı planladığını söyledi. Ama aynı ankette yapay zekânın doğruluğuna **güvenmeyenlerin** oranı (yaklaşık yüzde 46), **güvenenlerden** (yaklaşık yüzde 33) daha yüksekti. En sık şikâyet de "neredeyse doğru ama tam değil" çözümlerdi. Bu benim deneyimimle de örtüşüyor: yapay zekânın yazdığı kod çoğu zaman çalışıyor gibi görünüyor, ama kenar durumlarda, projenin kurallarında ya da güncel API'lerde küçük hatalar barındırıyor. "Neredeyse doğru" kod, bariz yanlış koddan daha tehlikeli, çünkü fark etmesi daha zor.

2. **Hissedilen hız ile ölçülen hız farklı olabilir.** METR adlı araştırma kuruluşunun 2025'te yayımladığı randomize kontrollü bir çalışmada, kendi tanıdıkları büyük açık kaynak projelerinde çalışan deneyimli geliştiriciler, yapay zekâ araçlarını kullandıklarında görevleri ortalama yaklaşık yüzde 19 **daha yavaş** tamamladı. İlginç olan: aynı geliştiriciler, iş bittikten sonra bile yapay zekâ sayesinde yaklaşık yüzde 20 **hızlandıklarını** düşünüyordu. Bu tek bir çalışma ve belirli bir durumu ölçüyor (çok iyi bildikleri, karmaşık kod tabanları); başka çalışmalar daha basit ya da yeni görevlerde hızlanma buldu. Ama ders net: verimliliği hissimle değil, ölçerek değerlendirmeliyim. Google'ın DORA raporları da benzer bir uyarı yapıyor: 2024 raporunda yapay zekâ kullanımındaki artış, teslimat istikrarında küçük bir düşüşle birlikte görülmüştü; raporların vardığı sonuç, yapay zekânın iyi mühendislik pratiklerinin (küçük değişiklikler, güçlü testler, hızlı geri bildirim) yerine geçmediği, olanları **büyüttüğü**.

3. **Değeri artan beceriler: tarif etmek, yargılamak, karar vermek.** Okuduklarımdan ve kendi gözlemlerimden çıkardığım tablo:

   | Değeri azalan | Değeri artan |
   |---|---|
   | Sözdizimini ezbere bilmek | Problemi net tarif etmek (spesifikasyon, kabul kriterleri) |
   | Standart kodu (boilerplate) hızlı yazmak | Doğru bağlamı vermek (kurallar, örnekler, mimari kararlar) |
   | Bir API'nin parametrelerini hatırlamak | Kodu okuyup yargılamak: doğru mu, güvenli mi, gereksiz karmaşık mı? |
   | Tek başına bir fonksiyonu sıfırdan yazmak | Test yazmak ve doğrulamak |
   | | Mimari ve trade-off kararları |
   | | Temel bilgi: ağ, veritabanı, bellek, eşzamanlılık (yanlışı fark etmek için) |
   | | İletişim: ekiple, iş tarafıyla, yapay zekâyla |

   Burada bir paradoks var: yapay zekâ temel bilgiyi daha az değil, **daha çok** gerekli kılıyor. Bir sorgunun N+1 problemi olduğunu, bir `catch`'in hatayı yuttuğunu, bir CORS ayarının fazla geniş olduğunu fark edebilmek için o konuyu bilmek gerekiyor. Yapay zekâ "ne"yi yazabiliyor; "bu doğru mu?" sorusunu cevaplamak hâlâ benim işim. Learning Sky'daki bütün temel yazılar bu yüzden var.

   Bir de sorumluluk boyutu: kodu kim yazmış olursa olsun, onu onaylayıp canlıya gönderen benim. "Yapay zekâ yazdı" bir hata raporunda geçerli bir açıklama değil.

## 3. Neyi yanlış anladım ya da hâlâ belirsiz

- Başta "yapay zekâ yazılımcıların yerini alacak mı?" sorusuna evet ya da hayır cevabı arıyordum. Okudukça sorunun yanlış olduğunu düşünmeye başladım: iş kaybolmuyor gibi görünüyor ama içeriği değişiyor. Bu değişimin ne kadar hızlı olacağını, özellikle yeni başlayanlar (junior) için ne anlama geleceğini kimse kesin bilmiyor.
- Yeni başlayanlar için bir ikilem görüyorum: temel becerileri kazanmanın yolu, şimdi yapay zekânın yaptığı küçük işleri kendin yapmaktı. Yapay zekâ bunları yaparken temel nasıl öğrenilecek? Benim cevabım şimdilik Learning Sky: bilinçli olarak temelden öğrenmek, yapay zekâyı da öğretmen ve sparring partneri olarak kullanmak.
- Bu alan çok hızlı değişiyor. Bu yazıdaki rakamlar 2025 verileri; birkaç ay içinde eskiyebilirler.

## 4. Örnek

[`example/`](example/) klasöründe kendi yapay zekâ ile çalışma akışım var (`workflow.md`): bir özelliği yapay zekâya yaptırmadan önce yazdığım kısa spesifikasyon şablonu, çalışırken uyduğum kurallar ve kodu kabul etmeden önceki kontrol listem. Bu yazının "çalışan örneği" kod değil, bir süreç; çünkü değişen şey de kod değil, süreç.

**Yapay zekâ notu:** Bu yazıyı hazırlarken yapay zekâya "yapay zekâ yazılımcıların işini nasıl değiştiriyor?" diye sorduğumda bana iyimser ve genel bir tablo çizdi, rakamları da kaynaksız verdi. Bu yazıdaki her rakamı birincil kaynağından (anket raporu, araştırma makalesi) kontrol ettim. Konu yapay zekânın kendisi olunca bu kontrol daha da önemli.

## 5. Kaynakça

_Bu yazıda yararlandığım kaynaklar. Bağlantılara son erişim: 18 Kasım 2026._

- Stack Overflow, "2025 Developer Survey", AI bölümü. https://survey.stackoverflow.co/2025/
- METR. "Measuring the Impact of Early-2025 AI on Experienced Open-Source Developer Productivity" (Temmuz 2025). https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/
- Google Cloud, DORA "Accelerate State of DevOps Report 2024". https://dora.dev/research/2024/dora-report/
- Google Cloud, DORA "State of AI-assisted Software Development" (2025). https://dora.dev/
- Addy Osmani. *Beyond Vibe Coding*, O'Reilly, 2025.
