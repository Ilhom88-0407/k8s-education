# Kubernetes Dashboard — web interfeys

> 🎯 **Bu darsda nimani o'rganamiz:**
> - minikube'da Dashboard'ni bir buyruq bilan ochish
> - Oddiy klasterda Dashboard'ni o'rnatish va kirish huquqini sozlash
> - Nima uchun `cluster-admin` berish xavfli va qachon mumkin
> - NodePort orqali Dashboard'ga tashqaridan kirish

## 💡 Hayotiy o'xshatish: avtomobil paneli

`kubectl` — dvigatel bo'limiga tushib, hamma narsani qo'l bilan tekshirish.
Dashboard — **boshqaruv paneli**: tezlik, yoqilg'i, harorat bir qarashda
ko'rinadi.

Panel qulay, lekin mexanik baribir dvigatel bo'limiga tushadi. Shuning uchun
Dashboard `kubectl` ni **almashtirmaydi** — u faqat umumiy manzarani tezroq
ko'rsatadi. CKA imtihonida esa Dashboard umuman bo'lmaydi.

## minikube'da — bir buyruq

```bash
minikube dashboard
```

![minikube dashboard buyrug'ining chiqishi: dashboard va metrics-scraper image'lari yuklanmoqda, so'ng proxy ishga tushirilmoqda](image-2.png)

Buyruq brauzerni o'zi ochadi. Faqat URL kerak bo'lsa:

```bash
minikube dashboard --url
```

To'liq ma'lumot ko'rinishi uchun metrics-server ni ham yoqing:

```bash
minikube addons enable metrics-server
```

## Oddiy klasterda o'rnatish

minikube ishlatmayotgan bo'lsangiz, Dashboard'ni qo'lda o'rnatish kerak.

### 1-qadam. Dashboard'ni o'rnatish

```bash
kubectl apply -f https://raw.githubusercontent.com/kubernetes/dashboard/v2.7.0/aio/deploy/recommended.yaml
```

⚠️ Versiyani tekshiring. Yuqoridagi `v2.7.0` — Helm'siz o'rnatishning
oxirgi versiyalaridan biri. Joriy versiya uchun
[rasmiy repozitoriyani](https://github.com/kubernetes/dashboard/releases)
ko'ring; 7.x dan boshlab Dashboard faqat Helm orqali o'rnatiladi.

O'rnatilganini tekshirish:

```bash
kubectl get pods -n kubernetes-dashboard
```

### 2-qadam. Administrator hisobini yaratish

> 📁 **Tayyor fayl:** [`amaliyot/lesson5/admin-user.yaml`](amaliyot/lesson5/admin-user.yaml)

```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: admin-user
  namespace: kubernetes-dashboard
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: admin-user
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: cluster-admin
subjects:
  - kind: ServiceAccount
    name: admin-user
    namespace: kubernetes-dashboard
```

```bash
kubectl apply -f amaliyot/lesson5/admin-user.yaml
```

### 🔴 Xavfsizlik ogohlantirishi

Bu manifest `admin-user` hisobiga **`cluster-admin`** rolini beradi — ya'ni
klasterdagi **har qanday** amalni bajarish huquqini: barcha namespace'lardagi
Secret'larni o'qish, istalgan Pod'ni o'chirish, RBAC qoidalarini o'zgartirish.

| Muhit | Shunday qilish mumkinmi |
|---|---|
| minikube, lokal sinov klasteri | ✅ Ha |
| Jamoaviy dev klaster | ⚠️ Ehtiyot bo'ling |
| Ishlab chiqarish | ❌ **Hech qachon** |

Ishlab chiqarishda foydalanuvchiga faqat kerakli huquqlarni beruvchi
alohida `Role` va `RoleBinding` yoziladi. Masalan, faqat o'qish uchun:

```bash
kubectl create clusterrolebinding dashboard-viewer \
  --clusterrole=view \
  --serviceaccount=kubernetes-dashboard:admin-user
```

⚠️ Kirish tokeni ham maxfiy ma'lumot. Uni skrinshotga olib, repozitoriyaga
yoki chatga yuborish — klaster kalitini oshkor qilish bilan barobar.

### 3-qadam. Dashboard'ni tashqariga chiqarish

Standart holatda Dashboard servisi ClusterIP turida — unga tashqaridan
kirib bo'lmaydi. NodePort'ga o'tkazamiz:

```bash
kubectl patch svc kubernetes-dashboard -n kubernetes-dashboard \
  -p '{"spec": {"type": "NodePort"}}'
```

Tayinlangan portni aniqlaymiz:

```bash
kubectl get svc -n kubernetes-dashboard
```

### 4-qadam. Token olish va kirish

```bash
kubectl -n kubernetes-dashboard create token admin-user
```

![kubectl patch svc bilan kubernetes-dashboard servisi NodePort turiga o'tkazildi (443:31560/TCP), keyin kubectl create token admin-user buyrug'i kirish uchun JWT token chiqardi](image-3.png)

Token vaqtinchalik — standart holatda **1 soat** amal qiladi. Uzoqroq kerak
bo'lsa `--duration=24h` qo'shing.

Endi brauzerda `https://<node-IP>:<NodePort>` ochib, tokenni kiritasiz:

![Kubernetes Dashboard'ning Workloads sahifasi: 1 ta Deployment, 10 ta Pod va 2 ta ReplicaSet ishlayapti; quyida k8s-web-hello deployment'i mrpocker88/k8s-web-hello:1.0.2 image'i bilan 10/10 pod holatida](image-4.png)

### NodePort o'rniga — xavfsizroq usul

Dashboard'ni tashqi tarmoqqa umuman ochmasdan:

```bash
kubectl -n kubernetes-dashboard port-forward svc/kubernetes-dashboard 8443:443
```

Endi faqat `https://localhost:8443` orqali va faqat siz kira olasiz.

## minikube va oddiy Kubernetes farqi

| Vazifa | minikube | Oddiy Kubernetes |
|---|---|---|
| **Buyruq** | `minikube dashboard` | `kubectl proxy` yoki `port-forward` |
| **O'rnatish** | Avtomatik tayyor | `kubectl apply` orqali qo'lda |
| **Avtorizatsiya** | Talab qilinmaydi | Token yoki kubeconfig kerak |
| **Tashqi kirish** | `--url` bayrog'i | NodePort, Ingress yoki port-forward |

## 🧪 Mustaqil topshiriqlar

> Taxminiy vaqt: 20 daqiqa.

**1-topshiriq · oson.** minikube'da Dashboard'ni oching va `Workloads`
bo'limida nechta Deployment ishlayotganini sanang.

<details><summary>O'zingizni tekshiring</summary>

```bash
kubectl get deployments -A --no-headers | wc -l
# Dashboard'dagi son bilan bir xil bo'lishi kerak
```
</details>

**2-topshiriq · o'rta.** `admin-user` uchun token oling va uning amal
qilish muddatini 24 soatga uzaytiring.

<details><summary>O'zingizni tekshiring</summary>

```bash
kubectl -n kubernetes-dashboard create token admin-user --duration=24h
```
</details>

**3-topshiriq · qiyin.** `cluster-admin` o'rniga faqat o'qish huquqini
beruvchi `view` rolini bog'lang. **Avval ayting:** Dashboard'da nima
o'zgaradi?

<details><summary>O'zingizni tekshiring</summary>

```bash
# Obyektlar ko'rinadi, lekin "Delete" va "Edit" tugmalari xato beradi:
# pods is forbidden: User cannot delete resource
```
</details>

📁 To'liq yechimlar: [`amaliyot/lesson5/YECHIM.md`](amaliyot/lesson5/YECHIM.md)

## ❓ Savol-Javob

**Savol:** Dashboard'siz ishlash mumkinmi?
**Javob:** Nafaqat mumkin — tavsiya etiladi. `kubectl` tezroq, skript
yozish mumkin va CKA imtihonida faqat u bo'ladi. Dashboard — qo'shimcha
qulaylik.

**Savol:** Token muddati tugadi. Nima qilay?
**Javob:** Yangisini oling: `kubectl -n kubernetes-dashboard create token admin-user`.

**Savol:** Brauzer "ishonchsiz sertifikat" deb ogohlantiryapti.
**Javob:** Dashboard o'zi imzolagan sertifikat ishlatadi. Lokal muhitda
"Advanced → Proceed" bosing. Ishlab chiqarishda haqiqiy sertifikat qo'ying.

**Savol:** Dashboard'ni internetga ochsam bo'ladimi?
**Javob:** Yo'q. U klasterga to'liq kirish nuqtasi. Faqat `port-forward`
yoki VPN orqali oching.

## 📌 CKA imtihon uchun maslahat

Imtihonda Dashboard **yo'q** va kerak ham emas. Lekin RBAC bilimi kerak —
`admin-user.yaml` aynan RBAC misolidir:

```bash
kubectl create serviceaccount <nom> -n <ns>
kubectl create clusterrolebinding <nom> --clusterrole=view --serviceaccount=<ns>:<nom>
kubectl auth can-i delete pods --as=system:serviceaccount:<ns>:<nom>
```

`kubectl auth can-i` — huquqlarni tekshirishning eng tez usuli, yod oling.

## 📖 Asosiy atamalar

| Atama | Ma'nosi |
|---|---|
| **ServiceAccount** | Pod va xizmatlar uchun hisob (odam uchun emas) |
| **ClusterRole** | Butun klaster bo'ylab amal qiluvchi huquqlar to'plami |
| **ClusterRoleBinding** | ClusterRole'ni hisobga bog'lovchi obyekt |
| **`cluster-admin`** | Cheksiz huquq beruvchi tayyor ClusterRole |
| **`view`** | Faqat o'qish huquqini beruvchi tayyor ClusterRole |
| **Bearer token** | Dashboard'ga kirishda ishlatiladigan vaqtinchalik JWT |

## 🔗 Manbalar

- [Kubernetes Dashboard](https://github.com/kubernetes/dashboard)
- [RBAC Authorization](https://kubernetes.io/docs/reference/access-authn-authz/rbac/)
- [Accessing the Dashboard](https://kubernetes.io/docs/tasks/access-application-cluster/web-ui-dashboard/)

---
⬅️ [Oldingi dars](lesson4.md) · [Bo'lim indeksi](README.md) · ➡️ [lesson6.md](lesson6.md)
