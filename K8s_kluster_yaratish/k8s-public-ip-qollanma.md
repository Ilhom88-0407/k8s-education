# Kubernetes API Server'ga Public IP (NAT) Orqali Ulanish

> **Maqsad:** `kubeadm` yordamida o'rnatilgan Kubernetes klasterga tashqi (NAT) IP manzili orqali xavfsiz `kubectl` ulanishini sozlash.

---

## 📋 Mundarija

- [Muammoning tasviri](#muammoning-tasviri)
- [Tashxis](#tashxis)
- [Yechim — bosqichma-bosqich](#yechim--bosqichma-bosqich)
  - [1-bosqich: Zaxira nusxa](#1-bosqich-zaxira-nusxa)
  - [2-bosqich: Sertifikatni qayta yaratish](#2-bosqich-sertifikatni-qayta-yaratish)
  - [3-bosqich: API server pod'ini restart qilish](#3-bosqich-api-server-podini-restart-qilish)
  - [4-bosqich: ConfigMap'ni yangilash](#4-bosqich-configmapni-yangilash)
  - [5-bosqich: Tekshirish](#5-bosqich-tekshirish)
- [Mumkin bo'lgan xatolar](#mumkin-bolgan-xatolar)
- [Foydali buyruqlar](#foydali-buyruqlar)

---

## Muammoning tasviri

Klaster Private IP (`192.168.16.196`) ga o'rnatilgan, lekin tashqaridan Public IP (`194.107.115.75`) orqali ulanish kerak. Standart `kubectl` ulanishida quyidagi xatolik chiqadi:

```
Unable to connect to the server: tls: failed to verify certificate:
x509: certificate is valid for 10.96.0.1, 192.168.16.196,
not 194.107.115.75
```

**Sabab:** `kube-apiserver` sertifikati faqat ichki IP manzillar uchun yaratilgan. Tashqi IP `Subject Alternative Name (SAN)` ro'yxatida yo'q.

---

## Tashxis

Joriy sertifikatdagi SAN'larni ko'rish:

```bash
sudo openssl x509 -in /etc/kubernetes/pki/apiserver.crt -noout -text | grep -A2 "Subject Alternative Name"
```

**Avvalgi natija** (xato):
```
X509v3 Subject Alternative Name:
    DNS:kubernetes, ..., IP Address:10.96.0.1, IP Address:192.168.16.196
```

Public IP yo'q — qo'shish kerak.

---

## Yechim — bosqichma-bosqich

> **Eslatma:** Barcha buyruqlar **master node** ustida `root` huquqlari bilan bajariladi.

### 1-bosqich: Zaxira nusxa

Har qanday muammo yuz berganda qaytarib olish uchun PKI papkasini zaxiralang:

```bash
sudo cp -r /etc/kubernetes/pki /etc/kubernetes/pki.backup.$(date +%F)
```

Tekshirish:
```bash
ls -la /etc/kubernetes/ | grep pki
```

### 2-bosqich: Sertifikatni qayta yaratish

Eski sertifikat va kalitni o'chirib, yangisini Public IP bilan yarating:

```bash
# Eski sertifikatni o'chirish
sudo rm /etc/kubernetes/pki/apiserver.crt /etc/kubernetes/pki/apiserver.key

# Yangi sertifikatni Public IP bilan yaratish
sudo kubeadm init phase certs apiserver --apiserver-cert-extra-sans=194.107.115.75
```

**Kutilgan natija:**
```
[certs] apiserver serving cert is signed for DNS names [kubernetes ...]
       and IPs [10.96.0.1 192.168.16.196 194.107.115.75]
```

Tekshirish:
```bash
sudo openssl x509 -in /etc/kubernetes/pki/apiserver.crt -noout -text | grep -A2 "Subject Alternative Name"
```

Endi `194.107.115.75` ham ro'yxatda bo'lishi kerak. ✅

### 3-bosqich: API server pod'ini restart qilish

Yangi sertifikatni qabul qilishi uchun `kube-apiserver` static pod'ini qayta yuklang:

**Variant A** — manifest faylini vaqtincha ko'chirish (ishonchli usul):

```bash
sudo mv /etc/kubernetes/manifests/kube-apiserver.yaml /tmp/
sleep 20
sudo mv /tmp/kube-apiserver.yaml /etc/kubernetes/manifests/
```

**Variant B** — konteynerni to'g'ridan-to'g'ri o'chirish:

```bash
sudo crictl rm -f $(sudo crictl ps -q --name kube-apiserver)
sleep 30
```

`kubelet` o'zi yangi konteynerni ko'taradi.

Tekshirish:
```bash
sudo crictl ps | grep apiserver
```

`Running` holatida ko'rinishi kerak.

### 4-bosqich: ConfigMap'ni yangilash

Bu kelajakdagi `kubeadm upgrade` operatsiyalarida SAN ro'yxati saqlanib qolishi uchun zarur:

```bash
sudo kubectl --kubeconfig=/etc/kubernetes/admin.conf -n kube-system edit configmap kubeadm-config
```

`apiServer: {}` qatorini quyidagicha **almashtiring**:

```yaml
    apiServer:
      certSANs:
      - 194.107.115.75
      - 192.168.16.196
      - 10.96.0.1
      - kubernetes
      - kubernetes.default
      - kubernetes.default.svc
      - kubernetes.default.svc.cluster.local
```

> ⚠️ **YAML qoidalari:**
> - **2 ta probel** indentatsiya, TAB **ishlatmang**
> - `{}` belgisini olib tashlang
> - `-` belgisi list elementi sifatida `certSANs:` dan ichkariroqda turishi kerak

Saqlash va chiqish (`:wq` vim'da, `Ctrl+O` keyin `Ctrl+X` nano'da).

Tasdiqlash:
```bash
sudo kubectl --kubeconfig=/etc/kubernetes/admin.conf -n kube-system get cm kubeadm-config -o yaml | grep -A 10 apiServer
```

### 5-bosqich: Tekshirish

**Server tomonidan:**
```bash
sudo kubectl --kubeconfig=/etc/kubernetes/admin.conf get nodes
sudo kubectl --kubeconfig=/etc/kubernetes/admin.conf -n kube-system get pods
```

**Mijoz tomonidan (Windows/Linux/Mac):**

`~/.kube/config` (yoki `C:\Users\admin\.kube\config`) faylida server manzili Public IP bo'lishi kerak:
```yaml
clusters:
- cluster:
    server: https://194.107.115.75:6443
    certificate-authority-data: <base64>
  name: kubernetes
```

Ulanishni tekshiring:
```bash
kubectl get nodes
kubectl cluster-info
```

✅ **Tayyor!**

---

## Mumkin bo'lgan xatolar

### Xato 1: "connection refused"

```
The connection to the server 192.168.16.196:6443 was refused
```

**Sabab:** `kube-apiserver` hali to'liq ishga tushmagan.

**Yechim:** 30-60 soniya kuting va `sudo crictl ps | grep apiserver` orqali holatni tekshiring. Konteyner `Running` bo'lishi kerak.

### Xato 2: ConfigMap o'zgarmagan

Agar `kubeadm init phase certs apiserver` (flag siz) bajarilganda Public IP qo'shilmasa — bu ConfigMap'da `certSANs` saqlanmaganligini bildiradi.

**Yechim:** Doim `--apiserver-cert-extra-sans=194.107.115.75` flag bilan ishlating yoki ConfigMap'ni qaytadan, e'tibor bilan tahrirlang.

### Xato 3: Tashqi portga ulanmayapti

```
dial tcp 194.107.115.75:6443: connection refused
```

(TLS xatosi emas, TCP-darajadagi xato)

**Tekshirish:**
```bash
# Server tinglayaptimi?
sudo ss -tlnp | grep 6443

# Tashqaridan port ochiqligi (boshqa mashinadan):
# Linux:   nc -zv 194.107.115.75 6443
# Windows: Test-NetConnection 194.107.115.75 -Port 6443
```

**Yechim:** NAT qiluvchi gateway'da `194.107.115.75:6443 → 192.168.16.196:6443` DNAT qoidasi va firewall'da `6443/tcp` port ruxsati borligini tasdiqlang.

### Xato 4: Sertifikat eski cache'da

Mijoz tomonida sertifikat o'zgarmasligi kerak — chunki CA bir xil. Lekin agar `~/.kube/config` faylida eski `certificate-authority-data` bo'lsa, uni serverdan yangilangan `admin.conf` dan ko'chirib oling:

```bash
sudo cat /etc/kubernetes/admin.conf
```

---

## Foydali buyruqlar

### Sertifikat ma'lumotlarini ko'rish

```bash
# Faqat SAN ro'yxati
sudo openssl x509 -in /etc/kubernetes/pki/apiserver.crt -noout -text | grep -A2 "Subject Alternative Name"

# To'liq sertifikat ma'lumoti
sudo openssl x509 -in /etc/kubernetes/pki/apiserver.crt -noout -text

# Sertifikat amal qilish muddati
sudo openssl x509 -in /etc/kubernetes/pki/apiserver.crt -noout -dates

# Barcha sertifikatlar muddati (kubeadm)
sudo kubeadm certs check-expiration
```

### Static pod monitoring

```bash
# Static pod fayllari
ls -la /etc/kubernetes/manifests/

# Hozir ishlayotgan konteynerlar
sudo crictl ps

# Yaqinda to'xtagan konteynerlar
sudo crictl ps -a | head -20

# Konteyner loglari
sudo crictl logs <container_id>

# Kubelet loglari
sudo journalctl -u kubelet -n 50 --no-pager
```

### Qayta ishga tushirish

```bash
# kubelet restart (ehtiyot bo'ling — barcha pod'larni ta'sir qiladi)
sudo systemctl restart kubelet

# Faqat apiserver konteynerni restart qilish
sudo crictl rm -f $(sudo crictl ps -q --name kube-apiserver)
```

### ConfigMap bilan ishlash

```bash
# kubeadm-config'ni ko'rish
sudo kubectl --kubeconfig=/etc/kubernetes/admin.conf -n kube-system get cm kubeadm-config -o yaml

# Backup
sudo kubectl --kubeconfig=/etc/kubernetes/admin.conf -n kube-system get cm kubeadm-config -o yaml > kubeadm-config-backup.yaml

# Tahrirlash
sudo kubectl --kubeconfig=/etc/kubernetes/admin.conf -n kube-system edit cm kubeadm-config
```

---

## Qo'shimcha

### Xavfsizlik bo'yicha eslatma

- API server'ni Internet'ga to'g'ridan-to'g'ri ochish **xavfli**. Quyidagilarni qo'llang:
  - **Firewall** orqali faqat ma'lum IP manzillarga ruxsat bering
  - **VPN** orqali ulanish maqbul yechim
  - **`insecure-skip-tls-verify: true`** ni production'da **hech qachon** ishlatmang

### Sertifikat muddati

Standart `kubeadm` sertifikatlarining amal qilish muddati — **1 yil**. Yangilash:

```bash
sudo kubeadm certs renew all
sudo systemctl restart kubelet
```

---

> 📅 **Sana:** 2026-yil 13-may
>
> 🖥 **Klaster:** kubeadm v1.35.4, Calico CNI
>
> 🌐 **Konfiguratsiya:** Private IP `192.168.16.196` ↔ NAT ↔ Public IP `194.107.115.75`
