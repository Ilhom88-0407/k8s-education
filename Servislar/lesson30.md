# NodePort — node porti orqali tashqariga chiqarish

> 🎯 **Bu darsda nimani o'rganamiz:**
> - NodePort ClusterIP dan nimasi bilan farq qiladi
> - `PORT(S)` ustunidagi `8080:30690/TCP` yozuvini o'qish
> - NodePort oralig'i 30000–32767 nima uchun shunday
> - Qachon NodePort ishlatiladi, qachon ishlatilmaydi

## 💡 Hayotiy o'xshatish: binodagi yon eshik

ClusterIP — bino ichidagi ichki telefon. NodePort — **har bir binoning yon
eshigi**: ko'chadan turib istalgan binoning yon eshigidan kirib, ichkaridagi
kerakli xonaga tushishingiz mumkin.

Eshik raqami g'alati bo'ladi (30690 kabi), lekin u **har binoda bir xil** —
qaysi biriga kirsangiz ham bir joyga tushasiz.

## ClusterIP va NodePort farqi

Ikkalasi ham bir xil Deployment ustiga qo'yilgan:

**NodePort:**

```text
NAME           TYPE       CLUSTER-IP    EXTERNAL-IP   PORT(S)          AGE
nginx-deploy   NodePort   10.97.78.89   <none>        8080:30690/TCP   9s
```

**ClusterIP:**

```text
NAME           TYPE        CLUSTER-IP    EXTERNAL-IP   PORT(S)    AGE
nginx-deploy   ClusterIP   10.101.7.48   <none>        8080/TCP   44s
```

Ikki farq ko'rinadi:

1. `TYPE` ustuni;
2. `PORT(S)` da NodePort ikkita raqam ko'rsatadi: `8080:30690/TCP`.

⚠️ Diqqat: NodePort'da ham `CLUSTER-IP` bor. Chunki **NodePort ClusterIP'ni
o'z ichiga oladi** — u ClusterIP ustiga qo'shimcha kirish yo'li qo'shadi,
uni almashtirmaydi.

## `8080:30690/TCP` ni o'qish

```
8080  :  30690  / TCP
  ↑        ↑
Service   Node porti
 porti    (tashqaridan)
```

- **8080** — klaster ichidan: `http://nginx-deploy:8080`;
- **30690** — tashqaridan: `http://<istalgan-node-IP>:30690`.

Uchinchi raqam (`targetPort`) bu ustunda ko'rinmaydi — u Pod ichidagi port
va `describe` da ko'rinadi.

## NodePort Service yaratish

Avvalgi Service'ni o'chiramiz:

```bash
kubectl delete service nginx-deploy
```

Yangisini yaratamiz:

```bash
kubectl expose deployment nginx-deploy --type=NodePort --port=8080 --target-port=80
```

```text
service/nginx-deploy exposed
```

> 📁 **Tayyor fayl:** [`amaliyot/servis_yaratish/03-nodeport.yaml`](amaliyot/servis_yaratish/03-nodeport.yaml)

Manifest bilan aniq port belgilash:

```yaml
spec:
  type: NodePort
  ports:
    - port: 80
      targetPort: 80
      nodePort: 30080     # ixtiyoriy; yozmasangiz Kubernetes o'zi tanlaydi
```

## Nima uchun 30000–32767

Bu oraliq ataylab **yuqori** tanlangan: 1–1023 portlar tizim xizmatlari
uchun (SSH 22, HTTP 80, HTTPS 443), 1024–29999 esa oddiy ilovalar uchun band
bo'lishi mumkin.

Oraliqni o'zgartirish mumkin (`--service-node-port-range` bayrog'i
apiserver'da), lekin bunga deyarli hech qachon ehtiyoj bo'lmaydi.

⚠️ **Har NodePort butun klaster bo'ylab noyob.** 30080 bandmi — ikkinchi
Service uni ololmaydi.

## Sinash

```bash
kubectl get nodes -o wide          # node IP'larini olamiz
curl http://192.168.16.197:30690
```

minikube'da qulay yorliq bor:

```bash
minikube service nginx-deploy --url
minikube service nginx-deploy        # brauzerni ham ochadi
```

**Muhim:** so'rovni **istalgan** node'ga yuborishingiz mumkin — hatto Pod
o'sha node'da bo'lmasa ham. kube-proxy uni to'g'ri node'ga yo'naltiradi.

