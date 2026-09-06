# Pod'larni qayta yaratish va o'chirish

> 🎯 **Bu darsda nimani o'rganamiz:**
> - Pod'ni o'chirish va yangilangan konfiguratsiya bilan qayta yaratish
> - `kubectl apply` va `kubectl replace` orasidagi farq
> - Nima uchun Deployment'dagi Pod'ni o'chirish uni yo'q qilmaydi
> - Barcha namespace'lardagi Pod'larni ko'rish

## 💡 Hayotiy o'xshatish: lampochka

Yonib ketgan lampochkani **tuzatmaysiz** — yangisiga almashtirasiz. Pod
ham xuddi shunday: uni "tuzatish" degan tushuncha yo'q, o'chiriladi va
o'rniga yangisi qo'yiladi.

Farq shundaki, lampochkani siz o'zingiz almashtirasiz. Deployment ostidagi
Pod'ni esa **ReplicaSet** o'zi almashtiradi — siz faqat eskisini olib
tashlaysiz, yangisi o'zi paydo bo'ladi.

## Pod'ni o'chirish

```bash
kubectl delete pod <pod-nomi>
kubectl delete pod <pod-nomi> -n <namespace>
kubectl delete -f manifest.yaml           # manifestdagi hamma narsani
```

⚠️ **Muhim farq:**

| Pod qanday yaratilgan | `delete pod` dan keyin |
|---|---|
| `kubectl run` yoki `apply -f pod.yaml` bilan bevosita | **Butunlay yo'qoladi.** Hech kim tiklamaydi |
| Deployment / ReplicaSet ostida | **Darrov yangisi paydo bo'ladi.** ReplicaSet sanoqni saqlaydi |

Ikkinchi holat ataylab shunday: bu Pod'ni "qayta ishga tushirish"ning eng
oddiy usuli.

## Konfiguratsiyani yangilash

```bash
kubectl apply -f manifest.yaml
```

`apply` — **idempotent**: obyekt yo'q bo'lsa yaratadi, bor bo'lsa farqni
qo'llaydi. Shuning uchun uni istagancha marta ishga tushirish mumkin.

| Buyruq | Xatti-harakati |
|---|---|
| `kubectl apply -f` | Yo'q bo'lsa yaratadi, bor bo'lsa yangilaydi. **Odatdagi tanlov** |
| `kubectl create -f` | Yo'q bo'lsa yaratadi, bor bo'lsa **xato beradi** |
| `kubectl replace -f` | Butunlay almashtiradi; yo'q bo'lsa xato beradi |

