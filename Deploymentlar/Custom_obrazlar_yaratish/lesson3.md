### NodeJS dasturi uchun Dockerfile yaratish
Endi biz Dockerfile yaratamiz. Dockerfile bu bizning dasturimiz uchun Docker image yaratish uchun kerak bo'lgan ko'rsatmalarni o'z ichiga olgan fayl. Biz Dockerfile ni k8s-web-hello papkasida yaratamiz va unga quyidagi kodni yozamiz:
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
COPY . .
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