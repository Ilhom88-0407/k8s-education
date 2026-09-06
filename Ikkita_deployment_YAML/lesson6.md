# Deployment'dagi Pod sonini o'zgartirish

> 🎯 **Bu darsda nimani o'rganamiz:**
> - Manifestdagi `replicas` ni o'zgartirish va qayta qo'llash
> - O'zgarish ikkala ilovaga qanday ta'sir qiladi

```bash
kubectl edit deployment k8s-web-to-nginx
```
Bu buyruqni bajarishimiz bilan biz deploymentni tahrirlash uchun editor ochiladi. Bu editor orqali biz deploymentdagi podlarni sonini o'zgartirishimiz mumkin bo'ladi. Biz deploymentdagi podlarni sonini 3 ga o'zgartiramiz va saqlaymiz.

```yaml
spec:
  replicas: 3
```
Shu bilan birga deployment k8s-web-to-nginx.yaml faylida ham podlarni sonini 3 ga o'zgartiramiz va saqlaymiz.

```yaml
spec:
  replicas: 3
``` 

## Deploymentni o'chirib tashlash

```bash
kubectl delete deployment k8s-web-to-nginx
``` 
Yuqoridagi buyruqni bajarishimiz bilan biz k8s-web-to-nginx deploymentini o'chirib tashlaymiz. Bu buyruqni bajarishimiz bilan bizning clusterimizda k8s-web-to-nginx deploymenti va unga tegishli podlar o'chiriladi.
## Deploymentni yaratish

```bash
kubectl apply -f k8s-web-to-nginx.yaml
```
Yuqoridagi buyruqni bajarishimiz bilan biz k8s-web-to-nginx.yaml faylida yozilgan deploymentni yaratamiz. Bu buyruqni bajarishimiz bilan bizning clusterimizda k8s-web-to-nginx deploymenti va unga tegishli podlar yaratiladi.
## Deploymentni tekshirish

```bash
kubectl get deployments
```
Yuqoridagi buyruqni bajarishimiz bilan biz clusterimizda mavjud bo'lgan deploymentlarni ko'ra olamiz. Bu buyruqni bajarishimiz bilan biz k8s-web-to-nginx deploymentini va uning holatini ko'ra olamiz.
```bash
kubectl get pods
```
Yuqoridagi buyruqni bajarishimiz bilan biz clusterimizda mavjud bo'lgan podlarni ko'ra olamiz. Bu buyruqni bajarishimiz bilan biz k8s-web-to-nginx deploymentiga tegishli podlarni va ularning holatini ko'ra olamiz.

## 🧪 Mustaqil topshiriq

**Topshiriq.** Shu darsdagi buyruqlarni o'z klasteringizda qaytaring va
natijani `kubectl get all` bilan tasdiqlang.

<details><summary>O'zingizni tekshiring</summary>

```bash
kubectl get deploy,svc,pods -o wide
```
</details>

📁 Tayyor fayllar: [`amaliyot/`](amaliyot/)

## ❓ Savol-Javob

**Savol:** `kubectl apply -f` ga bir necha faylni birdan berish mumkinmi?
**Javob:** Ha: `kubectl apply -f a.yaml -f b.yaml`. Butun papkani ham:
`kubectl apply -f amaliyot/`.

**Savol:** Bitta faylda bir necha obyekt bo'lishi mumkinmi?
**Javob:** Ha. Ular `---` qatori bilan ajratiladi. Bu bog'liq obyektlarni
(Service + Deployment) birga saqlashda qulay.

## 📖 Asosiy atamalar

| Atama | Ma'nosi |
|---|---|
| **Service DNS nomi** | Klaster ichida servisga murojaat qilish uchun nom |
| **ClusterIP** | Faqat klaster ichidan ko'rinadigan Service turi |
| **CoreDNS** | Service nomlarini IP'ga aylantiruvchi klaster DNS serveri |
| **FQDN** | `<servis>.<namespace>.svc.cluster.local` — to'liq nom |
| **Ko'p hujjatli YAML** | Bitta faylda `---` bilan ajratilgan bir necha obyekt |

## 🔗 Manbalar

- [DNS for Services and Pods](https://kubernetes.io/docs/concepts/services-networking/dns-pod-service/)
- [Connecting Applications with Services](https://kubernetes.io/docs/tutorials/services/connect-applications-service/)
- [Service — kubernetes.io](https://kubernetes.io/docs/concepts/services-networking/service/)

---
⬅️ [Bo'lim indeksi](README.md) · ➡️ [lesson7.md](lesson7.md)
