# K8S dokumentlari bilan ishlash

> 🎯 **Bu darsda nimani o'rganamiz:**
> - kubernetes.io hujjatlaridan tayyor manifest namunasini olish
> - `kubectl explain` bilan maydon nomini topish
> - Imtihonda hujjatlardan qanday tez foydalanish
## https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#dns-label-names
K8S bo'yicha barcha ma'limotlarni quyidagi sayq orqali olsangiz bo'ladi:
```
https://kubernetes.io/ru/docs/home/
```
bizga ko'proq kerak bo'ladigonini ko'rib chiqishimiz kerak.
1. Referens -> kubernetes-api -> kubernetes-api 
2. Referens -> API Overview
3. Referens -> API Access Control
Deployment dokumentlari bilan ishlash:
``` 
https://kubernetes.io/docs/concepts/workloads/controllers/deployments/
```
bu yerda quyidagi malimotlarni ko'rishimiz mumkin:
```
- apiVersion: apps/v1 - bu API versiyasi
- kind: Deployment - bu Deployment tipi
- metadata:
    name: k8s-web-hello - bu Deployment nomi
- spec: 
    selector:
      matchLabels:  
        app: k8s-web-hello - bu Deployment nomi
    template:   
      metadata:
        labels:
          app: k8s-web-hello - bu Deployment nomi
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
DeploymentSpec Documentlari bilan ishlash:

Selector (LabelSelector), required - bu majburiy bo'lib, Deployment qaysi Podlarni boshqarishini bildiradi.

template (PodTemplateSpec), required - bu majburiy bo'lib, qaysi Pod yaratish uchun qolip.

containers (Container[]), required - bu majburiy bo'lib, qaysi Docker image ishlatilishini ko'rsatadi.

ports (ContainerPort[]), required - bu majburiy bo'lib, qaysi Docker image ishlatilishini ko'rsatadi.

replicas (int32), bu Podlar sonini ko'rsatadi. majburiy emas.

strategy (DeploymentStrategy), bu Podlarni qanday qilib o'zgartirishini ko'rsatadi.

    strategy.type (string), bu Podlarni qanday qilib o'zgartirishini ko'rsatadi.

    strategy.rollingUpdate (RollingUpdateDeployment), bu Podlarni qanday qilib o'zgartirishini ko'rsatadi.

strategy.rollingUpdate (RollingUpdateDeployment).maxUnavailable (intstr.IntOrString), bu Podlarni qanday qilib o'zgartirishini ko'rsatadi.

strategy.rollingUpdate (RollingUpdateDeployment).maxSurge (intstr.IntOrString), bu Podlarni qanday qilib o'zgartirishini ko'rsatadi.


Agar biz <spec> ni ichida nimalar bo'lishini bilmoqchimiz bo'lsak:
```
kubectl get deployment k8s-web-hello -o yaml
```
yoki dokumnetatsiyada ko'rsatilgan qiymatni ko'rib chiqishimiz mumkin.

https://kubernetes.io/docs/reference/kubernetes-api/workload-resources/deployment-v1/#DeploymentSpec

bu yerda bizga ko'proq kerak bo'ladigonini ko'rib chiqishimiz kerak.

selector (LabelSelector), required - bu majburiy bo'lib, Deployment qaysi Podlarni boshqarishini bildiradi.

template (PodTemplateSpec), required - bu majburiy bo'lib, qaysi Pod yaratish uchun qolip.

replicas (int32), bu Podlar sonini ko'rsatadi. majburiy emas.

minReadySeconds (int32), bu Podlarni qanday qilib o'zgartirishini ko'rsatadi.

strategy (DeploymentStrategy), bu Podlarni qanday qilib o'zgartirishini ko'rsatadi.

    strategy.type (string), bu Podlarni qanday qilib o'zgartirishini ko'rsatadi.

    strategy.rollingUpdate (RollingUpdateDeployment), bu Podlarni qanday qilib o'zgartirishini ko'rsatadi.

            strategy.rollingUpdate.maxSurge (IntOrString), bu Podlarni qanday qilib o'zgartirishini ko'rsatadi.

            strategy.rollingUpdate.maxUnavailable (IntOrString), bu Podlarni qanday qilib o'zgartirishini ko'rsatadi.

## 🧪 Mustaqil topshiriqlar

> Taxminiy vaqt: 10 daqiqa.

**1-topshiriq · oson.** `kubectl explain` bilan Pod'ning `spec` ichida
qanday maydonlar borligini toping.

<details><summary>O'zingizni tekshiring</summary>

```bash
kubectl explain pod.spec | head -30
```
</details>

**2-topshiriq · o'rta.** Klasteringizda qaysi API versiyalari mavjudligini
ro'yxatlang.

<details><summary>O'zingizni tekshiring</summary>

```bash
kubectl api-resources | head -20
kubectl api-versions | sort
```
</details>

**3-topshiriq · qiyin.** `kubectl explain` bilan `livenessProbe` ning
barcha ichki maydonlarini rekursiv chiqaring.

<details><summary>O'zingizni tekshiring</summary>

```bash
kubectl explain pod.spec.containers.livenessProbe --recursive
```
</details>

## ❓ Savol-Javob

**Savol:** Imtihonda internetdan foydalanish mumkinmi?
**Javob:** CKA imtihonida faqat `kubernetes.io/docs` va bir necha rasmiy
sayt ochiq. Boshqa saytlar, StackOverflow va AI vositalari taqiqlangan.

**Savol:** `kubectl explain` hujjatlardan tezroqmi?
**Javob:** Ancha tezroq. U klasterning **o'z versiyasidagi** maydonlarni
ko'rsatadi — hujjatlarda esa boshqa versiya bo'lishi mumkin.

## 📌 CKA imtihon uchun maslahat

Hujjatlardan namuna izlaganda qidiruv so'zini aniq yozing: "ingress
example yaml", "networkpolicy example". Sahifadagi YAML blokini nusxa
ko'chirib, keyin tahrirlash — noldan yozishdan tezroq.

```bash
kubectl explain <resurs>.<maydon>          # bitta maydon
kubectl explain <resurs> --recursive       # butun daraxt
```

## 📖 Asosiy atamalar

| Atama | Ma'nosi |
|---|---|
| **`kubectl explain`** | Resurs maydonlarini klasterdan o'qib tushuntiruvchi buyruq |
| **`kubectl api-resources`** | Klasterdagi barcha resurs turlari ro'yxati |
| **`kubectl api-versions`** | Mavjud API guruh va versiyalari |

## 🔗 Manbalar

- [Kubernetes API Reference](https://kubernetes.io/docs/reference/kubernetes-api/)
- [kubectl explain](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands#explain)

---
⬅️ [Oldingi dars](lesson2.md) · [Bo'lim indeksi](README.md) · ➡️ [lesson4.md](lesson4.md)
