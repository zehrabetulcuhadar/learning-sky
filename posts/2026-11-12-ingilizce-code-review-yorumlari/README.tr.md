[🇬🇧 English](README.en.md) | 🇹🇷 **Türkçe**

# Code review yorumları İngilizce nasıl yazılır? Kibar ve net kalıplar

> *Zehra tarafından araştırıldı ve yazıldı. Yapay zekâ yardımıyla taslağı hazırlandı, ben gözden geçirdim.*

**Kısa cevap:** İyi bir İngilizce code review yorumu üç şey yapar: **kodu konuşur, kişiyi değil** ("you did" yerine "this function does"), **ne kadar önemli olduğunu belirtir** (engel mi, öneri mi, küçük bir not mu) ve **nedenini söyler**. Soru biçimi ("What do you think about...?", "Could we...?") emir biçiminden daha yumuşak durur ama belirsizleşmemelidir. Etiketli yorum biçimi (`suggestion:`, `issue:`, `nit:`) bu üçünü tek satırda halletmeyi kolaylaştırır.

## 1. Neyi araştırdım ve neden

Code review, İngilizcenin en hassas olduğu yer. Commit mesajı sadece makineye ve geleceğe yazılıyor; review yorumu ise bir insana, onun emeğine yazılıyor. Türkçede doğal gelen dolaysızlık İngilizce yazıda sert okunabiliyor, ya da tam tersi, fazla kibarlık yüzünden "bu bir öneri mi, zorunlu mu?" anlaşılmıyor.

Bir de yapay zekâ çağında review yapmak daha önemli hale geldi: kodun büyük kısmını yapay zekâ yazıyorsa, insanın işi giderek "okumak ve yorum yazmak" oluyor. Bu yüzden İngilizce gezegeninin ikinci ek yazısını buna ayırdım.

## 2. Üç ana çıkarım

1. **Kodu konuş, kişiyi değil.** Aynı geri bildirim, öznesi değişince bambaşka okunuyor:
   - ❌ *"You forgot to handle null here."* → suçlayıcı
   - ✅ *"This will throw if `user` is null. Should we add a guard?"* → kodun davranışı + öneri
   - ❌ *"Why did you do it this way?"* → savunmaya iter
   - ✅ *"Can you help me understand why we chose a loop here instead of LINQ?"* → merak
   - ❌ *"This is wrong."*
   - ✅ *"I think this returns the previous value, not the updated one. Am I missing something?"*

   "We" kullanmak ("Could we...?", "Should we...?") kodun ortak olduğunu hissettiriyor. "I think" ve "I'm not sure, but" ise yorumun bir görüş olduğunu, kesin hüküm olmadığını gösteriyor.

2. **Ağırlığı belirt.** Kibarlık belirsizliğe dönüşünce karşı taraf her yorumu ya zorunlu sanıyor ya da hepsini görmezden geliyor. Çözüm, yorumun ne kadar önemli olduğunu açıkça söylemek. **Conventional Comments** bunu etiketlerle yapıyor:
   - `praise:` iyi bir şeyi takdir etmek. *"praise: Nice use of `switchMap` here, it cancels the old request."*
   - `nitpick:` ya da `nit:` önemsiz, isteğe bağlı. *"nit: Typo in the variable name (`recieve`)."*
   - `suggestion:` önerilen bir iyileştirme. *"suggestion: We could extract this into a pipe so the template stays simple."*
   - `issue:` gerçek bir sorun. *"issue: This query runs inside the loop, so it will hit the database once per item."*
   - `question:` emin olmadığın bir şey. *"question: Is this endpoint called by anything else?"*
   - `thought:` engel değil, fikir.
   - Ek süsleyiciler: `(blocking)`, `(non-blocking)`. *"suggestion (non-blocking): ..."*

   Google'ın review rehberi de aynı şeyi söylüyor: zorunlu olmayan yorumları "Nit:" ya da "Optional:" ile işaretle.

3. **Nedenini ve bir yol söyle.** "Bunu değiştir" demek yetmiyor, "neden" ve mümkünse "nasıl" gerekiyor. Benim şablonum: **gözlem → etki → öneri.**
   - *"This subscription is never unsubscribed (gözlem), so it will leak when the component is destroyed (etki). We could use `takeUntilDestroyed()` here (öneri)."*

   Kullandığım kalıplar:
   - *"Have you considered ...?"*, *"What do you think about ...?"*, *"Would it make sense to ...?"*
   - *"It might be worth ..."*, *"One option could be ..."*
   - *"I'd suggest ..."*, *"I'd prefer ... because ..."*
   - *"This looks good to me"* (LGTM), *"Approving with a couple of nits."*
   - Kabul ederken: *"Good catch, fixed in abc123."*, *"Done."*, *"Thanks, updated."*
   - Katılmazken: *"I see your point, but I'd keep it because ... What do you think?"*

## 3. Neyi yanlış anladım ya da hâlâ belirsiz

- "Please" eklemenin her şeyi kibar yaptığını sanıyordum. "Please fix this." hâlâ emir. Soru biçimi ve gerekçe, "please"den daha çok iş görüyor.
- Fazla yumuşatmak da sorun: *"Maybe, if you have time, it could possibly be nice to..."* ne istediğimi gizliyor. Gerçek bir hata varsa net olmak, kaba olmak değil.
- Kültürden kültüre değişiyor. Bazı ekipler doğrudanlığı tercih ediyor, bazıları dolaylılığı. Yeni bir ekipte önce eski review yorumlarını okuyup tonu anlamak iyi bir fikir gibi görünüyor.

## 4. Örnek

[`example/`](example/) klasöründe küçük bir Angular component'ine yazılmış review yorumları var: her biri önce "kötü" haliyle, sonra etiketli ve gerekçeli "iyi" haliyle. Bir de cebimde tuttuğum ifade bankası (`phrase-bank.md`).

**Yapay zekâ notu:** Yapay zekâ, Türkçe düşündüğüm bir yorumu İngilizceye çevirip tonunu yumuşatmakta çok iyi. "Bu yorumu kibar ama net yap, Conventional Comments etiketi ekle" diye istiyorum. Dikkat ettiğim şey: bazen fazla kibarlaştırıp asıl sorunu siliyor ya da teknik detayı değiştiriyor. Çıkan yorumu gönderemeden önce "teknik olarak hâlâ aynı şeyi mi söylüyor?" diye kontrol ediyorum.

## 5. Kaynakça

_Bu yazıda yararlandığım kaynaklar. Bağlantılara son erişim: 18 Kasım 2026._

- Conventional Comments. https://conventionalcomments.org/
- Google Engineering Practices, "How to write code review comments". https://google.github.io/eng-practices/review/reviewer/comments.html
- Michael Lynch. "How to Do Code Reviews Like a Human". https://mtlynch.io/human-code-reviews-1/
- Erin Meyer. *The Culture Map*, doğrudan ve dolaylı geri bildirim üzerine.

---

© 2026 Zehra Betül Çuhadar. Bu yazının metni ve görselleri [CC BY-NC-ND 4.0](https://creativecommons.org/licenses/by-nc-nd/4.0/deed.tr) lisanslıdır: adımı ve bağlantıyı vererek, ticari olmayan amaçla ve değiştirmeden paylaşabilirsin. Kod örnekleri için tüm hakları saklıdır, bkz. [LICENSE-CODE](../../LICENSE-CODE).
