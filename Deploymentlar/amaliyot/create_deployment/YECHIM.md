# Yechimlar — Deploymentlar bo'limi

## create_deployment.md topshiriqlari

### 1-topshiriq · oson

```bash
kubectl create deployment mashq-deploy --image=nginx:1.27-alpine --replicas=2
kubectl get rs -l app=mashq-deploy
```

```text
NAME                      DESIRED   CURRENT   READY   AGE
mashq-deploy-7d4f8c9b6d   2         2         2       15s
```

ReplicaSet nomi = Deployment nomi + `pod-template-hash`. Xesh Pod shablonidan
hisoblanadi, shuning uchun bir xil shablon doim bir xil xesh beradi.

### 2-topshiriq · o'rta

```bash
POD=$(kubectl get pods -l app=mashq-deploy -o jsonpath='{.items[0].metadata.name}')
kubectl delete pod "$POD"
kubectl get pods -l app=mashq-deploy
```

Yana 2 ta Pod bo'ladi, lekin bittasining `AGE` ustuni bir necha soniya.
Nomi ham boshqacha — oxirgi tasodifiy qism har Pod uchun yangidan
generatsiya qilinadi.

**Nima bo'ldi:** ReplicaSet controller Pod'lar sonini doim kuzatib turadi.
Siz bittasini o'chirgan zahoti u kerakli son (2) bilan haqiqiy sonni (1)
solishtirdi va yangi Pod yaratdi.

### 3-topshiriq · qiyin

**Kutilgan javob:** xato beradi, ikki xil sabab bilan.

**Yangi Deployment yaratayotgan bo'lsangiz:**

```text
The Deployment "nginx-deploy" is invalid: spec.template.metadata.labels:
Invalid value: map[string]string{"app":"nginx-namuna"}:
`selector` does not match template `labels`
```

Deployment o'zi yaratgan Pod'larni topa olmasligi mumkin bo'lgan konfiguratsiyani
Kubernetes qabul qilmaydi.

**Mavjud Deployment'ni tahrirlayotgan bo'lsangiz:**

```text
The Deployment "nginx-deploy" is invalid: spec.selector:
Invalid value: ...: field is immutable
```

`spec.selector` **o'zgarmas**. Sababi: agar selektorni o'zgartirish mumkin
bo'lganda, Deployment eski Pod'larini "unutib" qo'yardi va ular egasiz
qolardi. Kubernetes bunga yo'l qo'ymaydi.

**Yechim:** Deployment'ni o'chirib qayta yaratish.

```bash
kubectl delete deployment nginx-deploy
kubectl apply -f 01-nginx-deployment.yaml
```

## podlarni_sonini_oshirish.md topshiriqlari

### 1-topshiriq · oson

```bash
kubectl scale deployment nginx-deploy --replicas=4
kubectl get deployment nginx-deploy -o jsonpath='{.status.readyReplicas}{"\n"}'
```

### 2-topshiriq · o'rta

Birinchi terminalda:

```bash
kubectl get pods -l app=nginx-namuna --watch
```

Ikkinchisida:

```bash
kubectl scale deployment nginx-deploy --replicas=1
```

Uchta Pod `Terminating` holatiga o'tadi va yo'qoladi. Qolgani — odatda
**eng eskisi**: Kubernetes avval tayyor bo'lmaganlarni, keyin eng yoshlarini
o'chiradi.

### 3-topshiriq · qiyin

**Kutilgan javob:** 3 ta Pod qoladi — masshtablash bekor bo'ladi.

```bash
kubectl scale deployment nginx-deploy --replicas=6
kubectl get deployment nginx-deploy          # READY 6/6

kubectl apply -f 01-nginx-deployment.yaml
kubectl get deployment nginx-deploy          # READY 3/3
```

**Nima uchun:** `kubectl apply` manifestni haqiqat manbai deb biladi.
Manifestda `replicas: 3` yozilgan, shuning uchun u 6 ni 3 ga qaytaradi.

Bu ishlab chiqarishdagi eng ko'p uchraydigan tuzoqlardan biri: kimdir
qo'lda masshtablaydi, keyin CI/CD `apply` qiladi va masshtablash yo'qoladi.

**Ikki yechim:**

1. Doim manifest orqali masshtablang (`replicas:` ni tahrirlab, keyin `apply`).
2. HPA ishlatsangiz, manifestdan `replicas:` ni **butunlay olib tashlang** —
   shunda `apply` HPA qo'ygan songa tegmaydi.

## Tozalash

```bash
bash tozalash.sh
```
