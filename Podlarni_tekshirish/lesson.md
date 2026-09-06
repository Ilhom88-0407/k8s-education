# Pod holatini o'qish — get, describe va logs

> 🎯 **Bu darsda nimani o'rganamiz:**
> - `kubectl get pods` chiqishidagi har bir ustun nimani bildiradi
> - `kubectl describe pod` da eng muhim joy — Events bo'limi
> - Pod IP manzili nima uchun tashqaridan ko'rinmaydi
> - Klaster ichidan Pod'ni qanday sinash kerak

## 💡 Hayotiy o'xshatish: shifokor ko'rigi

Bemor kelganda shifokor uchta narsani ketma-ket qiladi: **qaraydi**
(umumiy holat), **so'raydi** (nima bo'ldi, qachondan beri) va **tahlil
oladi** (aniq ko'rsatkichlar).

Kubernetes'da ham xuddi shunday:

| Shifokor | kubectl |
|---|---|
| Qaraydi — umumiy ko'rinish | `kubectl get pods` |
| So'raydi — nima bo'ldi, qachon | `kubectl describe pod` |
| Tahlil oladi — ilovaning o'z xabari | `kubectl logs` |

Tartibni buzmang: `logs` dan boshlash — tahlildan boshlashga o'xshaydi,
ko'pincha vaqt yo'qotasiz.

## 1-qadam: `kubectl get pods`

```bash
kubectl get pods
```

```text
NAME            READY   STATUS    RESTARTS   AGE
my-nginx-pod    1/1     Running   0          5m
```

| Ustun | Nimani bildiradi |
|---|---|
| **NAME** | Pod'ning nomi |
| **READY** | `tayyor / jami` konteynerlar. `1/1` — bitta konteyner bor va u tayyor. `0/1` — bor, lekin hali tayyor emas |
| **STATUS** | `Running`, `Pending`, `CrashLoopBackOff`, `ImagePullBackOff`, `Terminating` |
| **RESTARTS** | Konteyner necha marta qayta ishga tushgan. **Nol bo'lmasa — e'tibor bering** |
| **AGE** | Pod qachondan beri mavjud |

⚠️ `READY 0/1` va `STATUS Running` birga bo'lishi mumkin. Bu "konteyner
ishlayapti, lekin readiness probe hali o'tmadi" degani — Service unga
trafik yubormaydi.

## 2-qadam: `kubectl describe pod`

```bash
kubectl describe pod my-nginx-pod
```

![kubectl describe pod my-nginx-pod chiqishi: Namespace default, Node minikube/192.168.49.2, Status Running va Pod IP 10.244.0.3](image.png)

Chiqish uzun, lekin unda uchta muhim joy bor:

1. **`Node:`** — Pod qaysi node'da ishlayapti. Bo'sh bo'lsa, scheduler unga
   hali node topolmagan.
2. **`Containers:` → `State:` va `Last State:`** — konteyner hozir qanday
   holatda va oldingi urinishda nima bilan tugagan (`Exit Code`).
3. **`Events:`** — eng pastda. **Nosozlik sababi deyarli har doim shu yerda.**

Odatdagi Events xabarlari:

```text
Warning  FailedScheduling   0/3 nodes are available: insufficient cpu
Warning  Failed             Failed to pull image "nginx:1.99": not found
Normal   Pulled             Successfully pulled image "nginx:1.27-alpine"
Warning  BackOff            Back-off restarting failed container
```

## 3-qadam: `kubectl logs`

```bash
kubectl logs my-nginx-pod
kubectl logs my-nginx-pod --tail=50
kubectl logs my-nginx-pod --previous     # yiqilgan oldingi konteyner
```

## Pod IP manzili — nima uchun tashqaridan ping bermaydi

`describe` chiqishida `IP: 10.244.0.3` ko'rinadi. Bu manzil **faqat klaster
ichida** mavjud: u CNI plagini yaratgan virtual tarmoqqa tegishli va sizning
kompyuteringizning marshrutlash jadvalida yo'q.

Shuning uchun kompyuteringizdan `ping 10.244.0.3` javob bermaydi — bu
nosozlik emas, **kutilgan xatti-harakat**.

### Klaster ichidan qanday sinaladi

⚠️ **`kubectl ssh` degan buyruq mavjud emas.** Uchta ishlaydigan usul bor:

**1. Vaqtinchalik Pod ochish (eng oson):**

```bash
kubectl run sinov --rm -it --image=curlimages/curl:8.10.1 --restart=Never \
  -- curl -s http://10.244.0.3
```

`--rm` — buyruq tugagach Pod o'zi o'chadi.

**2. Mavjud Pod ichidan:**

```bash
kubectl exec -it my-nginx-pod -- sh
# ichida: wget -qO- http://10.244.0.4
```

**3. Lokal portga ulash:**

```bash
kubectl port-forward pod/my-nginx-pod 8080:80
curl http://localhost:8080
```

Node'ning o'ziga kirish kerak bo'lsa (bu kamdan-kam kerak):

```bash
minikube ssh                                    # minikube uchun
kubectl debug node/<node-nomi> -it --image=busybox:1.37   # istalgan klasterda
```

## 🧪 Mustaqil topshiriqlar

> Taxminiy vaqt: 15 daqiqa.

**1-topshiriq · oson.** Ataylab mavjud bo'lmagan image bilan Pod yarating:
`kubectl run buzuq --image=nginx:9.99-yoq`. `STATUS` nima bo'ladi va sababini
qayerdan topasiz?

<details><summary>O'zingizni tekshiring</summary>

```bash
kubectl describe pod buzuq | tail -8
# Events'da: Failed to pull image ... not found
```
</details>

**2-topshiriq · o'rta.** Ishlab turgan Pod'ning IP manzilini oling va **boshqa
Pod'dan** unga so'rov yuborib javob olganingizni isbotlang.

<details><summary>O'zingizni tekshiring</summary>

```bash
kubectl get pod my-nginx-pod -o jsonpath='{.status.podIP}{"\n"}'
# curl javobida "Welcome to nginx!" bo'lishi kerak
```
</details>

**3-topshiriq · qiyin.** `kubectl run yiqiluvchi --image=busybox:1.37 --
sh -c 'sleep 5; exit 1'` ni bajaring. **Avval ayting:** bir daqiqadan keyin
`RESTARTS` va `STATUS` nima bo'ladi? Keyin tekshiring va sababni `--previous`
bilan toping.

<details><summary>O'zingizni tekshiring</summary>

```bash
kubectl get pod yiqiluvchi
# STATUS: CrashLoopBackOff, RESTARTS: 3-4 atrofida
kubectl describe pod yiqiluvchi | grep -A3 'Last State'
# Exit Code: 1
```
</details>

📁 To'liq yechimlar: [`amaliyot/lesson/YECHIM.md`](amaliyot/lesson/YECHIM.md)

## ❓ Savol-Javob

**Savol:** `RESTARTS` ustunida katta son turibdi. Bu qanchalik jiddiy?
**Javob:** Juda jiddiy. Konteyner yiqilyapti va Kubernetes uni qayta-qayta
ko'taryapti. `kubectl logs <nom> --previous` bilan yiqilish sababini toping.

**Savol:** `describe` chiqishi juda uzun, hammasini o'qish shartmi?
**Javob:** Yo'q. Eng pastdan boshlang: `kubectl describe pod <nom> | tail -20`.
Events deyarli har doim javobni beradi.

**Savol:** `Events` bo'limi bo'sh. Nima uchun?
**Javob:** Kubernetes hodisalarni standart holatda faqat 1 soat saqlaydi.
Eski Pod uchun ular yo'qolgan bo'ladi — `kubectl get events --sort-by=.metadata.creationTimestamp`
bilan umumiy ro'yxatga qarang.

**Savol:** `READY 0/1` va `Running` — bu qanday bo'ladi?
**Javob:** Konteyner ishga tushgan, lekin **readiness probe** hali muvaffaqiyat
qaytarmagan. Service bunday Pod'ga trafik yubormaydi. Probe sozlamalarini
`describe` da tekshiring.

## 📌 CKA imtihon uchun maslahat

Nosozlik masalalarida shu uch buyruq 90% hollarda yechim beradi:

```bash
kubectl get pods -o wide
kubectl describe pod <nom> | tail -20
kubectl logs <nom> --previous
```

Barcha namespace'lardagi muammoli Pod'larni tez topish:

```bash
kubectl get pods -A --field-selector=status.phase!=Running
```

## 📖 Asosiy atamalar

| Atama | Ma'nosi |
|---|---|
| **READY** | `tayyor/jami` konteynerlar nisbati |
| **RESTARTS** | Konteyner necha marta qayta ishga tushgan |
| **Events** | `describe` chiqishining oxiridagi hodisalar jurnali |
| **Readiness probe** | Konteyner trafik qabul qilishga tayyorligini tekshiruvchi sinov |
| **Exit Code** | Konteyner qaysi kod bilan tugagani; `0` — normal, boshqasi — xato |
| **`--rm`** | Vaqtinchalik Pod'ni ish tugagach avtomatik o'chiradi |

## 🔗 Manbalar

- [Debug Pods — kubernetes.io](https://kubernetes.io/docs/tasks/debug/debug-application/debug-pods/)
- [Pod Lifecycle — kubernetes.io](https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/)
- [Configure Liveness, Readiness and Startup Probes](https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/)

---
⬅️ [Bo'lim indeksi](README.md) · ➡️ Keyingi bo'lim: [Konteynerlar_bilan_ishlash](../Konteynerlar_bilan_ishlash/)
