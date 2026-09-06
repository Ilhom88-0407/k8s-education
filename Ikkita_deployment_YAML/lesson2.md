# Ikkita deployment yaratish plani

> 🎯 **Bu darsda nimani o'rganamiz:**
> - Ilova kodida boshqa servisga qanday murojaat qilinadi
> - `/nginx` yo'li ichkarida nima qiladi
> - Xatolarni ushlash nima uchun muhim

# Bu rasmda ikkita deployment yaratilganligini ko'rishimiz mumkin

1. deployment <k8s-web-to-ngnix>
2. deployment <nginx>

# shu bilan birgalikda 1 ta CluserIP servis

# K8S clusterIP
# LoadBalancer

# shu kabi xizmatlarni ishga tushirib ko'rib chiqamiz.  

1 - deployment <k8s-web-to-ngnix> da biz quyidagi <k8s-web-to-ngnix> katalogidagi index.mjs dan foydalanamiz
```js
import express from 'express'
import os from 'os'

const app = express()
const PORT = 3000

app.get("/", (req, res) => {
  const helloMessage = `<h1>Hello from the ${os.hostname()}</h1>`
  console.log(helloMessage)
  res.send(helloMessage)
})

app.get("/nginx", async (req, res) => {
  const url = 'http://nginx'
  const response = await fetch(url);
  const body = await response.text();
  res.send(body)
})

app.get("/jsonplaceholder", async (req, res) => {
  const url = "https://jsonplaceholder.typicode.com/todos";
  const response = await fetch(url);
  const body = await response.text();
  res.setHeader("Content-Type", "application/json");
  res.send(body);
});

app.listen(PORT, () => {
  console.log(`Web server is listening at port ${PORT}`)
})
```

- express → server yaratish uchun framework.
- os → kompyuter/server haqida ma'lumot olish uchun modul.
- app → Express ilovasi.
- PORT → Server 3000-portda ishlaydi.

- / route
```javascript
app.get("/", (req, res) => {
```
Browserda / ochilganda ishlaydi.
```javascript
const helloMessage = `<h1>Hello from the ${os.hostname()}</h1>`
res.send(helloMessage)
```
Server nomini (hostname) olib HTML ko'rinishda chiqaradi va javob yuboradi.

Misol:
```text
Hello from the ubuntu-server
```
- /nginx route
```javascript
app.get("/nginx", async (req, res) => {
```
Bu route boshqa service'ga request yuboradi.

Misol:
```
Hello from the nginx
```
const url = 'http://nginx'
const response = await fetch(url);
```
nginx nomli container/serverga so'rov yuboradi. bu degani ikkinchu deploymentda nginx nomli container/server yaratilganligini ko'rib chiqamiz.
```
const body = await response.text();
res.send(body)
```
Kelgan javobni foydalanuvchiga qaytaradi.

Ko'pincha Docker Compose'da ishlatiladi.

- /jsonplaceholder route
```
const url = "https://jsonplaceholder.typicode.com/todos";
```
- Test API'dan ma'lumot oladi.
```
const response = await fetch(url);
```
API'ga request yuboradi.
```
res.setHeader("Content-Type", "application/json");
```
- Javob JSON ekanini bildiradi.
```
res.send(body);
```
JSON ma'lumotni qaytaradi.

Bu loyiha:

Express server yaratadi
Route'lar bilan ishlaydi
Boshqa API'larga request yuboradi
JSON va HTML response qaytaradi
Docker/Nginx bilan ishlashga mos yozilgan

### Endi bo'lsa yaratdan proyekni docker hub ga yuklaymiz:
1. direktoriyaga o'tamiz
```bash 
cd .\k8s-web-to-nginx\
```
2. Docker Hub ga yuklash uchun quyidagi buyruqni bajarishimiz kerak:
```bash
docker build -t k8s-web-to-nginx .mrpocker88/k8s-web-to-nginx
```
3. Docker Hub ga yuklash uchun quyidagi buyruqni bajarishimiz kerak:
```bash
docker push k8s-web-to-nginx
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
⬅️ [Bo'lim indeksi](README.md) · ➡️ [lesson4.md](lesson4.md)
