[🇬🇧 English](README.en.md) | 🇹🇷 **Türkçe**

# İyi bir commit mesajı İngilizce nasıl yazılır?

> *Zehra tarafından araştırıldı ve yazıldı. Yapay zekâ yardımıyla taslağı hazırlandı, ben gözden geçirdim.*

**Kısa cevap:** İyi bir commit mesajının başlığı en fazla 50 karakter civarındadır, **emir kipinde** yazılır ("Add", "Fix", "Remove"; "Added" ya da "Adding" değil), büyük harfle başlar ve sonunda nokta yoktur. Gerekirse bir boş satırdan sonra gelen gövde, **neyi ve neden** değiştirdiğini anlatır, nasıl yaptığını kod zaten gösterir. Pratik test: başlık "If applied, this commit will ..." cümlesini doğru tamamlamalı.

## 1. Neyi araştırdım ve neden

Learning Sky ve kişisel sitem için artık neredeyse her gün commit atıyorum ve mesajları İngilizce yazıyorum. Bir gün kendi geçmişime baktım: "update", "fix", "changes", "son hali". Altı ay sonra bunların hiçbiri bana bir şey anlatmayacak.

Commit mesajı aynı zamanda iş yerinde İngilizceyi en sık yazdığım yer. Kısa, kalıplı ve her gün tekrar ediyor. Yani hem Git alışkanlığı hem İngilizce pratiği için mükemmel bir başlangıç.

## 2. Üç ana çıkarım

1. **Başlık emir kipinde, çünkü Git de öyle konuşuyor.** Git kendi ürettiği mesajlarda emir kipi kullanıyor: `Merge branch 'main'`, `Revert "..."`. Topluluktaki yaygın kural da bu. Kontrol cümlesi: *"If applied, this commit will __"*.
   - ✅ `Add dark mode toggle to the header` → "...will add dark mode toggle" ✔
   - ❌ `Added dark mode toggle` → "...will added" ✘
   - ❌ `Adding dark mode` / `dark mode stuff` / `fix`

   Başlık için kurallar (Chris Beams'in çok alıntılanan "yedi kuralı"ndan): başlığı gövdeden boş satırla ayır, başlığı 50 karakter civarında tut, büyük harfle başla, sonuna nokta koyma, emir kipi kullan, gövdeyi 72 karakterde sar, gövdede "nasıl"ı değil "ne ve neden"i anlat.

2. **Gövde geleceğe yazılan bir not.** Kodun *ne* değiştiğini `git diff` gösterir. Göstermediği şey *neden*. Altı ay sonra `git blame` ile bir satıra gelen kişi (çoğu zaman ben) "bu neden böyle?" diye soracak. Gövde bu soruya cevap verir:

   ```
   Generate sky.json in CI instead of by hand

   Editing sky.json manually caused it to drift from the posts.
   The workflow now runs build_sky.py on every push, so meta.json
   is the single source of truth.
   ```

   İngilizce kalıplar işime yaradı: *"Previously, ..."*, *"This caused ..."*, *"Now ..."*, *"so that ..."*, *"Without this, ..."*. Bir de bağlantı: *"Closes #12"*, *"Refs #34"*.

3. **Conventional Commits bir seçenek, zorunluluk değil.** Birçok proje başlığa bir tür öneki koyuyor: `feat: add search box`, `fix: handle empty post list`, `docs: update README`, `refactor:`, `test:`, `chore:`. Bu biçim otomatik sürüm notu ve sürüm numarası üretmeyi kolaylaştırıyor. Dikkat ettiğim fark: Conventional Commits'te önekten sonra küçük harfle başlamak yaygın. Hangi kuralı seçersem seçeyim, önemli olan bir repoda **tutarlı** olmak.

## 3. Neyi yanlış anladım ya da hâlâ belirsiz

- Emir kipini kaba sanıyordum ("Add!" bağırmak gibi). Aslında bir komut değil, bir tarif: commit'in ne yapacağını anlatıyor.
- Sık yaptığım İngilizce hatalar: `Fixed bug` (geçmiş zaman), `Fix a bug` (hangi bug?), `Update files` (hangi dosyalar, neden?). Belirsiz fiiller yerine somut fiiller: `Rename`, `Extract`, `Replace`, `Prevent`, `Handle`, `Drop`.
- Her küçük commit'e gövde yazmak gerekiyor mu? Bence hayır. Tek satırlık değişiklikte iyi bir başlık yeter. Gövde, "neden" açık olmadığında gerekiyor. Bu sınırı hâlâ deneyerek buluyorum.

## 4. Örnek

[`example/`](example/) klasöründe küçük bir commit mesajı denetleyicisi var. Bir mesajı alıp şunlara bakıyor: başlık uzunluğu, büyük harf, sondaki nokta, geçmiş zaman ya da "-ing" ile başlayan fiil, başlıktan sonra boş satır. İstersen Git'in `commit-msg` hook'u olarak da kullanılabilir.

Sık kullandığım fiiller ve anlamları:

| Fiil | Ne zaman |
|---|---|
| Add | Yeni bir şey eklediğinde |
| Fix | Bir hatayı düzelttiğinde |
| Remove / Drop | Bir şeyi sildiğinde |
| Rename | Sadece ad değiştiğinde |
| Refactor / Extract | Davranış aynı, yapı değiştiğinde |
| Update / Bump | Bağımlılık ya da sürüm yükselttiğinde |
| Improve | Performans ya da okunabilirlik arttığında (ama neyi, söyle) |
| Revert | Önceki bir commit'i geri aldığında |

**Yapay zekâ notu:** Yapay zekâ araçları `git diff`'ten commit mesajı yazmakta iyi, ama genelde sadece *ne* değiştiğini sayıyor ("Update index.astro and add styles"). *Neden*'i bilmiyor, çünkü neden kafamda. Ona "Bu değişikliği şu sorunu çözmek için yaptım" diye bir cümle verince mesaj gerçekten işe yarar hale geliyor. Ürettiği başlığı yine "If applied, this commit will..." testinden geçiriyorum.

## 5. Kaynakça

_Bu yazıda yararlandığım kaynaklar. Bağlantılara son erişim: 18 Kasım 2026._

- Chris Beams. "How to Write a Git Commit Message". https://cbea.ms/git-commit/
- Conventional Commits 1.0.0. https://www.conventionalcommits.org/
- Pro Git, "Contributing to a Project: Commit Guidelines". https://git-scm.com/book/en/v2/Distributed-Git-Contributing-to-a-Project
- Tim Pope. "A Note About Git Commit Messages" (2008).

---

© 2026 Zehra Betül Çuhadar. Bu yazının metni ve görselleri [CC BY-NC-ND 4.0](https://creativecommons.org/licenses/by-nc-nd/4.0/deed.tr) lisanslıdır: adımı ve bağlantıyı vererek, ticari olmayan amaçla ve değiştirmeden paylaşabilirsin. Kod örnekleri için tüm hakları saklıdır, bkz. [LICENSE-CODE](../../LICENSE-CODE).
