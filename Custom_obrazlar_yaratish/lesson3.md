### NodeJS dasturi uchun Dockerfile yaratish
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