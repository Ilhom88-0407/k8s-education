## Endi bo'lsa deploymentlardag podlarni sonini o'zgartiramiz. Buning uchun biz deploymentni tahrirlashimiz kerak bo'ladi. Biz deploymentni tahrirlash uchun quyidagi buyruqni bajarishimiz kerak bo'ladi:

```bash
kubectl edit deployment k8s-web-to-nginx
```
Bu buyruqni bajarishimiz bilan biz deploymentni tahrirlash uchun editor ochiladi. Bu editor orqali biz deploymentdagi podlarni sonini o'zgartirishimiz mumkin bo'ladi. Biz deploymentdagi podlarni sonini 3 ga o'zgartiramiz va saqlaymiz.

```yaml
spec:
  replicas: 3
```
Shu bilan birga deployment k8s-web-to-nginx.yaml faylida ham podlarni sonini 3 ga o'zgartiramiz va saqlaymiz.

```yaml
spec:
  replicas: 3
``` 

## Deploymentni o'chirib tashlash

```bash
kubectl delete deployment k8s-web-to-nginx
``` 
Yuqoridagi buyruqni bajarishimiz bilan biz k8s-web-to-nginx deploymentini o'chirib tashlaymiz. Bu buyruqni bajarishimiz bilan bizning clusterimizda k8s-web-to-nginx deploymenti va unga tegishli podlar o'chiriladi.
## Deploymentni yaratish

```bash
kubectl apply -f k8s-web-to-nginx.yaml
```
Yuqoridagi buyruqni bajarishimiz bilan biz k8s-web-to-nginx.yaml faylida yozilgan deploymentni yaratamiz. Bu buyruqni bajarishimiz bilan bizning clusterimizda k8s-web-to-nginx deploymenti va unga tegishli podlar yaratiladi.
## Deploymentni tekshirish

```bash
kubectl get deployments
```
Yuqoridagi buyruqni bajarishimiz bilan biz clusterimizda mavjud bo'lgan deploymentlarni ko'ra olamiz. Bu buyruqni bajarishimiz bilan biz k8s-web-to-nginx deploymentini va uning holatini ko'ra olamiz.
```bash
kubectl get pods
```
Yuqoridagi buyruqni bajarishimiz bilan biz clusterimizda mavjud bo'lgan podlarni ko'ra olamiz. Bu buyruqni bajarishimiz bilan biz k8s-web-to-nginx deploymentiga tegishli podlarni va ularning holatini ko'ra olamiz.