## Deployment uchun YAML fayl yaratish
# 📄 YAML Fayllarida Ma'lumot Turlari (Qisqacha Qo'llanma)

Ushbu qo'llanma Kubernetes tizimida `Deployment` yaratishni, uning arxitekturasini va YAML fayllarini to'g'ri yozish qoidalarini o'rganishga mo'ljallangan.
[Grafikani ochish](ko'rinishi.html)
<embed src="ko'rinishi.html" width="100%" height="600">
<object data="ko'rinishi.html" type="text/html" width="100%" height="600"></object>
<iframe src="ko'rinishi.html" width="100%" height="600"></iframe>
---

# 🏗️ 1-QISM: Kubernetes Deployment Obyekti

Kubernetes'da ilovalarni uzluksiz ishlatish uchun `Deployment` obyektidan foydalaniladi.

## 📄 Amaliy misol (k8s-web-hello loyihasi)

```yaml
apiVersion: apps/v1
kind: Deployment

metadata:
  name: k8s-web-hello

spec:
  replicas: 5

  selector:
    matchLabels:
      app: k8s-web-hello

  template:
    metadata:
      labels:
        app: k8s-web-hello

    spec:
      containers:
        - name: k8s-web-hello
          image: mrpocker88/k8s-web-hello:1.0.2

          resources:
            limits:
              memory: "128Mi"
              cpu: "250m"

          ports:
            - containerPort: 3000
```
📖 Qatorlar bo'yicha lug'at
apiVersion

Kubernetes bilan qaysi API versiyasida ishlayotganimizni bildiradi.
```yaml
apiVersion: apps/v1
```
kind
Qanday turdagi resurs yaratilayotganini bildiradi.
```yaml
kind: Deployment
```

metadata

Resurs haqida umumiy ma'lumotlar.
metadata:
```yaml 
 name: k8s-web-hello
```
spec
Deployment qanday ishlashi kerakligini belgilaydi.
```yaml
spec:
```
replicas
Ilovaning nechta nusxasi ishlashi kerakligini ko'rsatadi.
```yaml
replicas: 5
```
selector.matchLabels
Deployment qaysi Podlarni boshqarishini bildiradi.
```yaml
selector:
  matchLabels:
    app: k8s-web-hello
```

template
Yangi Pod yaratish uchun qolip.
```yaml
template:
```

containers.image
Qaysi Docker image ishlatilishini ko'rsatadi.
```yaml
image: mrpocker88/k8s-web-hello:1.0.2
```

resources.limits
Container ishlatishi mumkin bo'lgan maksimal resurslar.
```yaml
resources:
  limits:
    memory: "128Mi"
    cpu: "250m"
```

ports.containerPort
Container ichidagi ochiq port.
```yaml
ports:
  - containerPort: 3000
  ```
🏭 2-QISM: Kubernetes Arxitekturasi

Kubernetes ichida bir nechta qatlamlar ishlaydi.

🏢 Deployment — Zavod boshqaruvchisi

Deployment umumiy nazoratni olib boradi.

Misol:

“Doim 5 ta Pod ishlab tursin.”

Agar Pod o'chsa, Deployment uni qayta tiklaydi.

👨‍🔧 ReplicaSet — Smena ustasi

ReplicaSet Podlar sonini nazorat qiladi.

Agar kerakli son kamayib ketsa:

yangi Pod yaratadi
avtomatik tiklaydi (Auto Healing)
📦 Pod — Ishchi xonasi

Pod — Kubernetes'dagi eng kichik ishchi obyekt.

Har bir Pod ichida:

1 yoki bir nechta container bo'ladi
alohida IP bo'ladi
alohida tarmoq muhiti bo'ladi
🐳 Container — Dasturning o'zi

Bu Docker image orqali ishga tushadigan asosiy dastur.

Misol:
```
image: mrpocker88/k8s-web-hello:1.0.2
```

# 📝 3-QISM: YAML Faylni Oddiy Tilda O'qish

Kubernetes'ga yuborilgan buyruq oddiy tilda quyidagicha bo'ladi:

> “Salom Kubernetes.
> Menga `k8s-web-hello` nomli loyiha yarat.
> Har doim 5 ta nusxa ishlasin.
> Har bir nusxaga `app: k8s-web-hello` yorlig'ini ber.
> Internetdan `mrpocker88/k8s-web-hello:1.0.2` image yuklab ishlat.
> Har biri maksimum 128MB RAM va 250m CPU ishlatsin.
> 3000-port ochiq bo'lsin.”

---

# 🧩 4-QISM: YAML Sintaksisi va Ma'lumot Turlari

YAML — inson o'qishi uchun qulay konfiguratsiya tili.

---

## 1️⃣ Oddiy Ma'lumot Turlari (Scalars)

```yaml
ism: Ali
yosh: 25
harorat: 36.6
talabami: true
avtomobil: null
```

2️⃣ Ro'yxatlar (Lists / Sequences)
- belgisi bilan yoziladi.
```yaml
dasturlash_tillari:
  - Python
  - JavaScript
  - Java
  ```
3️⃣ Lug'atlar (Mappings / Dictionaries)
Kalit-qiymat juftliklari.
```yaml
shaxs_malumotlari:
  ism: Vali
  familiya: Aliyev
  yosh: 30
```
4️⃣ Ko'p Qatorli Matnlar (Multiline Strings)
|
Qatorlarni saqlab qoladi.
```yaml
izoh: |
  Bu birinchi qator.
  Bu ikkinchi qator.
```
>
Qatorlarni birlashtirib yuboradi.
```yaml
izoh: >
  Bu juda uzun gap bo'lishi mumkin,
  lekin YAML uni bitta qator sifatida
  o'qiydi.
```
⚠️ ENG MUHIM QOIDA
❌ TAB ishlatmang

YAML fayllarda TAB qat'iyan taqiqlanadi.

Faqat SPACE ishlating.
--------------------------------------
✅ To'g'ri format
```yaml
spec:
  containers:
    - name: nginx
```
❌ Noto'g'ri format
```yaml
spec:
<TAB>containers:
```