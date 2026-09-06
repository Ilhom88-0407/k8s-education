// k8s-web-to-nginx — servislar o'zaro qanday gaplashishini ko'rsatuvchi ilova.
//
// Uchta yo'l bor:
//   /                 -> o'z Pod nomini qaytaradi
//   /nginx            -> KLASTER ICHIDAGI nginx servisiga so'rov yuboradi
//   /jsonplaceholder  -> TASHQI API ga so'rov yuboradi
//
// Eng muhimi `/nginx`: u yerda IP emas, `http://nginx` degan NOM yozilgan.
// Bu nom — Service'ning DNS nomi. Nginx pod'lari o'chib-yonsa ham,
// nom o'zgarmaydi va kodni tahrirlash kerak bo'lmaydi.
import express from 'express'
import os from 'os'

const app = express()
const PORT = process.env.PORT || 3000

// Service nomi muhit o'zgaruvchisi orqali beriladi — shunda manifestda
// o'zgartirish uchun image'ni qayta qurish kerak bo'lmaydi.
const NGINX_URL = process.env.NGINX_URL || 'http://nginx'

app.get('/', (req, res) => {
  const xabar = `<h1>Hello from the ${os.hostname()}</h1>`
  console.log(xabar)
  res.send(xabar)
})

app.get('/nginx', async (req, res) => {
  try {
    const javob = await fetch(NGINX_URL)
    res.send(await javob.text())
  } catch (xato) {
    // Bu xato odatda ikki sababdan bo'ladi: nginx Service yaratilmagan,
    // yoki uning Endpoints ro'yxati bo'sh.
    console.error(`${NGINX_URL} ga ulanib bo'lmadi:`, xato.message)
    res.status(502).send(`<h1>502 — ${NGINX_URL} javob bermadi</h1>
      <p>Tekshiring: <code>kubectl get endpoints nginx</code></p>`)
  }
})

app.get('/jsonplaceholder', async (req, res) => {
  try {
    const javob = await fetch('https://jsonplaceholder.typicode.com/todos')
    res.setHeader('Content-Type', 'application/json')
    res.send(await javob.text())
  } catch (xato) {
    console.error('Tashqi API javob bermadi:', xato.message)
    res.status(502).json({ xato: 'tashqi API javob bermadi' })
  }
})

app.get('/healthz', (req, res) => res.status(200).send('ok'))

app.listen(PORT, () => {
  console.log(`Web server ${PORT}-portda tinglayapti`)
})
