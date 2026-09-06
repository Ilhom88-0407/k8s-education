# Endi bo'lsa biz yaratgan deployment uchun service yaratamiz va podlarni sonini5 ga ko'paytiramiz (scaling):

> 🎯 **Bu darsda nimani o'rganamiz:**
> - O'z ilovangiz uchun Service yaratish
> - Pod'lar sonini oshirish va yukning taqsimlanishini ko'rish
```bash
kubectl expose deployment k8s-web-hello --type=LoadBalancer --port=3333 --target-port=3000
service/k8s-web-hello exposed
```
Servis ishga tushganini tekshirish uchun quyidagi buyruqni bajarishimiz kerak:
```bash
kubectl get services
```
endi bo'lsa biz deployment'ni scaling qilamiz, ya'ni podlar sonini 5 ga ko'paytiramiz:
```bash
kubectl scale deployment k8s-web-hello --replicas=5
deployment.apps/k8s-web-hello scaled
```
tekshirish uchun man NodePort dan foydalangan xolda brauzerda http://<node_ip>:31990 manziliga kiramiz va biz 5 ta podning ishga tushganini ko'rishimiz mumkin.
Biz yaratgan servis LoadBalancer nizning Cloudda ishlamaganligi sababli biz LoadBalancer servisi orqali ishga tushirilgan servisni imkoni bo'lmadi.

## 🧪 Mustaqil topshiriqlar

> Taxminiy vaqt: 15 daqiqa.

**1-topshiriq · oson.** Deployment'ni 5 replikaga masshtablang.

<details><summary>O'zingizni tekshiring</summary>

```bash
kubectl get deployment k8s-web-hello -o jsonpath='{.status.readyReplicas}{"\n"}'
```
</details>

**2-topshiriq · o'rta.** Service orqali sahifani 10 marta oching va
javobdagi Pod nomi o'zgarayotganini ko'ring.

<details><summary>O'zingizni tekshiring</summary>

```bash
for i in $(seq 10); do curl -s http://<SERVICE-URL> | grep -o 'k8s-web-hello-[a-z0-9-]*'; done | sort -u
# Bir nechta har xil Pod nomi chiqishi kerak
```
</details>

**3-topshiriq · qiyin.** Bitta Pod'ni o'chiring va so'rovlar davom
etayotganini tekshiring. **Avval ayting:** biror so'rov yo'qoladimi?

<details><summary>O'zingizni tekshiring</summary>

Pod `Terminating` holatiga o'tgan zahoti Service uni Endpoints
ro'yxatidan chiqaradi — shuning uchun yangi so'rovlar unga bormaydi.
</details>

## ❓ Savol-Javob

**Savol:** So'rovlar Pod'lar orasida teng taqsimlanadimi?
**Javob:** kube-proxy iptables rejimida tasodifiy tanlaydi — ko'p
so'rovda taqsimot tenglashadi, lekin har 3 so'rovda aniq 1-2-3 bo'lmaydi.

**Savol:** Bir mijoz doim bitta Pod'ga tushishini xohlasam?
**Javob:** `spec.sessionAffinity: ClientIP` qo'ying.

## 📖 Asosiy atamalar

| Atama | Ma'nosi |
|---|---|
| **Image** | Ilova va uning muhitidan iborat o'zgarmas qolip |
| **Konteyner** | Ishga tushirilgan image nusxasi |
| **Dockerfile** | Image qanday qurilishini tasvirlovchi fayl |
| **Registry** | Image'lar saqlanadigan omborxona (Docker Hub, GHCR, ECR) |
| **Teg (tag)** | Image versiyasini bildiruvchi belgi: `:1.0.3` |
| **Qatlam (layer)** | Dockerfile'ning har bir buyrug'i hosil qiladigan bo'lak |

## 🔗 Manbalar

- [Dockerfile reference](https://docs.docker.com/reference/dockerfile/)
- [Images — kubernetes.io](https://kubernetes.io/docs/concepts/containers/images/)
- [Node.js Docker best practices](https://github.com/nodejs/docker-node/blob/main/docs/BestPractices.md)

---
⬅️ [Oldingi dars](lesson4.md) · [Bo'lim indeksi](README.md) · ➡️ Keyingi bo'lim: [Dasturni_yangilash](../Dasturni_yangilash/)
