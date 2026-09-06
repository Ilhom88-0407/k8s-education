# LoadBalancer servisiga publik IP manzilini tayinlash

> 🎯 **Bu darsda nimani o'rganamiz:**
> - Bulutda LoadBalancer servis haqiqiy tashqi IP olishi
> - Tashqi IP'ni tekshirish va ilovaga kirish
Kubernetes klasterida LoadBalancer turidagi servis yaratganingizda, odatda bulut provayderi avtomatik ravishda publik IP manzilini tayinlaydi. Biroq, ba'zi hollarda siz o'zingizning IP manzilingizni belgilashni xohlashingiz mumkin. Bu holatda, siz LoadBalancer servisining `loadBalancerIP` maydonini ishlatishingiz mumkin.  Quyidagi misolda, `my-loadbalancer-service` nomli LoadBalancer turidagi servis yaratilmoqda va unga `194.107.115.75` IP manzili tayinlanadi:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-loadbalancer-service
spec:
  type: LoadBalancer
  loadBalancerIP: "194.107.115.75"
  selector:
    app: my-app 
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8080
``` 
Bu `LoadBalancerIP` maydonini to'g'ri ishlatish uchun, sizning klasteringizda bu IP manzili mavjud bo'lishi va sizning bulut provayderingiz tomonidan qo'llab-quvvatlanishi kerak. Shuningdek, bu IP manzili sizning tarmog'ingizda bo'sh va foydalanishga tayyor bo'lishi kerak.
Yuqoridagi YAML faylini `kubectl apply -f` buyrug'i yordamida klasterga qo'llang va servis yaratilishini tekshiring. Agar hamma narsa to'g'ri bo'lsa, sizning LoadBalancer servisingiz `my-loadbalancer-service` nomli bo'lishi va 194.107.115.75 IP manziliga ega bo'lishi kerak.
## Ayrim bulutli provayderlarda LoadBalancer servisni IP manzilini tayinlash uchun qo'shimcha konfiguratsiyalar talab qilinishi mumkin. Masalan, Google Cloud Platform (GCP) da siz avval statik IP manzilini yaratishingiz va keyin uni LoadBalancer servisiga tayinlashingiz kerak bo'ladi. AWS da esa siz Elastic IP manzilini yaratib, uni LoadBalancer servisiga tayinlashingiz mumkin. Har bir bulut provayderining o'ziga xos talablarini tekshirish va ularga mos ravishda konfiguratsiya qilish mumkin.

## Unicon.uz bulutli muxidida LoadBalancer servisni IP manzilini tayinlash


## ❌ Nima uchun bu yuqoridagi konfiguratsiya ishlamaydi

```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-loadbalancer-service
spec:
  type: LoadBalancer
  loadBalancerIP: "194.107.115.75"
  # ...
```

**3 ta sabab:**

1. **Cloud Controller yo'q** — `LoadBalancer` AWS/GCP/Azure'da avtomatik LB yaratadi. Bare-metal'da Service `<pending>` holatida qoladi.
2. **`loadBalancerIP` deprecated** — Kubernetes v1.24+ versiyada eskirgan.
3. **IP node'da yo'q** — `194.107.115.75` NAT natijasi, node interfeysida faqat `192.168.16.196` bor.

---

## ✅ Yechimlar — taqqoslash

| Variant | Murakkablik | Qo'shimcha komponent | Sizga mosligi |
|---------|-------------|---------------------|---------------|
| **NodePort + NAT** | 🟢 Past | Yo'q | ⭐ Eng yaxshi |
| **Ingress + NodePort** | 🟡 O'rta | Ingress controller | Ko'p xizmat uchun |
| **MetalLB** | 🔴 Yuqori | MetalLB | Klaster kengaysa |

---

## ⭐ Tavsiya: NodePort + NAT

### 1. Service yarating

```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-app-service
spec:
  type: NodePort
  selector:
    app: my-app
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8080
      nodePort: 30080
