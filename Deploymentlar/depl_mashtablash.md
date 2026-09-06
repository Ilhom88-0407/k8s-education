# `describe deployment` chiqishini to'liq o'qish

> 🎯 **Bu darsda nimani o'rganamiz:**
> - `describe deployment` chiqishidagi har bir bo'lim nimani anglatadi
> - `OldReplicaSets` va `NewReplicaSet` nima uchun kerak
> - `Conditions` bo'limi qanday o'qiladi
> - `revision` raqami va yangilanish tarixi

## 💡 Hayotiy o'xshatish: kasallik tarixi

Shifokor bemorning kartasini ochganda faqat bugungi holatni emas, **butun
tarixni** ko'radi: qachon nima bo'lgan, qanday davolangan, natija qanday.

`kubectl describe deployment` — o'sha karta. U bir varaqda joriy holatni,
sozlamalarni va o'tmishni birga ko'rsatadi.

## To'liq chiqish

Quyida `nginx-deploy` deployment'ining haqiqiy `describe` chiqishi (5 replika,
3-revizyada):

```bash
kubectl get deployments
```

```text
NAME           READY   UP-TO-DATE   AVAILABLE   AGE
nginx-deploy   5/5     5            5           2d18h
```

```bash
kubectl describe deploy nginx-deploy
```

```text
Name:                   nginx-deploy
Namespace:              default
CreationTimestamp:      Fri, 01 May 2026 13:46:30 +0000
Labels:                 app=nginx-deploy
Annotations:            deployment.kubernetes.io/revision: 3
Selector:               app=nginx-deploy
Replicas:               5 desired | 5 updated | 5 total | 5 available | 0 unavailable
StrategyType:           RollingUpdate
MinReadySeconds:        0
RollingUpdateStrategy:  25% max unavailable, 25% max surge
Pod Template:
  Labels:       app=nginx-deploy
  Annotations:  kubectl.kubernetes.io/restartedAt: 2026-05-01T14:20:45Z
  Containers:
   nginx:
    Image:         nginx
    Port:          <none>
    Host Port:     <none>
    Environment:   <none>
    Mounts:        <none>
  Volumes:         <none>
  Node-Selectors:  <none>
  Tolerations:     <none>
Conditions:
  Type           Status  Reason
  ----           ------  ------
  Available      True    MinimumReplicasAvailable
  Progressing    True    NewReplicaSetAvailable
OldReplicaSets:  nginx-deploy-8b9dbd8c9 (0/0 replicas created), nginx-deploy-7b875bc49c (0/0 replicas created)
NewReplicaSet:   nginx-deploy-75c8b7c74b (5/5 replicas created)
Events:          <none>
```

## Bo'limlarni bir-bir ko'ramiz

### `Replicas:` qatori

```text
Replicas:  5 desired | 5 updated | 5 total | 5 available | 0 unavailable
```

| Qism | Ma'nosi |
|---|---|
| `desired` | Siz so'ragan son |
| `updated` | Nechtasi oxirgi shablonga mos |
| `total` | Hozir mavjud Pod'lar (yangilanish paytida `desired` dan ko'p bo'lishi mumkin) |
| `available` | Trafik qabul qilishga tayyor |
| `unavailable` | Hali tayyor emas |

**Yangilanish ketayotganini shundan bilasiz:** `updated` < `desired`.

### `StrategyType` va `RollingUpdateStrategy`

```text
StrategyType:           RollingUpdate
RollingUpdateStrategy:  25% max unavailable, 25% max surge
```

- **`maxUnavailable: 25%`** — 5 Pod'dan bir vaqtda ko'pi bilan 1 tasi
  yo'q bo'lishi mumkin.
- **`maxSurge: 25%`** — vaqtincha 6-Pod ko'tarilishi mumkin.

Ikkinchi strategiya — **`Recreate`**: barcha eski Pod'lar o'chadi, keyin
yangilari ko'tariladi. Bu **uzilish** demak, lekin eski va yangi versiya
bir vaqtda ishlashi mumkin bo'lmagan hollarda (masalan, umumiy baza
sxemasi o'zgarganda) kerak bo'ladi.

### `Annotations: deployment.kubernetes.io/revision: 3`

Bu Deployment 3-marta o'zgargan. Tarixni ko'rish:

```bash
kubectl rollout history deployment nginx-deploy
```

```text
REVISION  CHANGE-CAUSE
1         <none>
2         <none>
3         <none>
```

`CHANGE-CAUSE` bo'sh — chunki hech kim izoh qoldirmagan. Uni to'ldirish:

```bash
kubectl annotate deployment nginx-deploy \
  kubernetes.io/change-cause="image 1.27 ga yangilandi"
```

### `Conditions:` bo'limi

```text
Type           Status  Reason
Available      True    MinimumReplicasAvailable
Progressing    True    NewReplicaSetAvailable
```

| Type | `True` bo'lsa | `False` bo'lsa |
|---|---|---|
| **Available** | Yetarli Pod tayyor | Ilova ishlamayapti |
| **Progressing** | Yangilanish ketyapti yoki muvaffaqiyatli tugadi | To'xtab qolgan (`ProgressDeadlineExceeded`) |
| **ReplicaFailure** | — | Pod yaratib bo'lmayapti (kvota, resurs) |

`Progressing: False` + `ProgressDeadlineExceeded` — yangilanish 10 daqiqadan
(standart) beri oldinga siljimayapti. Sababni Pod'lardan qidiring.

### `OldReplicaSets` va `NewReplicaSet`

