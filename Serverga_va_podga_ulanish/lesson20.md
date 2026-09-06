# Node va Pod'ga ulanish usullari

> 🎯 **Bu darsda nimani o'rganamiz:**
> - Node'larning IP manzillarini topish
> - Node'ga SSH orqali kirish — qachon kerak, qachon kerak emas
> - `kubectl debug node/` bilan SSH'siz node'ni tekshirish
> - Pod ichiga kirish va `chroot /host` nima qiladi

## 💡 Hayotiy o'xshatish: uy va xonadon

Node — bu **ko'p qavatli uy**, Pod esa undagi **xonadon**.

Xonadonga kirish uchun uyning kalitini so'rashingiz shart emas — domofon
(apiserver) sizni to'g'ri xonadonga ulaydi. Uyning **podvaliga** tushish
kerak bo'lgandagina (kubelet loglari, disk to'lgani, tarmoq sozlamalari)
uy boshqaruvchisidan kalit so'raysiz.

Amalda kunlik ishning 95% xonadon darajasida bo'ladi.

## 1. Node'larning IP manzillarini ko'rish

```bash
kubectl get nodes -o wide
```

```text
NAME                STATUS   ROLES           AGE   VERSION   INTERNAL-IP      OS-IMAGE
test-server-k8s-1   Ready    control-plane   10d   v1.31.4   192.168.16.196   Ubuntu 22.04
test-server-k8s-2   Ready    <none>          10d   v1.31.4   192.168.16.197   Ubuntu 22.04
```

| Ustun | Nimani bildiradi |
|---|---|
| **STATUS** | `Ready` — node ishlayapti. `NotReady` — kubelet javob bermayapti |
| **ROLES** | `control-plane` yoki bo'sh (`<none>` — oddiy worker node) |
| **INTERNAL-IP** | Node'ning klaster ichidagi IP manzili — SSH shu manzilga |
| **VERSION** | Node'dagi kubelet versiyasi |

Faqat IP'larni olish:

```bash
kubectl get nodes -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.status.addresses[?(@.type=="InternalIP")].address}{"\n"}{end}'
```

## 2. Node'ga SSH orqali kirish

```bash
ssh root@192.168.16.197
ssh foydalanuvchi@192.168.16.197
```

minikube uchun alohida buyruq bor:

```bash
minikube ssh
```

⚠️ **SSH deyarli har doim kerak emas.** U faqat quyidagi hollarda kerak:

| Vazifa | SSH kerakmi |
|---|---|
| Pod loglarini o'qish | ❌ `kubectl logs` |
| Pod ichiga kirish | ❌ `kubectl exec` |
| Pod'ga so'rov yuborish | ❌ `kubectl port-forward` |
| kubelet servisi holatini ko'rish | ✅ `systemctl status kubelet` |
| Node diski to'lganini tekshirish | ✅ `df -h` |
| containerd konfiguratsiyasini o'zgartirish | ✅ |
| Static Pod manifestlarini tahrirlash | ✅ `/etc/kubernetes/manifests/` |

## 3. Pod ichiga kirish

Avval Pod'ning nomi va namespace'ini bilib oling:

```bash
kubectl get pods -A
```

Keyin:

```bash
kubectl exec -it -n <namespace> <pod-nomi> -- /bin/sh
```

`/bin/bash` faqat to'liq distributiv asosidagi image'larda bor. Alpine
asosidagilarda (`nginx:alpine`, `busybox`) faqat `/bin/sh` mavjud —
shuning uchun **`sh` dan boshlash xavfsizroq**.

Batafsil: [Konteynerlar_bilan_ishlash](../Konteynerlar_bilan_ishlash/).

## 4. `kubectl debug node/` — SSH'siz node'ni tekshirish

SSH kaliti bo'lmaganda yoki node bulutda bo'lib, unga bevosita kirish
yopiq bo'lganda:

```bash
kubectl debug node/test-server-k8s-2 -it --image=busybox:1.37
```

Bu buyruq node'da vaqtinchalik Pod ko'taradi. Pod:

- node'ning **host namespace'lariga** kirish huquqiga ega bo'ladi (tarmoq,
  jarayonlar);
- node'ning butun fayl tizimini o'z ichidagi **`/host`** katalogiga ulaydi.

Konteynerga kirgandan keyin node'ning o'z muhitiga o'tish:

```bash
chroot /host
```

Shundan keyin siz go'yo node'ning o'zida turgandek bo'lasiz —
`systemctl status kubelet`, `journalctl -u kubelet`, `crictl ps` kabi
buyruqlar ishlaydi.

⚠️ Bu Pod node'ga to'liq kirish huquqini beradi. Shuning uchun `debug`
huquqi RBAC'da faqat administratorlarga beriladi.

