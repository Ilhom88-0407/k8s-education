# Dars 325 — CKA imtihoni haqida ko'p so'raladigan savollar va maslahatlar

> 🎯 **Bu darsda nimani o'rganamiz:**
> - Imtihonga tayyor ekaningizni qanday bilish mumkin
> - Natijalar qachon keladi va necha foiz ball kerak
> - Imtihon muhitida avtomatik to'ldirish va klaster almashtirish qanday ishlaydi
> - Ro'yxatdan o'tishda chegirma kodlari

## Oddiy hayotiy o'xshatish: haydovchilik guvohnomasi

CKA imtihoni — bu haydovchilik guvohnomasi olishga o'xshaydi. Nazariy qoidalarni yodlab qo'yish yetarli emas — mashina rulini ushlab, chorrahada to'g'ri qaror qabul qila olishingiz kerak. Shuning uchun bu kursda shunchalik ko'p amaliy lab va mock imtihon bor: maqsad — sizni "rulda" qulay his qildirish, faqat qoidalarni yodlatish emas.

## ❓ Ko'p so'raladigan savollar

**Men haqiqiy imtihonga tayyormanmi?**

Agar kursdagi barcha darslar, lablar va mock imtihonlarni tugatgan bo'lsangiz — deyarli tayyorsiz. O'zingizni tekshirish uchun tasodifiy lab yoki mock imtihonni qayta ishlang: agar maslahatlarga yoki javob fayllariga qaramasdan tez va ishonchli yecha olsangiz, tayyor hisoblanasiz. Esda tuting: haqiqiy imtihonda o'tish uchun atigi **66%** ball kerak, va sizda bepul qayta topshirish huquqi ham bor. Shuning uchun ortiqcha xavotir olmasdan urinib ko'ring!

> Ro'yxatdan o'tish uchun [Linux Foundation'ning rasmiy sahifasiga](https://training.linuxfoundation.org/certification/certified-kubernetes-administrator-cka/) o'ting. Ro'yxatdan o'tishda **30KK** kodini kiriting — bu CKA imtihoni narxidan 30% chegirma beradi.

**Natijalar qachon keladi?**

Imtihon natijalari elektron pochtaga **48 soat ichida** yuboriladi.

**Ushbu kurs va mock imtihonlar imtihon uchun yetarlimi?**

Ha! Kurs imtihon uchun zarur bo'lgan barcha mavzularni qamrab oladi. Agar amaliy testlar va mock imtihonlarni yetarlicha mashq qilib, Kubernetes rasmiy hujjatlari bilan "til topishsangiz" — tayyor bo'lasiz.

**Mock imtihonlarning qiyinlik darajasi haqiqiy imtihonga o'xshaydimi?**

Kursga qiyinlik darajasi haqiqiy imtihonga yaqinroq bo'lgan 2 ta yangi mock imtihon (2 va 3) qo'shilgan. Ularni albatta ishlab chiqing.

**Imtihon muhitida avtomatik to'ldirish (autocomplete) ishlaydimi?**

Ha, ishlaydi. Shuning uchun `kubectl` buyruqlarini avtomatik to'ldirish bilan mashq qilib boring.

**Imtihonda bir nechta klaster/kontekst orasida qanday almashaman?**

Har bir savol boshida qaysi klaster/kontekstga o'tish kerakligi ko'rsatilgan buyruq beriladi. **Har doim** shu buyruqni ishga tushiring — hatto to'g'ri klasterda turganingizga ishonchingiz komil bo'lsa ham! Bu imtihonda eng ko'p ball yo'qotiladigan joylardan biri: noto'g'ri klasterda ishlagan javob hisoblanmaydi.

Ko'proq savol-javoblarni [CNCF rasmiy FAQ sahifasidan](https://www.cncf.io/certification/cka/faq/) topishingiz mumkin.

## 📌 Rasmiy imtihon maslahatlari

Linux Foundation'ning o'zi tavsiya qiladigan rasmiy maslahatlar bilan [bu sahifada](https://docs.linuxfoundation.org/tc-docs/certification/tips-cka-and-ckad) tanishib chiqing — vaqtni boshqarish, muhitni sozlash va imtihon qoidalari haqida foydali tavsiyalar bor.

## 📖 Mock imtihonlar haqida muhim eslatma

Mock imtihonlar (KodeKloud tomonidan tayyorlangan) hali sinov bosqichida bo'lgani uchun quyidagilarni yodda tuting:

| Eslatma | Nima degani |
|---|---|
| Bu haqiqiy imtihonning nusxasi emas | Savollar formati sal boshqacha bo'lishi mumkin |
| Savollar aynan bir xil emas | Haqiqiy imtihonda boshqa savollar chiqadi |
| Interfeys bir xil emas | Haqiqiy imtihon muhiti boshqacha ko'rinishda |
| Baholash tizimi farq qilishi mumkin | Ball hisoblash usuli aynan mos kelmasligi mumkin |
| Qiyinlik darajasi farq qilishi mumkin | Ba'zi savollar osonroq yoki qiyinroq bo'lishi mumkin |

Shunga qaramay, mock imtihonlar sizga savolni o'qish va tushunish, o'z ishingizni tekshirish va vaqtni boshqarish ko'nikmalarini mashq qilish uchun juda foydali.

## 🔗 Manbalar

- [CNCF — CKA FAQ](https://www.cncf.io/certification/cka/faq/)
- [Linux Foundation — CKA imtihoniga ro'yxatdan o'tish](https://training.linuxfoundation.org/certification/certified-kubernetes-administrator-cka/)
- [Rasmiy imtihon maslahatlari (CKA va CKAD)](https://docs.linuxfoundation.org/tc-docs/certification/tips-cka-and-ckad)
- [KodeKloud Mock Test havolasi](https://uklabs.kodekloud.com/topic/mock-exam-1-4/)

---
*Bu dars KodeKloud CKA kursining 325, 326 va 329-materiallari asosida tayyorlandi.*
