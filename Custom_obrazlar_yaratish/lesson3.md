# NodeJS ilovasi uchun Dockerfile yozish

> 🎯 **Bu darsda nimani o'rganamiz:**
> - Dockerfile buyruqlari: FROM, WORKDIR, COPY, RUN, EXPOSE, CMD
> - Qatlamlar tartibi build tezligiga qanday ta'sir qiladi
> - Nima uchun base image versiya tegi bilan yoziladi
> - Image'ni qurish va Docker Hub'ga yuklash
Dockerfile yaratamiz. Dockerfile bu bizning dasturimiz uchun Docker image yaratish uchun kerak bo'lgan ko'rsatmalarni o'z ichiga olgan fayl. Biz Dockerfile ni k8s-web-hello papkasida yaratamiz va unga quyidagi kodni yozamiz:
```bash
root@test-server-k8s-1:~# nano Dockerfile
```
Dockerfile ni yaratganimizdan so'ng, unga quyidagi kodni yozamiz:
```Dockerfile
# Base image sifatida NodeJS ni tanlaymiz
FROM node:18    
# Ishchi katalogni yaratamiz
WORKDIR /app
# package.json va package-lock.json fayllarini ishchi katalogga nusxalash
COPY package*.json ./
# Express kutubxonasini o'rnatamiz
RUN npm install
# Barcha fayllarni ishchi katalogga nusxalash
COPY . ./
# Dasturimizni 3000 portda ishga tushiramiz
EXPOSE 3000
# Dasturimizni ishga tushirish uchun buyruq
CMD ["npm", "start"]
```
Bu Dockerfile da biz node:18 image ni bazaviy image sifatida tanlaymiz. Keyin biz ishchi katalogni /app deb belgilaymiz va package.json va package-lock.json fayllarini ishchi katalogga nusxalaymiz. Keyin npm install buyrug'ini bajarib, express kutubxonasini o'rnatamiz. Keyin biz barcha fayllarni ishchi katalogga nusxalaymiz va dasturimizni 3000 portda ishga tushiramiz. Oxirida esa npm start buyrug'ini bajarib, dasturimizni ishga tushiramiz.
Endi biz Dockerfile ni yaratdik, endi biz Docker image ni yaratishimiz kerak. Docker image ni yaratish uchun quyidagi buyruqni bajarishimiz kerak:
```bash
docker build -t k8s-web-hello:1.0.0 .
``` 
Bu buyruq Dockerfile ni o'qib, k8s-web-hello:1.0.0 nomli Docker image ni yaratadi. Endi biz Docker image ni yaratdik, biz uni Docker Hub ga yuklashimiz kerak. Docker Hub bu Docker image larni saqlash va ulashish uchun mo'ljallangan bulutli platformadir. Docker Hub ga yuklash uchun quyidagi buyruqni bajarishimiz kerak:
```bash
docker tag k8s-web-hello:1.0.0 <dockerhub_username>/k8s-web-hello:1.0.0
docker push <dockerhub_username>/k8s-web-hello:1.0.0
```
Bu buyruqlar birinchi navbatda Docker image ni <dockerhub_username>/k8s-web-hello:1.0.0 nomi bilan belgilaydi va keyin uni Docker Hub ga yuklaydi. Endi biz Docker image ni yaratdik va uni Docker Hub ga yukladik, endi biz Kubernetes klasterimizda bu image ni ishlatishimiz mumkin.
Biz <docker push> bajarganimizda quyidagi ma'lumotlarni ko'ramiz:
```bash
PS D:\project AI\k8s\Custom_obrazlar_yaratish\k8s-web-hello> docker push mrpocker88/k8s:ver1
The push refers to repository [docker.io/<dockerhub_username>/k8s-web-hello]
e433a8ee85c6: Waiting 
8021d3ef7423: Waiting 
cfac36f8abc1: Waiting 
a91cbc26aaf5: Waiting 
955ff8363abc: Waiting 
6a0ac1617861: Waiting 
8144736fd000: Waiting 
90014ec3ccc9: Waiting 
03daade08b05: Waiting 
82b0198afa7a: Pushed 
1024cb31288e: Layer already exists 
468c64bb1a5a: Layer already exists 
38894dc3cd34: Pushed 
64aa1333f5a0: Layer already exists 
1c3a93350d1d: Layer already exists 
782c5d76b773: Layer already exists 
d17f077ada11: Layer already exists
```
docker push <dockerhub_username>/k8s-web-hello:1.0.0 ushbu buyruqni bajarishdan oldin, siz Docker Hub ga login qilgan bo'lishingiz kerak. Agar siz hali login qilmagan bo'lsangiz, quyidagi buyruqni bajarib, Docker Hub ga login qilishingiz mumkin:
```bash
docker login
```
Agarda biz barcha teglarni docker push qilishni xohlasak, quyidagi buyruqni bajarishimiz mumkin:
```bash
docker push <dockerhub_username>/k8s-web-hello:*
yoki 
docker push <dockerhub_username>/k8s-web-hello --all-tags
```