Pod'ning ba'zi maydonlari (masalan `spec.containers[].image` dan boshqa
ko'pchiligi) **o'zgarmas**. Ularni yangilash uchun Pod'ni o'chirib qayta
yaratish kerak — yana bir sabab, nega Deployment ishlatiladi.

## Pod'larni ko'rish

```bash
kubectl get pods                    # joriy namespace
kubectl get pods -n kube-system     # ma'lum bir namespace
kubectl get pods -A                 # BARCHA namespace'lar
kubectl get pods -o wide            # IP va node ustunlari bilan
kubectl get pods --watch            # o'zgarishlarni jonli kuzatish
```

`--watch` yangilanishni kuzatishda qulay: yangi Pod'lar `Running` ga
o'tayotganini va eskilari `Terminating` bo'layotganini real vaqtda ko'rasiz.

## Pod yaratish

```bash
# manifestdan — ishlab chiqarish uchun
kubectl apply -f amaliyot/lesson21/01-sinov-pod.yaml

# tez sinash uchun
kubectl run sinov --image=nginx:1.27-alpine
```

## 🧪 Mustaqil topshiriqlar

> Taxminiy vaqt: 10 daqiqa.

**1-topshiriq · oson.** `kubectl run` bilan `yolgiz-pod` yarating, keyin uni
o'chiring va `kubectl get pods` bilan haqiqatan yo'qolganini tasdiqlang.

<details><summary>O'zingizni tekshiring</summary>

```bash
kubectl get pod yolgiz-pod
# Error from server (NotFound) — kutilgan natija
```
</details>

**2-topshiriq · o'rta.** `kubectl create deployment mashq-deploy
--image=nginx:1.27-alpine --replicas=2` bilan Deployment yarating. Uning
Pod'laridan birini o'chiring. Nechta Pod qoladi?

<details><summary>O'zingizni tekshiring</summary>

```bash
kubectl get pods -l app=mashq-deploy
# Yana 2 ta pod bo'ladi — bittasi yangi, AGE ustuni buni ko'rsatadi
```
</details>

**3-topshiriq · qiyin.** Bir terminalda `kubectl get pods --watch` ni ishga
tushiring. Ikkinchisida Pod'ni o'chiring. **Avval ayting:** birinchi
terminalda qanday holatlar ketma-ketligini ko'rasiz?

<details><summary>O'zingizni tekshiring</summary>

Kutilgan ketma-ketlik: `Terminating` → yangi Pod `Pending` → `ContainerCreating`
→ `Running`. Eski Pod ro'yxatdan yo'qoladi.
</details>

📁 To'liq yechimlar: [`amaliyot/lesson21/YECHIM.md`](amaliyot/lesson21/YECHIM.md)

## ❓ Savol-Javob

**Savol:** Pod `Terminating` holatida qotib qoldi. Nima qilay?
**Javob:** Kubernetes avval ilovaga tugash uchun vaqt beradi
(`terminationGracePeriodSeconds`, standart 30 soniya). Uzoq davom etsa,
ilova `SIGTERM` signalini e'tiborsiz qoldirayotgan bo'lishi mumkin.
Majburiy o'chirish: `kubectl delete pod <nom> --force --grace-period=0`
— lekin bu oxirgi chora.

**Savol:** Butun namespace'dagi Pod'larni birdan o'chirish mumkinmi?
**Javob:** `kubectl delete pods --all -n <namespace>`. Lekin Deployment
ostidagilar darrov qaytadi — ularni yo'q qilish uchun Deployment'ni o'chirish
kerak.

**Savol:** `apply` va `create` orasida qaysi birini tanlay?
**Javob:** Doim `apply`. U idempotent va manifestni qayta qo'llash imkonini
beradi. `create` faqat "bu obyekt hali yo'qligiga ishonchim komil" degan
holatda.

## 📌 CKA imtihon uchun maslahat

Vaqtni tejaydigan bayroqlar:

```bash
kubectl delete pod <nom> --grace-period=0 --force   # darhol o'chirish
kubectl delete pod --all -n <namespace>             # namespace'dagi hammasi
kubectl delete -f fayl.yaml                         # manifestdagi hammasi
```

Imtihonda Pod'ni "qayta ishga tushirish" so'ralsa, Deployment ostidagi
Pod'ni shunchaki o'chiring — ReplicaSet yangisini o'zi ko'taradi.
Deployment uchun esa: `kubectl rollout restart deployment <nom>`.

## 📖 Asosiy atamalar

| Atama | Ma'nosi |
|---|---|
| **Idempotent** | Necha marta bajarilsa ham natija bir xil bo'ladigan amal |
| **`Terminating`** | Pod o'chirilyapti; ilovaga tugash uchun vaqt berilgan |
| **`--grace-period`** | Ilovaga tugash uchun beriladigan soniyalar soni |
| **`-A`** | `--all-namespaces` ning qisqasi |
| **`--watch`** | O'zgarishlarni real vaqtda kuzatish |

## 🔗 Manbalar

- [kubectl apply — Declarative Management](https://kubernetes.io/docs/tasks/manage-kubernetes-objects/declarative-config/)
- [Pod Lifecycle: Termination](https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/#pod-termination)
- [kubectl Cheat Sheet](https://kubernetes.io/docs/reference/kubectl/quick-reference/)

---
⬅️ [Oldingi dars](lesson21.md) · [Bo'lim indeksi](README.md) · ➡️ Keyingi bo'lim: [Serverga_va_podga_ulanish](../Serverga_va_podga_ulanish/)
