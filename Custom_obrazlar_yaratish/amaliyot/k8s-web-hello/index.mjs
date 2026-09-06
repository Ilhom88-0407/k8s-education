// k8s-web-hello — darslik uchun eng oddiy web ilova.
//
// Ilova javobda o'zi ishlab turgan Pod'ning nomini (os.hostname())
// qaytaradi. Shu sababli sahifani bir necha marta yangilaganingizda
// javob har safar boshqa Pod'dan kelishini ko'rasiz — Service yukni
// qanday taqsimlayotgani shundan bilinadi.
import express from 'express'
import os from 'os'

const app = express()
const PORT = process.env.PORT || 3000
const VERSION = process.env.APP_VERSION || '3'

app.get('/', (req, res) => {
  const xabar = `<h1>VERSION ${VERSION}: Hello from the ${os.hostname()}</h1>`
  console.log(xabar)
  res.send(xabar)
})

// Kubernetes probe'lari uchun yengil endpoint.
// livenessProbe va readinessProbe shu yo'lni tekshiradi.
app.get('/healthz', (req, res) => res.status(200).send('ok'))

app.listen(PORT, () => {
  console.log(`Web server ${PORT}-portda tinglayapti`)
})
