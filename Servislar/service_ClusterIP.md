# ClusterIP — klaster ichidagi barqaror manzil

> 🎯 **Bu darsda nimani o'rganamiz:**
> - ClusterIP Service yaratish va uni sinash
> - `port` va `targetPort` boshqa-boshqa bo'lishi
> - ClusterIP manzili qayerdan olinadi
> - DNS nomi orqali murojaat qilish

## 💡 Hayotiy o'xshatish: ofis qabulxonasi

Qabulxona raqami hech qachon o'zgarmaydi. Xodimlar ishga kelib-ketaveradi,
xonalari almashadi — lekin siz doim bitta raqamga qo'ng'iroq qilasiz va
sizni kerakli odamga ulashadi.

ClusterIP — o'sha qabulxona. Faqat u **ofis ichidagilar uchun**: ko'chadan
turib bu raqamni ola olmaysiz.

## ClusterIP Service yaratish

```bash
kubectl expose deploy nginx-deploy --port=8080 --target-port=80
```

```text
service/nginx-deploy exposed
```

Bu buyruqda:

- `--port=8080` — **Service** 8080-portda tinglaydi;
- `--target-port=80` — so'rov Pod'ning **80-portiga** uzatiladi.

Ikkisi boshqa-boshqa bo'lishi mumkin va bu ko'p ishlatiladi: ilova ichida
80-portda ishlaydi, tashqarida esa boshqa raqam ostida ko'rinadi.

> 📁 **Tayyor fayl:** [`amaliyot/servis_yaratish/02-clusterip.yaml`](amaliyot/servis_yaratish/02-clusterip.yaml)

## Natijani tekshirish

```bash
kubectl get services
```

```text
NAME           TYPE        CLUSTER-IP    EXTERNAL-IP   PORT(S)    AGE
kubernetes     ClusterIP   10.96.0.1     <none>        443/TCP    117s
nginx-deploy   ClusterIP   10.101.7.48   <none>        8080/TCP   44s
```

`CLUSTER-IP: 10.101.7.48` — Service'ga **avtomatik** berilgan manzil. U
klasterning Service tarmog'idan (odatda `10.96.0.0/12`) olinadi va
Service o'chirilmaguncha **o'zgarmaydi**.

`EXTERNAL-IP: <none>` — bu normal. ClusterIP turi tashqi manzil olmaydi.

## Sinash

Node'ning o'zida turib:

```bash
curl http://10.101.7.48:8080
```

```text
<!DOCTYPE html>
<html>
<head>
<title>Welcome to nginx!</title>
...
<h1>Welcome to nginx!</h1>
<p>If you see this page, nginx is successfully installed and working.</p>
...
```

Node'ga kira olmasangiz — vaqtinchalik Pod ochib:

```bash
kubectl run t --rm -it --image=curlimages/curl:8.10.1 --restart=Never \
  -- curl -s http://10.101.7.48:8080
```

## IP emas, DNS nomini ishlating

ClusterIP barqaror, lekin Service qayta yaratilsa u ham o'zgaradi. Shuning
uchun kodda **IP emas, nom** yoziladi:

```bash
curl http://nginx-deploy:8080
```

Kubernetes'ning ichki DNS'i (CoreDNS) har Service uchun nom yaratadi:

| Qayerdan chaqirilyapti | Yoziladigan manzil |
|---|---|
| Bir xil namespace'dan | `nginx-deploy` |
| Boshqa namespace'dan | `nginx-deploy.default` |
| To'liq shakl | `nginx-deploy.default.svc.cluster.local` |

DNS ishlayotganini tekshirish:

```bash
kubectl run t --rm -it --image=busybox:1.37 --restart=Never \
  -- nslookup nginx-deploy
```

## 🧪 Mustaqil topshiriqlar

> Taxminiy vaqt: 15 daqiqa.

**1-topshiriq · oson.** ClusterIP Service yarating: `port=9090`,
`targetPort=80`. Service'ning ClusterIP manzilini toping.

