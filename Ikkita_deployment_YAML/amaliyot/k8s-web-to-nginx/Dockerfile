# k8s-web-to-nginx — ikkinchi servisga murojaat qiluvchi namuna ilova.
#
# Bu ilova `/nginx` yo'liga so'rov kelganda `http://nginx` manziliga
# murojaat qiladi — ya'ni Kubernetes Service'ning DNS nomiga. Shu bilan
# servislar o'zaro qanday gaplashishini ko'rsatadi.
#
# Qurish: docker build -t <foydalanuvchi>/k8s-web-to-nginx:2.0.0 .
FROM node:22-alpine

WORKDIR /app

COPY package.json package-lock.json ./
RUN npm ci --omit=dev

COPY . ./

EXPOSE 3000

CMD ["npm", "start"]
