# Web dasturlar yaratish
## Kerakli bo'lgan dasturlarni o'rnatish
Hozir biz NodeJS dasturini o'rnatamiz. NodeJS bu JavaScript dasturlash tilida yozilgan server tomon dasturlarni yaratish uchun ishlatiladigan platformadir. 

### NodeJS dastur yordamida Web server yaratish va ishga tushurish

Serverimizda nodejs dasturini o'rnatib olamiz. Buning uchun terminalda quyidagi buyruqni bajarishimiz kerak:
```bash
sudo apt update
sudo apt install nodejs npm -y
```
Shu bilan birgalikda nodejs va npm larni versiyasini tekshirib ko'rishimiz mumkin:
```bash
root@test-server-k8s-1:~# node --version
v18.19.1
root@test-server-k8s-1:~# npm --version
9.2.0
```
Endi k8s-web-hello nomli papka yaratib olamiz. 
va cli da quyidagi komandani bajaramiz:
```bash
mkdir k8s-web-hello
cd k8s-web-hello
#va ushbu komandani bajarib, package.json faylini yaratamiz
npm init -y
```
Ushbu bajarganimizda bizning papkamizda package.json fayli yaratiladi. Endi biz server.js nomli fayl yaratamiz va unga quyidagi kodni yozamiz:
```javascript
{
  "name": "k8s-web-hello",
  "version": "1.0.1",
  "description": "",
  "main": "index.js",
  "scripts": {
    "start": "node index.mjs"
  },
  "keywords": [],
  "author": "",
  "license": "ISC",
  "dependencies": {
    "express": "^4.17.2"
  }
}
```
Bu kodda biz express kutubxonasini o'rnatamiz. Express bu NodeJS uchun eng mashhur web frameworklardan biridir. Endi biz express kutubxonasini o'rnatamiz:
```bash
npm install express
```
Shu bilan birgalikda biz joylahgan <k8s-web-hello> papkasida index.mjs nomli fayl yaratamiz va unga quyidagi kodni yozamiz:
```javascript
import express from 'express'
import os from 'os'

const app = express()
const PORT = 3000

app.get("/", (req, res) => {
  const helloMessage = `<h1>VERSION 2: Hello from the ${os.hostname()}</h1>`
  console.log(helloMessage)
  res.send(helloMessage)
})

app.listen(PORT, () => {
  console.log(`Web server is listening at port ${PORT}`)
})
```
Ushbu index.mjs faylida biz express kutubxonasini import qilamiz va web server yaratamiz. Bizning web serverimiz 3000 portda ishlaydi va serverga ulanngan xar bir foydalanuvchiga "Hello from the [hostname]"  haqida xabar yuboradi.

Endi biz serverni ishga tushiramiz:
```bash
root@test-server-k8s-1:~/k8s/k8s-web-hello# node index.mjs
Web server is listening at port 3000
## har bir serverga ulangan foydalanuvchi va serverning ekranida quyidagi xabar paydo bo'ladi:
VERSION 2: Hello from the test-server-k8s-1
VERSION 2: Hello from the test-server-k8s-1
```
Tekshirish uchun brauzerda http://localhost:3000 manziliga o'tamiz va quyidagi xabarni ko'ramiz:
VERSION 2: Hello from the test-server-k8s-1

agarda Windows operatsion tizimida ishlayotgan bo'lsangiz, curl orqali tekshirasiz:
```
C:\Users\admin>curl http://194.107.115.75:3000/
<h1>VERSION 2: Hello from the test-server-k8s-1</h1>
```

