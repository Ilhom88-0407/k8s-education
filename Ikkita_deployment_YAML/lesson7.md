# YAML malumotlarini yaratish bo'yicha yakuniy dars

> 🎯 **Bu darsda nimani o'rganamiz:**
> - Bo'lim bo'yicha yakuniy xulosa
> - YAML yozishda eng ko'p uchraydigan xatolar

## Bu darsda biz kichik bir `YAML` fayl yaratishni o'rganamiz.
## `YAML` fayl yaratish uchun biz oddiy matn muharriridan foydalanamiz. Masalan, `Notepad` yoki `VS Code`.
## Quyidagi `YAML` faylni yaratamiz:

```yaml
apiVersion: v1
kind: Pod
metadata:
    name: my-pod        
spec:
    containers:
    - name: my-container
      image: nginx
      ports:
      - containerPort: 80   
``` 
## Bu `YAML` fayl `Kubernetes` uchun `Pod` resursini yaratadi.
## `apiVersion` - bu resursning API versiyasini ko'rsatadi.
## `kind` - bu resursning tipini ko'rsatadi. 
## `metadata` - bu resursning metadata qismini ko'rsatadi. Bu yerda biz `name` maydonini `my-pod` deb belgilaymiz.
## `spec` - bu resursning spetsifikatsiyasini ko'rsatadi. Bu yerda biz `containers` maydonini belgilaymiz.
## `containers` - bu resursning konteynerlarini ko'rsatadi. Bu yerda biz bitta konteyner yaratamiz.
## `name` - bu konteynerning nomini ko'rsatadi. Bu yerda biz `my-container` deb belgilaymiz.
## `image` - bu konteynerning image'ini ko'rsatadi. Bu yerda biz `nginx` image'ini ishlatamiz.
## `ports` - bu konteynerning portlarini ko'rsatadi. Bu yerda biz `containerPort` maydonini `80` deb belgilaymiz.
## Endi biz bu `YAML` faylni saqlaymiz. Masalan  `my-pod.yaml` nomi bilan saqlaymiz.
## Endi biz  bu `YAML` faylni `Kubernetes` klasteriga qo'llaymiz. Buning uchun quyidagi buyruqni bajarishimiz kerak:

```bash
kubectl apply -f my-pod.yaml
``` 
# Bu buyruq `my-pod.yaml` faylini `Kubernetes` klasteriga qo'llaydi va `Pod` resursini yaratadi.
# Endi biz `Pod` resursining holatini tekshirishimiz mumkin. Buning uchun quyidagi buyruqni bajarishimiz kerak:

```bash
kubectl get pods
```     
# Bu buyruq `Kubernetes` klasteridagi barcha `Pod` resurslarini ko'rsatadi. Siz `my-pod` nomli `Pod` resursini ko'rishingiz kerak.
# Agar siz `my-pod` resursining holatini batafsil ko'rishni istasangiz, quyidagi buyruqni bajarishingiz mumkin:

```bash
kubectl describe pod my-pod
```     
# Bu buyruq `my-pod` resursining holatini ko'rsatadi.   
# Endi biz `my-pod` resursini o'chirishimiz mumkin. Buning uchun quyidagi buyruqni bajarishimiz kerak:

```bash
kubectl delete pod my-pod
```
# Bu buyruq `my-pod` resursini `Kubernetes` klasteridan o'chiradi.
# Endi biz `my-pod` resursining holatini tekshirishimiz mumkin. Buning uchun quyidagi buyruqni bajarishimiz kerak:

```bash
kubectl get pods
```
# Bu buyruq `Kubernetes` klasteridagi barcha `Pod` resurslarini ko'rsatadi. Siz `my-pod` nomli `Pod` resursini ko'rmasligingiz kerak, chunki u o'chirilgan.
# Bu darsda biz `YAML` malumotlarini yaratish va `Kubernetes` klasteriga qo'llashni o'rgandik. Endi siz `YAML` fayllarini yaratish va `Kubernetes` resurslarini boshqarish bo'yicha asosiy bilimlarga egasiz. Keyingi darslarda biz yanada murakkab `YAML` fayllarini yaratishni o'rganamiz.

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
⬅️ [Bo'lim indeksi](README.md) · ➡️ [lesson8.md](lesson8.md)
