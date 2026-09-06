# Docker Hub ga yangilangan image ni push qilish

> 🎯 **Bu darsda nimani o'rganamiz:**
> - Yangilangan image'ni Docker Hub'ga yuklash
> - Klasterdagi Deployment'ni yangi image'ga o'tkazish
## Docker Hub ga yangilangan image ni push qilish uchun quyidagi buyruqlarni bajarishimiz kerak:

```bash 
docker build -t your_dockerhub_username/your_image_name:tag .
docker push your_dockerhub_username/your_image_name:tag
```
## Bu buyruqlar `Dockerfile` dan yangilangan image ni yaratadi va `Docker Hub` ga push qiladi. Siz `your_dockerhub_username`, `your_image_name`, va `tag` ni o'zingizning ma'lumotlaringiz bilan almashtirishingiz kerak.
## Endi siz `Docker Hub` da yangilangan image ni ko'rishingiz mumkin.   
## Endi biz `Kubernetes` klasterida yangilangan image ni ishlatish uchun `YAML` faylni yangilaymiz. Quyidagi `YAML` faylni yaratamiz:

```yaml
apiVersion: v1
kind: Pod   
metadata:
    name: my-pod
spec:
    containers: 
    - name: my-container
      image: your_dockerhub_username/your_image_name:tag
      ports:
      - containerPort: 80
```
### agarda biz image ni bitta versiyadan ikkinchi versiyaga yangilashni istasak biz docker hub ga yangilangan image ni push qilamiz va `YAML` faylni yangilaymiz. Masalan, agar biz `my-image:1.0` dan `my-image:2.0` ga yangilashni istasak, biz quyidagi buyruqlarni bajarishimiz kerak:

```bash
docker build -t your_dockerhub_username/my-image:1.0  -t your_dockerhub_username/my-image:2.0
docker push your_dockerhub_username/my-image --all-tags
```

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
⬅️ [Bo'lim indeksi](README.md) · ➡️ Keyingi bo'lim: [Bulutda_klaster_yaratish](../Bulutda_klaster_yaratish/)
