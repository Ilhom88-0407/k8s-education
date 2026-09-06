# Dars 327 — Kurs xulosasi (Bonus Lecture — Conclusion)

> 🎯 **Bu darsda nimani o'rganamiz:**
> - Kurs davomida bosib o'tilgan yo'lning sarhisobi
> - Imtihon oldidan qo'shimcha amaliyot manbalari (Ultimate CKA Mock Exam seriyasi)
> - CKA'dan keyingi sertifikatlar: CKS va KCNA

## Hayotiy o'xshatish: marafon marrasi

CKA kursi — uzoq marafon edi. Siz start chizig'ida "Pod nima?" deb boshlagan bo'lsangiz, endi marraga klaster quradigan, buzilganini tuzata oladigan administrator bo'lib yetib keldingiz. Marradan keyin sportchi nima qiladi? Natijasini mustahkamlaydi va keyingi musobaqaga (imtihonga!) tayyorgarlikni boshlaydi. Bu dars — ana shu marradagi qisqa "sovrin topshirish marosimi".

## Nimalarni o'rganib chiqdik?

Bu ajoyib o'quv safari yakuniga yetdi. Kurs davomida siz CKA imtihonining barcha bilim sohalarini bosib o'tdingiz:

```mermaid
graph TB
    A["CKA kursi"] --> B["Klaster arxitekturasi, o'rnatish va texnik xizmat"]
    A --> C["Workload va Scheduling - Deployment, Scheduler, Taints, Affinity"]
    A --> D["Services va Networking - Service, DNS, Ingress, CNI"]
    A --> E["Storage - Volume, PV, PVC, StorageClass"]
    A --> F["Troubleshooting - ilova, control plane, node, tarmoq"]
    B --> G["Amaliyot - labs, Lightning Labs, mock imtihonlar"]
    C --> G
    D --> G
    E --> G
    F --> G
    G --> H["CKA imtihoniga tayyor administrator"]
```

Muallifning tilaklari sodda va samimiy: imtihonga tayyorgarlikda omad, mehnat va intilish — muvaffaqiyat kaliti. Sertifikatni qo'lga kiritganingizda esa jamoa bilan quvonchni baham ko'rish uchun ijtimoiy tarmoqlarda ulashishingiz va kurs jamoasini belgilashingiz (tag qilishingiz) so'raladi.

## Qo'shimcha amaliyot: Ultimate CKA Mock Exam seriyasi

Imtihondan oldin **ko'proq amaliyot** xohlasangiz, KodeKloud'da yaqinda chiqarilgan **Ultimate CKA Mock Exam** seriyasi tavsiya qilinadi:

- haqiqiy imtihon muhitiga juda yaqin qilib qurilgan: **bir nechta klaster** va imtihon uslubidagi savollar;
- kursning ichidagi mock imtihonlarga ajoyib qo'shimcha;
- katta lab infratuzilmasi talab qilgani uchun faqat KodeKloud saytida, **pullik obuna** bilan ochiladi.

## Keyingi sertifikatlar va kurslar

| Yo'nalish | Nima beradi |
|---|---|
| **CKS** (Certified Kubernetes Security Specialist) | CKA'dan keyingi tabiiy qadam — Kubernetes xavfsizligi; KodeKloud'dagi kurs barcha mavzular, hands-on lab va mock imtihonlar bilan |
| **KCNA** (Kubernetes and Cloud Native Associate) | Boshlang'ich darajadagi sertifikat uchun tayyorlov kursi |
| Linux learning path | Mutlaq boshlovchidan sertifikatlangan Linux mutaxassisigacha, amaliy uslubda |
| Cloud learning paths | Mashhur cloud platformalar asoslari, sertifikatlar va servislarga chuqur kirish |

Bulardan tashqari KodeKloud'da Udemy'da yo'q 40+ kurs bor, yil davomida yana 50+ kurs (Linux, DevOps, cloud) rejalashtirilgan. **KodeKloud Pro** rejasida uchala cloud platforma uchun **cloud playground**lar va 50+ DevOps playground ham qo'shiladi — muhitni tozalashni unutib, cloud'da ortiqcha pul to'lash tashvishi yo'q, buni platforma o'zi hal qiladi.

💡 KodeKloud obunasini sotib olayotganda **UDEMY10** kupon kodi qo'shimcha maxsus chegirma beradi.

## 🧪 Mustaqil topshiriqlar

