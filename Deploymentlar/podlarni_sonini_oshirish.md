# Pod'lar sonini o'zgartirish — masshtablash

> 🎯 **Bu darsda nimani o'rganamiz:**
> - `kubectl scale` bilan Pod'lar sonini oshirish va kamaytirish
> - `READY`, `UP-TO-DATE` va `AVAILABLE` ustunlari orasidagi farq
> - Manifest orqali masshtablash va nima uchun u afzalroq
> - Avtomatik masshtablash (HPA) haqida qisqacha

## 💡 Hayotiy o'xshatish: kassalar soni

Do'konda odam kam bo'lganda ikkita kassa yetadi. Bayram oldidan navbat
uzayganda menejer yana uchtasini ochadi. Kechqurun oqim pasayganda ortiqchasi
yopiladi.

Kassa **qurilmaydi** — u tayyor turadi, faqat ochiladi yoki yopiladi. Pod
ham shunday: image allaqachon node'da bo'lsa, yangi Pod bir necha soniyada
ko'tariladi.

## Joriy holatni ko'rish

```bash
kubectl get deployments
kubectl get deployment nginx-deploy
```

```text
NAME           READY   UP-TO-DATE   AVAILABLE   AGE
nginx-deploy   3/3     3            3           10m
```

| Ustun | Ma'nosi | Qachon farq qiladi |
|---|---|---|
| **READY** | `tayyor / kerakli` | Yangi Pod ko'tarilayotganda: `3/5` |
| **UP-TO-DATE** | Nechtasi oxirgi shablonga mos | Yangilanish vaqtida ortda qoladi |
| **AVAILABLE** | Nechtasi trafik olishga tayyor | `minReadySeconds` tufayli kechikadi |

## `kubectl scale` bilan masshtablash

```bash
kubectl scale deployment nginx-deploy --replicas=5
```

```text
deployment.apps/nginx-deploy scaled
```

Natijani tekshiramiz:

```bash
kubectl get deployment nginx-deploy
```

```text
NAME           READY   UP-TO-DATE   AVAILABLE   AGE
nginx-deploy   5/5     5            5           15m
```

Kamaytirish ham xuddi shu buyruq bilan:

```bash
kubectl scale deployment nginx-deploy --replicas=2
```

Kamaytirilganda Kubernetes qaysi Pod'ni o'chirishni o'zi tanlaydi: avval
`Pending` va tayyor bo'lmaganlarini, keyin eng yoshlarini.

### Shartli masshtablash

Joriy soni ma'lum bo'lgandagina o'zgartirish (parallel ishlarda foydali):

```bash
kubectl scale deployment nginx-deploy --current-replicas=3 --replicas=5
```

Joriy soni 3 bo'lmasa, buyruq hech nima qilmaydi.

## Manifest orqali masshtablash

`kubectl scale` **tez**, lekin uning bir kamchiligi bor: manifest faylingizda
hamon eski son turadi. Keyingi `kubectl apply -f` masshtablashni **orqaga
qaytarib yuboradi**.

Shuning uchun ishlab chiqarishda manifest tahrirlanadi:

```yaml
spec:
  replicas: 5    # 3 dan 5 ga o'zgartirildi
```

```bash
kubectl apply -f amaliyot/create_deployment/01-nginx-deployment.yaml
```

> 📁 **Tayyor fayl:** [`amaliyot/create_deployment/01-nginx-deployment.yaml`](amaliyot/create_deployment/01-nginx-deployment.yaml)

## Nima bo'layotganini kuzatish

```bash
kubectl get pods -l app=nginx-namuna --watch
```

Yangi Pod'lar `Pending` → `ContainerCreating` → `Running` bosqichlaridan
o'tadi. Image allaqachon node'da bo'lsa, bu bir necha soniya oladi.

Kim nima qilganini ko'rish:

```bash
kubectl describe deployment nginx-deploy | tail -10
```

```text
Events:
  Type    Reason             Age   From                   Message
  ----    ------             ----  ----                   -------
  Normal  ScalingReplicaSet  30s   deployment-controller  Scaled up replica set nginx-deploy-5c689d4b9f to 5 from 3
```

## Avtomatik masshtablash — HPA

Yukni qo'lda kuzatib o'tirish shart emas. **HorizontalPodAutoscaler**
CPU yoki xotira ko'rsatkichiga qarab Pod sonini o'zi o'zgartiradi:

```bash
kubectl autoscale deployment nginx-deploy --min=2 --max=10 --cpu-percent=70
kubectl get hpa
```