## ⚠️ Darsdagi Dockerfile eskirgan

Yuqorida `FROM node:18` yozilgan. **Node.js 18 qo'llab-quvvatlashdan
chiqqan** — unga xavfsizlik yangilanishlari kelmaydi.

`amaliyot/` dagi tayyor fayl yangilangan:

> 📁 [`amaliyot/k8s-web-hello/Dockerfile`](amaliyot/k8s-web-hello/Dockerfile)

```dockerfile
FROM node:22-alpine

WORKDIR /app

COPY package.json package-lock.json ./
RUN npm ci --omit=dev

COPY . ./

EXPOSE 3000
CMD ["npm", "start"]
```

Uchta farq bor:

| Nima o'zgardi | Nima uchun |
|---|---|
| `node:18` → `node:22-alpine` | 18 eskirgan; `alpine` variant ~10 barobar kichik |
| `npm install` → `npm ci --omit=dev` | `ci` lockfile'ga qat'iy amal qiladi — build takrorlanadigan bo'ladi |
| `COPY package*.json` avval, kod keyin | Kod o'zgarganda `npm ci` qatlami kesh'dan olinadi |

## Qatlamlar keshi — nima uchun tartib muhim

Docker har buyruqni alohida **qatlam** qilib saqlaydi. Qatlam o'zgarmasa,
u kesh'dan olinadi.

```dockerfile
COPY package.json package-lock.json ./   # kamdan-kam o'zgaradi
RUN npm ci --omit=dev                    # -> kesh'dan olinadi
COPY . ./                                # har o'zgarishda yangilanadi
```

Agar `COPY . ./` ni yuqoriga qo'ysangiz, kodning bitta harfini
o'zgartirganingizda ham `npm ci` boshidan ishlaydi — bu har build'da
qo'shimcha daqiqalar.

## 🧪 Mustaqil topshiriqlar

> Taxminiy vaqt: 20 daqiqa.

**1-topshiriq · oson.** Image'ni qurib, hajmini o'lchang.

<details><summary>O'zingizni tekshiring</summary>

```bash
cd amaliyot/k8s-web-hello
docker build -t k8s-web-hello:1.0.3 .
docker images k8s-web-hello
```
</details>

**2-topshiriq · o'rta.** `node:22-alpine` va `node:22` bilan qurib,
hajmlarni solishtiring.

<details><summary>O'zingizni tekshiring</summary>

```bash
docker images | grep k8s-web-hello
# alpine ~150 MB, to'liq variant ~1.1 GB atrofida
```
</details>

**3-topshiriq · qiyin.** `COPY . ./` ni `RUN npm ci` dan **oldinga**
ko'chiring va kodni o'zgartirib qayta quring. **Avval ayting:** build
tezroqmi yoki sekinroq?

<details><summary>O'zingizni tekshiring</summary>

```bash
time docker build -t sinov .
# Sekinroq: npm ci endi har safar boshidan ishlaydi
```
</details>

## ❓ Savol-Javob

**Savol:** `EXPOSE 3000` portni ochadimi?
**Javob:** Yo'q. U faqat hujjat — "bu konteyner shu portda tinglaydi".
Portni ochish uchun `docker run -p 3000:3000` yoki Kubernetes'da Service kerak.

**Savol:** `CMD` va `ENTRYPOINT` farqi nima?
**Javob:** `CMD` — standart buyruq, `docker run` da uni almashtirish oson.
`ENTRYPOINT` — doim bajariladigan qism, `CMD` unga argument bo'lib qo'shiladi.

**Savol:** `alpine` variantida muammo bo'ladimi?
**Javob:** Ba'zan. Alpine `musl` libc ishlatadi (`glibc` emas), shuning
uchun ba'zi native modullar qayta kompilyatsiya talab qiladi.

## 📌 CKA imtihon uchun maslahat

CKA'da Docker image qurish so'ralmaydi — lekin `imagePullBackOff`
nosozligi ko'p uchraydi. Sabablari: teg xato, registry xususiy va
`imagePullSecrets` yo'q, yoki node'da tarmoq yo'q.

```bash
kubectl describe pod <nom> | grep -A5 Events
```

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
⬅️ [Oldingi dars](lesson1_2.md) · [Bo'lim indeksi](README.md) · ➡️ [lesson4.md](lesson4.md)