## Qachon NodePort ishlatiladi

| Holat | NodePort mosmi |
|---|---|
| Lokal sinov, demo, o'rganish | ✅ Ha |
| Ichki tarmoqdagi kichik ilova | ✅ Ha |
| Ommaviy veb-sayt | ❌ Yo'q — g'alati port raqami, TLS yo'q |
| Ko'p sayt bitta klasterda | ❌ Yo'q — Ingress kerak |

Ishlab chiqarishda odatda **Ingress** yoki **LoadBalancer** ishlatiladi.

## 🧪 Mustaqil topshiriqlar

> Taxminiy vaqt: 15 daqiqa.

**1-topshiriq · oson.** NodePort Service yarating va tayinlangan node portini
toping.

<details><summary>O'zingizni tekshiring</summary>

```bash
kubectl get svc web-nodeport -o jsonpath='{.spec.ports[0].nodePort}{"\n"}'
# 30000-32767 oralig'idagi raqam
```
</details>

**2-topshiriq · o'rta.** Node IP va NodePort orqali brauzerdan yoki `curl`
bilan nginx sahifasini oching.

<details><summary>O'zingizni tekshiring</summary>

```bash
minikube service web-nodeport --url
curl -s $(minikube service web-nodeport --url) | grep -o '<title>.*</title>'
```
</details>

**3-topshiriq · qiyin.** Ikkinchi Service yarating va unga ham `nodePort: 30080`
bering. **Avval ayting:** nima bo'ladi?

<details><summary>O'zingizni tekshiring</summary>

```bash
# Xato: provided port is already allocated
```
</details>

📁 To'liq yechimlar: [`amaliyot/servis_yaratish/YECHIM.md`](amaliyot/servis_yaratish/YECHIM.md)

## ❓ Savol-Javob

**Savol:** So'rovni Pod turgan node'ga yuborishim shartmi?
**Javob:** Yo'q. Istalgan node javob beradi — kube-proxy so'rovni kerakli
node'ga o'zi uzatadi.

**Savol:** NodePort'da HTTPS qanday qilinadi?
**Javob:** NodePort'ning o'zida TLS yo'q. TLS uchun Ingress yoki
LoadBalancer + sertifikat kerak.

**Savol:** `externalTrafficPolicy: Local` nima qiladi?
**Javob:** So'rovni faqat **o'sha node'dagi** Pod'ga yuboradi. Mijozning
haqiqiy IP'sini saqlab qoladi, lekin node'da Pod bo'lmasa so'rov yo'qoladi.

**Savol:** NodePort Service'ni tashqi tarmoqdan ochish xavfsizmi?
**Javob:** Portni to'g'ridan-to'g'ri internetga ochmang. Uning oldiga
firewall yoki tashqi balanslovchi qo'ying.

## 📌 CKA imtihon uchun maslahat

```bash
kubectl expose deploy web --type=NodePort --port=80
kubectl create service nodeport web --tcp=80:80 --node-port=30080
```

Imtihonda `nodePort` aniq raqam bilan so'ralsa, `kubectl expose` yetmaydi —
manifest yozing yoki `kubectl edit svc <nom>` bilan qo'shing.

Tekshirish:

```bash
kubectl get svc -o wide
curl http://$(kubectl get node -o jsonpath='{.items[0].status.addresses[0].address}'):30080
```

## 📖 Asosiy atamalar

| Atama | Ma'nosi |
|---|---|
| **NodePort** | Har node'ning IP va yuqori porti orqali ochadigan Service turi |
| **NodePort oralig'i** | 30000–32767; klaster bo'ylab noyob |
| **`nodePort`** | Aniq port raqamini qo'lda belgilovchi maydon |
| **`externalTrafficPolicy`** | `Cluster` (standart) yoki `Local` — so'rov qaysi Pod'ga borishini belgilaydi |

## 🔗 Manbalar

- [Service Type NodePort](https://kubernetes.io/docs/concepts/services-networking/service/#type-nodeport)
- [Source IP for Services](https://kubernetes.io/docs/tutorials/services/source-ip/)
- [minikube service](https://minikube.sigs.k8s.io/docs/commands/service/)

---
⬅️ [Oldingi dars](service_ClusterIP.md) · [Bo'lim indeksi](README.md) · ➡️ [lesson31.md](lesson31.md)