> Yechishdan oldin darsni yopib qo'ying. Taxminiy vaqt: 15 daqiqa.

**1-topshiriq · oson.** Kursda o'rgangan asosiy obyektlarni sanang: Pod'dan Ingress'gacha.

<details><summary>O'zingizni tekshiring</summary>

```bash
kubectl api-resources --namespaced=true | head -20
```
</details>

**2-topshiriq · o'rta.** O'z klasteringizda kurs davomida qolgan obyektlarni tozalang.

<details><summary>O'zingizni tekshiring</summary>

```bash
kubectl get all -A | grep -v kube-system
```
</details>

**3-topshiriq · qiyin.** Qaysi mavzuni eng zaif bilasiz? **Uni aniqlang va qaytaring.**

<details><summary>O'zingizni tekshiring</summary>

O'zingizni sinash uchun quyidagilarni **hujjatlarsiz** bajarib ko'ring:

```bash
# 1. 3 replikali deployment + NodePort servis
# 2. ConfigMap dan muhit o'zgaruvchisi
# 3. Pod uchun resurs limiti va liveness probe
# 4. NetworkPolicy: faqat bitta namespace'dan kirish
# 5. Buzuq Pod'ni topib tuzatish
```

Qaysi biri to'xtatib qo'ysa — o'sha bo'limga qayting.
</details>

## ❓ Savol-Javob

"Savol:" Kursni tugatdim — imtihondan oldin yana qanday amaliyot qilsam bo'ladi?
"Javob:" Kursning ichidagi mock imtihonlarni qayta ishlang, qo'shimcha sifatida KodeKloud'dagi Ultimate CKA Mock Exam seriyasini oling — u bir nechta klasterli, haqiqiy imtihonga o'xshash muhit beradi.

"Savol:" CKA'dan keyin qaysi sertifikatga o'tish mantiqiy?
"Javob:" Xavfsizlik yo'nalishida chuqurlashmoqchi bo'lsangiz — **CKS** (uni topshirish uchun amaldagi CKA talab qilinadi). Endi boshlayotgan hamkasblarga esa boshlang'ich **KCNA** mos.

"Savol:" Ultimate Mock Exam seriyasi nega Udemy'da emas?
"Javob:" U bir nechta klasterdan iborat katta lab infratuzilmasini talab qiladi, shuning uchun faqat KodeKloud platformasida (pullik obuna bilan) taqdim etiladi.

## 📌 CKA imtihon uchun maslahat

Kursni tugatish — yarim yo'l. Imtihon oldidan mock imtihonlarni **vaqt o'lchab** qayta-qayta ishlang: maqsad — javobni bilish emas, uni tez va xatosiz **terish** darajasiga chiqish.

## 🔗 Manbalar

- [CKA imtihoni rasmiy sahifasi — CNCF](https://www.cncf.io/training/certification/cka/)
- [CKS sertifikati — CNCF](https://www.cncf.io/training/certification/cks/)
- [KCNA sertifikati — CNCF](https://www.cncf.io/training/certification/kcna/)
- [KodeKloud platformasi](https://kodekloud.com)

---
*Bu dars KodeKloud CKA kursining 327-videosi asosida tayyorlandi.*

## 📖 Asosiy atamalar

Kurs davomida uchragan eng muhim atamalar bir joyda:

| Atama | Ma'nosi |
|---|---|
| **Pod** | Kubernetes yaratadigan eng kichik birlik |
| **Deployment** | Pod'lar sonini va versiyasini boshqaruvchi obyekt |
| **ReplicaSet** | Belgilangan sondagi Pod'ni saqlovchi obyekt |
| **Service** | Pod'lar oldiga barqaror IP va DNS nom qo'yuvchi obyekt |
| **Ingress** | HTTP trafikni domen va yo'l bo'yicha taqsimlovchi obyekt |
| **Namespace** | Klaster ichidagi mantiqiy bo'lim |
| **ConfigMap / Secret** | Konfiguratsiya va maxfiy ma'lumot saqlovchi obyektlar |
| **CNI** | Pod tarmog'ini quruvchi plagin |
| **kubelet** | Har node'da Pod'larni ko'taruvchi agent |
| **etcd** | Klasterning butun holati saqlanadigan baza |
| **Helm** | Kubernetes uchun paket menejeri |
| **Kustomize** | YAML'ni nusxalamasdan muhitga moslash vositasi |