⚠️ HPA ishlashi uchun klasterda **metrics-server** bo'lishi shart.
minikube'da: `minikube addons enable metrics-server`.

HPA'ni ishlatganda manifestdagi `replicas:` ni **olib tashlang** — aks holda
har `apply` HPA qo'ygan sonni buzadi.

## 🧪 Mustaqil topshiriqlar

> Taxminiy vaqt: 15 daqiqa.

**1-topshiriq · oson.** `nginx-deploy` ni 4 replikaga masshtablang va
`kubectl get deploy` bilan tasdiqlang.

<details><summary>O'zingizni tekshiring</summary>

```bash
kubectl get deployment nginx-deploy -o jsonpath='{.status.readyReplicas}{"\n"}'
# 4 chiqishi kerak
```
</details>

**2-topshiriq · o'rta.** Bir terminalda `kubectl get pods --watch` ni
ishga tushiring, ikkinchisida 1 replikaga kamaytiring. Qaysi Pod'lar
o'chirilishini kuzating.

<details><summary>O'zingizni tekshiring</summary>

```bash
kubectl get pods -l app=nginx-namuna
# Bitta Pod qoladi — eng katta AGE ga ega bo'lgani
```
</details>

**3-topshiriq · qiyin.** `kubectl scale` bilan 6 replikaga o'ting, keyin
manifestni **o'zgartirmasdan** `kubectl apply -f` qiling. **Avval ayting:**
nechta Pod qoladi va nima uchun?

<details><summary>O'zingizni tekshiring</summary>

```bash
kubectl get deployment nginx-deploy
# READY 3/3 ga qaytadi — manifestdagi replicas: 3 g'olib chiqadi
```
</details>

📁 To'liq yechimlar: [`amaliyot/create_deployment/YECHIM.md`](amaliyot/create_deployment/YECHIM.md)

## ❓ Savol-Javob

**Savol:** `replicas: 0` qilsam bo'ladimi?
**Javob:** Ha. Barcha Pod'lar o'chadi, lekin Deployment qoladi. Ilovani
vaqtincha to'xtatishning eng oson yo'li — keyin `--replicas=3` bilan
qaytariladi.

**Savol:** Masshtablashda yangi Pod'lar qaysi node'ga tushadi?
**Javob:** Buni scheduler hal qiladi: node'lardagi bo'sh resurs, taint/toleration,
affinity qoidalari va Pod'lar taqsimotiga qarab.

**Savol:** `kubectl scale` va manifest — qaysi biri kuchliroq?
**Javob:** Oxirgi qo'llangan g'olib. `apply` dan keyin manifestdagi son
o'rnatiladi. Shuning uchun ishlab chiqarishda faqat manifest orqali ishlang.

**Savol:** Kamaytirilganda qaysi Pod o'chadi?
**Javob:** Kubernetes tartibi bor: avval tayyor bo'lmaganlar, keyin
`pod-deletion-cost` annotatsiyasi pastroqlari, keyin eng yoshlari.

## 📌 CKA imtihon uchun maslahat

Masshtablash masalalarida eng tez yo'l — `kubectl scale`:

```bash
kubectl scale deployment <nom> --replicas=<son>
kubectl scale --replicas=3 -f manifest.yaml
```

Deployment'dan tashqari ReplicaSet, StatefulSet va ReplicationController
ham masshtablanadi.

Vazifada "manifest orqali" deb aytilgan bo'lsa, `kubectl edit deployment <nom>`
ishlating — u tahrirlagandan keyin darrov qo'llaydi.

## 📖 Asosiy atamalar

| Atama | Ma'nosi |
|---|---|
| **Masshtablash (scaling)** | Pod nusxalari sonini o'zgartirish |
| **`replicas`** | Nechta Pod ishlashi kerakligi |
| **UP-TO-DATE** | Nechta Pod eng oxirgi shablonga mos kelishi |
| **AVAILABLE** | Nechta Pod trafik qabul qilishga tayyorligi |
| **HPA** | HorizontalPodAutoscaler — yukka qarab Pod sonini o'zgartiruvchi obyekt |
| **metrics-server** | CPU va xotira ko'rsatkichlarini yig'uvchi komponent |

## 🔗 Manbalar

- [Scaling a Deployment — kubernetes.io](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/#scaling-a-deployment)
- [Horizontal Pod Autoscaling](https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/)
- [kubectl scale](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands#scale)

---
⬅️ [Oldingi dars](create_deployment.md) · [Bo'lim indeksi](README.md) · ➡️ [depl_mashtablash.md](depl_mashtablash.md)