Ish tugagach vaqtinchalik Pod'ni o'chiring:

```bash
kubectl get pods -A | grep node-debugger
kubectl delete pod <node-debugger-...> -n default
```

## 🧪 Mustaqil topshiriqlar

> Taxminiy vaqt: 10 daqiqa.

**1-topshiriq · oson.** Klasteringizdagi barcha node'larning nomi va
INTERNAL-IP manzilini bitta jadval qilib chiqaring.

<details><summary>O'zingizni tekshiring</summary>

```bash
kubectl get nodes -o wide
# INTERNAL-IP ustuni to'ldirilgan bo'lishi kerak
```
</details>

**2-topshiriq · o'rta.** `kubectl debug node/` bilan node'ga kiring va
`chroot /host` dan keyin kubelet holatini tekshiring.

<details><summary>O'zingizni tekshiring</summary>

```bash
# node ichida:
systemctl is-active kubelet
# "active" chiqishi kerak
```
</details>

**3-topshiriq · qiyin.** Node'da qaysi konteynerlar ishlayotganini
`kubectl` **ishlatmasdan** ko'ring. **Avval ayting:** qaysi buyruq kerak?

<details><summary>O'zingizni tekshiring</summary>

```bash
# node ichida (chroot /host dan keyin):
crictl ps
# Docker emas, containerd ishlatilsa — crictl kerak bo'ladi
```
</details>

## ❓ Savol-Javob

**Savol:** Node `NotReady` holatida. Birinchi navbatda nimani tekshiray?
**Javob:** kubelet servisini: `systemctl status kubelet` va
`journalctl -u kubelet -n 50`. Ko'p hollarda sabab shu ikki buyruqdan
chiqadi — sertifikat eskirgan, disk to'lgan yoki CNI o'rnatilmagan.

**Savol:** `kubectl debug node/` ishlamayapti, xato beradi.
**Javob:** Bu funksiya Kubernetes 1.20 dan beri bor. Eskiroq klasterda
ishlamaydi. Shuningdek RBAC'da `pods/attach` va `pods/ephemeralcontainers`
huquqlari kerak.

**Savol:** Pod'ni ishlab turgan node'ini qanday bilaman?
**Javob:** `kubectl get pod <nom> -o wide` — `NODE` ustuni. Yoki
`kubectl get pod <nom> -o jsonpath='{.spec.nodeName}'`.

**Savol:** `chroot /host` nima uchun kerak?
**Javob:** `debug` Pod'i o'z image'idagi fayl tizimida ishlaydi. `chroot /host`
ildiz katalogini node'ning haqiqiy fayl tizimiga o'zgartiradi — shundagina
node'ning o'z buyruqlari va konfiguratsiyalari ko'rinadi.

## 📌 CKA imtihon uchun maslahat

Imtihonda node bilan ishlash masalalari deyarli har doim SSH orqali
beriladi — vazifa matnida `ssh node01` deb aniq yoziladi.

Node'da eng ko'p kerak bo'ladigan yo'llar:

```bash
/etc/kubernetes/manifests/     # static Pod manifestlari (apiserver, etcd, ...)
/var/lib/kubelet/config.yaml   # kubelet konfiguratsiyasi
/etc/kubernetes/pki/           # sertifikatlar
```

Ish tugagach **`exit` bilan o'z terminalingizga qayting** — keyingi masala
boshqa node'da bo'lishi mumkin. Bu imtihonda eng ko'p uchraydigan e'tiborsizlik.

## 📖 Asosiy atamalar

| Atama | Ma'nosi |
|---|---|
| **INTERNAL-IP** | Node'ning klaster ichidagi IP manzili |
| **`NotReady`** | Node bor, lekin kubelet apiserver bilan gaplashmayapti |
| **Host namespace** | Node'ning o'z tarmoq va jarayonlar makoni |
| **`chroot`** | Jarayon uchun ildiz katalogini almashtiruvchi buyruq |
| **`crictl`** | containerd bilan bevosita ishlash vositasi (`docker` o'rnini bosadi) |
| **Static Pod** | kubelet `/etc/kubernetes/manifests/` dan o'qib ko'taradigan Pod |

## 🔗 Manbalar

- [kubectl debug — Debugging a Node](https://kubernetes.io/docs/tasks/debug/debug-cluster/kubectl-node-debug/)
- [Troubleshooting Clusters — kubernetes.io](https://kubernetes.io/docs/tasks/debug/debug-cluster/)
- [Nodes — kubernetes.io](https://kubernetes.io/docs/concepts/architecture/nodes/)

---
⬅️ [Bo'lim indeksi](README.md) · ➡️ Keyingi bo'lim: [YAML_yaratish](../YAML_yaratish/)