```text
OldReplicaSets:  nginx-deploy-8b9dbd8c9 (0/0), nginx-deploy-7b875bc49c (0/0)
NewReplicaSet:   nginx-deploy-75c8b7c74b (5/5 replicas created)
```

Eski ReplicaSet'lar `0/0` bilan **saqlanadi** — Pod'lari yo'q, lekin o'zlari
turadi. Nima uchun? `kubectl rollout undo` shular orqali ishlaydi: orqaga
qaytish uchun eski ReplicaSet'ni yana 5 ga masshtablash kifoya.

Nechtasi saqlanishini `spec.revisionHistoryLimit` belgilaydi (standart 10).

⚠️ Xesh (`75c8b7c74b`) Pod shablonidan hisoblanadi. Shuning uchun
`OldReplicaSets` va `NewReplicaSet` da **bir xil xesh turishi mumkin emas**.

### `Pod Template` ichidagi `Image: nginx`

Diqqat: bu yerda image **tegsiz** yozilgan. Bu xavfli — bugun `nginx:1.27`,
ertaga `nginx:1.29` tortilishi mumkin. Doim aniq teg qo'ying:

```bash
kubectl set image deployment/nginx-deploy nginx=nginx:1.27-alpine
```

## 🧪 Mustaqil topshiriqlar

> Taxminiy vaqt: 15 daqiqa.

**1-topshiriq · oson.** O'z Deployment'ingizning `revision` raqamini toping.

<details><summary>O'zingizni tekshiring</summary>

```bash
kubectl get deployment nginx-deploy \
  -o jsonpath='{.metadata.annotations.deployment\.kubernetes\.io/revision}{"\n"}'
```
</details>

**2-topshiriq · o'rta.** Image'ni o'zgartiring va `describe` chiqishida
`OldReplicaSets` paydo bo'lganini ko'ring.

<details><summary>O'zingizni tekshiring</summary>

```bash
kubectl describe deployment nginx-deploy | grep -E 'OldReplicaSets|NewReplicaSet'
# OldReplicaSets endi bo'sh emas
```
</details>

**3-topshiriq · qiyin.** `StrategyType` ni `Recreate` ga o'zgartiring va
image'ni yangilang. **Avval ayting:** `RollingUpdate` dan farqi nimada
ko'rinadi?

<details><summary>O'zingizni tekshiring</summary>

```bash
kubectl get pods -l app=nginx-namuna --watch
# Recreate'da BARCHA podlar avval Terminating bo'ladi, keyin yangilari ko'tariladi
# — ya'ni qisqa uzilish bo'ladi
```
</details>

📁 To'liq yechimlar: [`amaliyot/create_deployment/YECHIM.md`](amaliyot/create_deployment/YECHIM.md)

## ❓ Savol-Javob

**Savol:** `Events: <none>` — bu normalmi?
**Javob:** Ha. Kubernetes hodisalarni standart holatda 1 soat saqlaydi.
Deployment 2 kun oldin yaratilgan bo'lsa, hodisalar allaqachon o'chgan.

**Savol:** `restartedAt` annotatsiyasi qayerdan keldi?
**Javob:** `kubectl rollout restart deployment <nom>` uni qo'yadi. Bu
Pod shablonini "o'zgargan" qilib ko'rsatadi va shu bilan barcha Pod'larni
qayta yaratishga majbur qiladi — konfiguratsiyani o'zgartirmasdan.

**Savol:** Eski ReplicaSet'larni o'chirsam bo'ladimi?
**Javob:** Bo'ladi, lekin keyin ularga `rollout undo` qila olmaysiz.
Avtomatik tozalash uchun `revisionHistoryLimit` ni kamaytiring.

**Savol:** `maxSurge` va `maxUnavailable` ikkalasi ham 0 bo'lsa nima bo'ladi?
**Javob:** Kubernetes buni qabul qilmaydi — yangilanish hech qachon
boshlanmasdi. Kamida bittasi noldan katta bo'lishi kerak.

## 📌 CKA imtihon uchun maslahat

Deployment muammosini tez tashxislash:

```bash
kubectl rollout status deployment <nom>      # tugadimi yoki qotib qoldimi
kubectl rollout history deployment <nom>     # revizyalar
kubectl rollout undo deployment <nom>        # oldingi revizyaga qaytish
kubectl rollout undo deployment <nom> --to-revision=2
```

`describe` chiqishida birinchi qaraydigan joy — `Conditions`. `Available: False`
bo'lsa muammo Pod'larda, `Progressing: False` bo'lsa yangilanish qotib qolgan.

## 📖 Asosiy atamalar

| Atama | Ma'nosi |
|---|---|
| **`revision`** | Deployment shablonining versiya raqami |
| **`maxSurge`** | Yangilanish paytida qo'shimcha ko'tariladigan Pod'lar chegarasi |
| **`maxUnavailable`** | Bir vaqtda yo'q bo'lishi mumkin bo'lgan Pod'lar chegarasi |
| **`Recreate`** | Barchasini o'chirib, keyin yangisini ko'taradigan strategiya |
| **`Conditions`** | Deployment holatini bildiruvchi shartlar to'plami |
| **`revisionHistoryLimit`** | Nechta eski ReplicaSet saqlanishi |
| **`change-cause`** | Revizyaga qo'yiladigan izoh |

## 🔗 Manbalar

- [Deployment Status — kubernetes.io](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/#deployment-status)
- [Rolling Back a Deployment](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/#rolling-back-a-deployment)
- [kubectl rollout](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands#rollout)

---
⬅️ [Oldingi dars](podlarni_sonini_oshirish.md) · [Bo'lim indeksi](README.md) · ➡️ [deploymant3.md](deploymant3.md)
