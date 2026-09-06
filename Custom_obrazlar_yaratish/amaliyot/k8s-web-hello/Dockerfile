# k8s-web-hello — NodeJS ilovasi uchun Docker image.
#
# Qatlamlar tartibi ataylab shunday: avval faqat package fayllari
# nusxalanadi va `npm install` bajariladi, KEYIN qolgan kod. Shunda kodni
# o'zgartirganda Docker `npm install` qatlamini kesh'dan oladi va build
# bir necha barobar tez bo'ladi.
#
# Qurish:  docker build -t <foydalanuvchi>/k8s-web-hello:1.0.3 .
# Sinash:  docker run --rm -p 3000:3000 <foydalanuvchi>/k8s-web-hello:1.0.3

# Versiya QADALGAN. Tegsiz `node:alpine` bugun bir versiyani, ertaga
# boshqasini tortadi — build takrorlanmaydigan bo'lib qoladi.
FROM node:22-alpine

WORKDIR /app

# 1) Avval faqat bog'liqliklar ro'yxati
COPY package.json package-lock.json ./
RUN npm ci --omit=dev

# 2) Keyin kodning o'zi
COPY . ./

EXPOSE 3000

CMD ["npm", "start"]
