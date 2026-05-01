## Deploymant bu nima?
Deploymant - bu Kubernetes resursi bo'lib, u sizga ilovalarni boshqarish va ularni yangilash imkonini beradi. Deploymant yordamida siz ilovalaringizni avtomatik ravishda ko'paytirishingiz, yangilashingiz va kerak bo'lganda tiklashingiz mumkin. Deploymantlar, odatda, podlarni yaratish va boshqarish uchun ishlatiladi, shuning uchun ular ilovalarni ishga tushirish va ularni yangilash uchun qulay vositadir. 
!["rasmda misol ko'rsatilgan"](image.png)
### Deploymant yaratish uchun quyidagi buyruqni ishlatamiz:
```
kubectl apply -f <deploymant-definition.yaml>
```
yoki 
``` 
kubectl create deployment <deploymant-name> --image=<image-name> -n <namespace>
```
Bu buyruqlar yordamida siz yangi deploymantlarni yaratishingiz mumkin. Bu, masalan, yangi ilovani sinash yoki mavjud ilovaning yangi versiyasini ishga tushirish uchun foydalidir.
### Deploymantni ko'rish uchun quyidagi buyruqlarni ishlatishingiz mumkin:
```
kubectl get deployments -n <namespace>
kubectl get deployments -A
```