<details><summary>O'zingizni tekshiring</summary>

```bash
kubectl get svc web-mashq -o jsonpath='{.spec.clusterIP}:{.spec.ports[0].port}{"\n"}'
```
</details>

**2-topshiriq · o'rta.** Boshqa Pod'dan Service'ga **DNS nomi** orqali so'rov
yuboring va nginx sahifasini oling.

<details><summary>O'zingizni tekshiring</summary>

```bash
kubectl run t --rm -it --image=curlimages/curl:8.10.1 --restart=Never \
  -- curl -s http://web-mashq:9090 | grep -o '<title>.*</title>'
```
</details>

**3-topshiriq · qiyin.** O'z kompyuteringiz brauzeridan ClusterIP manziliga
kiring. **Avval ayting:** ishlaydimi? Nima uchun? Ishlamasa, qanday qilib
baribir ko'rish mumkin?

<details><summary>O'zingizni tekshiring</summary>

```bash
kubectl port-forward service/web-mashq 8080:9090
# endi http://localhost:8080 ochiladi
```
</details>

📁 To'liq yechimlar: [`amaliyot/servis_yaratish/YECHIM.md`](amaliyot/servis_yaratish/YECHIM.md)

## ❓ Savol-Javob

**Savol:** ClusterIP manzilini o'zim tanlasam bo'ladimi?
**Javob:** Ha, `spec.clusterIP` maydonida — lekin u Service tarmog'i
oralig'ida va band bo'lmasligi kerak. Odatda kerak emas.

**Savol:** `clusterIP: None` nima qiladi?
**Javob:** Bu **headless Service**. Unga IP berilmaydi, DNS so'rovi esa
to'g'ridan-to'g'ri Pod IP'larini qaytaradi. StatefulSet'lar uchun ishlatiladi.

**Savol:** ClusterIP'ga o'z kompyuterimdan kira olamanmi?
**Javob:** Yo'q. U klaster ichidagi manzil. Tashqaridan ko'rish uchun
`kubectl port-forward`, NodePort yoki LoadBalancer kerak.

**Savol:** Bir Deployment'ga bir necha Service qo'ysam bo'ladimi?
**Javob:** Ha, bemalol. Masalan bittasi ichki (ClusterIP), ikkinchisi tashqi
(LoadBalancer) — ikkalasi ham bir xil Pod'larga ishora qiladi.

## 📌 CKA imtihon uchun maslahat

ClusterIP — `--type` berilmaganda **standart tur**:

```bash
kubectl expose deploy web --port=80              # ClusterIP bo'ladi
kubectl create service clusterip web --tcp=80:80 # Deployment'siz ham
```

Service ishlayotganini imtihonda tez tekshirish:

```bash
kubectl run t --rm -it --image=busybox:1.37 --restart=Never -- wget -qO- http://web:80
```

## 📖 Asosiy atamalar

| Atama | Ma'nosi |
|---|---|
| **ClusterIP** | Standart Service turi; faqat klaster ichidan ko'rinadi |
| **Service tarmog'i** | ClusterIP'lar ajratiladigan IP oralig'i (odatda `10.96.0.0/12`) |
| **Headless Service** | `clusterIP: None`; DNS to'g'ridan-to'g'ri Pod IP'larini qaytaradi |
| **CoreDNS** | Klasterning ichki DNS serveri |
| **FQDN** | To'liq DNS nomi: `<svc>.<ns>.svc.cluster.local` |

## 🔗 Manbalar

- [Service Types — ClusterIP](https://kubernetes.io/docs/concepts/services-networking/service/#type-clusterip)
- [DNS for Services and Pods](https://kubernetes.io/docs/concepts/services-networking/dns-pod-service/)
- [Headless Services](https://kubernetes.io/docs/concepts/services-networking/service/#headless-services)

---
⬅️ [Oldingi dars](servis_yaratish.md) · [Bo'lim indeksi](README.md) · ➡️ [lesson30.md](lesson30.md)
