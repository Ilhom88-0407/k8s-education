# Ikkita deployment yaratish plani
![Ikki deployment sxemasi: tashqi IP LoadBalancer orqali k8s-web-to-nginx podiga kiradi; o'sha pod /nginx yo'liga so'rov kelganda ikkinchi ClusterIP servis orqali nginx podiga murojaat qiladi va javobni qaytaradi](image.png)
- bu rasmda bi 2 ta deployment yaratilganligini ko'rishimiz mumkin
1. deployment <k8s-web-to-ngnix>
-- bu yerda bizda 2 ta derektoriya bo'ladi 
        1. / #root direktoriyasi
        2. /nginx #nginx app direktoriyasi
2. deployment <nginx>
- shu bilan birgalikda 1 ta CluserIP servis 
- K8S clusterIP
- LoadBalancer
shu kabi xizmatlarni ishga tushirib ko'rib chiqamiz.

