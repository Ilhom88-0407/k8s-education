# Endi bo'lsa biz yaratgan deployment uchun service yaratamiz va podlarni sonini5 ga ko'paytiramiz (scaling):
```bash
kubectl expose deployment k8s-web-hello --type=LoadBalancer --port=3333 --target-port=3000
service/k8s-web-hello exposed
```
Servis ishga tushganini tekshirish uchun quyidagi buyruqni bajarishimiz kerak:
```bash
kubectl get services
```
endi bo'lsa biz deployment'ni scaling qilamiz, ya'ni podlar sonini 5 ga ko'paytiramiz:
```bash
kubectl scale deployment k8s-web-hello --replicas=5
deployment.apps/k8s-web-hello scaled
```
tekshirish uchun man NodePort dan foydalangan xolda brauzerda http://<node_ip>:31990 manziliga kiramiz va biz 5 ta podning ishga tushganini ko'rishimiz mumkin.
Biz yaratgan servis LoadBalancer nizning Cloudda ishlamaganligi sababli biz LoadBalancer servisi orqali ishga tushirilgan servisni imkoni bo'lmadi.