```

```bash
kubectl apply -f service.yaml
```

### 2. Gateway/NAT routerda DNAT qoidasi

```
194.107.115.75:80  →  192.168.16.196:30080
```

### 3. Tekshiring

```bash
# Server'da
sudo ss -tlnp | grep 30080
curl http://localhost:30080

# Tashqaridan
curl http://194.107.115.75
```

---

## 🌐 Ko'p xizmat uchun: Ingress

Agar bir nechta domenlar (`api.example.com`, `app.example.com`) bo'lsa:

```bash
helm install ingress-nginx ingress-nginx/ingress-nginx \
  --namespace ingress-nginx --create-namespace \
  --set controller.service.type=NodePort \
  --set controller.service.nodePorts.http=30080 \
  --set controller.service.nodePorts.https=30443
```

NAT qoidalari:
```
194.107.115.75:80  →  192.168.16.196:30080
194.107.115.75:443 →  192.168.16.196:30443
```

---

## 📝 Eslatmalar

- `nodePort` oralig'i: **30000–32767**
- Privileged portlar (80, 443) faqat NAT orqali yo'naltirilishi mumkin
- Bitta `nodePort` faqat bitta xizmat tomonidan ishlatiladi
- Production'da TLS sertifikatlari uchun **cert-manager** + Let's Encrypt tavsiya etiladi

---

> 📅 **2026-yil 13-may** · Klaster: kubeadm v1.35.4 · Public IP: 194.107.115.75
## Kubernetes LoadBalancer Bare-Metal Klasterda

## 🧪 Mustaqil topshiriq

**Topshiriq.** LoadBalancer servis yarating va `EXTERNAL-IP` to'lishini
kuting (odatda 1-3 daqiqa).

<details><summary>O'zingizni tekshiring</summary>

```bash
kubectl get svc -w
# EXTERNAL-IP <pending> dan haqiqiy IP ga o'zgaradi
```
</details>

## ❓ Savol-Javob

**Savol:** `EXTERNAL-IP` juda uzoq `<pending>` turibdi.
**Javob:** Bulutda odatda 1-3 daqiqa. Uzoq davom etsa: kvota tugagan
bo'lishi mumkin yoki provayder LoadBalancer'ni qo'llab-quvvatlamaydi.
`kubectl describe svc <nom>` dagi Events'ni o'qing.

**Savol:** LoadBalancer'ni o'chirsam, bulutdagi resurs ham o'chadimi?
**Javob:** Ha, Service o'chirilganda provayder balanslovchini ham
o'chiradi. Lekin tekshirib turing — hisobingizda unutilgan balanslovchi
qolib ketmasin.

## 📖 Asosiy atamalar

| Atama | Ma'nosi |
|---|---|
| **Managed Kubernetes** | Bulut provayderi control plane'ni o'zi boshqaradigan xizmat |
| **Node pool** | Bir xil sozlamali worker node'lar guruhi |
| **kubeconfig** | Klasterga ulanish ma'lumotlari saqlanadigan fayl |
| **Kontekst (context)** | kubeconfig ichidagi "qaysi klaster + qaysi foydalanuvchi" juftligi |
| **NAT** | Ichki manzillarni tashqi IP orqali ko'rsatuvchi tarmoq mexanizmi |

## 🔗 Manbalar

- [Kubernetes on Cloud Providers](https://kubernetes.io/docs/setup/production-environment/turnkey-solutions/)
- [Organizing Cluster Access Using kubeconfig](https://kubernetes.io/docs/concepts/configuration/organize-cluster-access-kubeconfig/)
- [DigitalOcean Kubernetes](https://docs.digitalocean.com/products/kubernetes/)

---
⬅️ [Oldingi dars](lesson2.md) · [Bo'lim indeksi](README.md) · ➡️ [k8s-public-ip-qollanma.md](k8s-public-ip-qollanma.md)
