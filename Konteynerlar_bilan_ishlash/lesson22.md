### Podlarni qayta yaratish va o'chirish
Podlarni qayta yaratish va o'chirish uchun quyidagi buyruqlarni ishlatishingiz mumkin:
``` 
kubectl delete pod <pod-name> -n <namespace>
kubectl apply -f <pod-definition.yaml>
``` 
Bu buyruqlar yordamida siz podlarni o'chirib, ularni yangilangan konfiguratsiya bilan qayta yaratishingiz mumkin. Bu, masalan, yangi image versiyasini sinash yoki resurslarni yangilash uchun foydalidir.
### Podlarni ko'rish
Podlarni ko'rish uchun quyidagi buyruqlarni ishlatishingiz mumkin:
``` 
kubectl get pods -n <namespace>
kubectl get pods -A
``` 
Bu buyruqlar yordamida siz o'zingizning namespace'ingizdagi yoki barcha namespace'lardagi podlarni ko'rishingiz mumkin. Bu, masalan, podlarning holatini tekshirish yoki ularning IP manzillarini ko'rish uchun foydalidir.
### Podlarga tashqaridan kirish      
Podlarga tashqaridan kirish uchun quyidagi buyruqlarni ishlatishingiz mumkin:
```
kubectl exec -it -n <namespace> <pod-name> -- /bin/bash
```
Bu buyruq yordamida siz pod ichiga kirib, uning ichidagi terminalga ega bo'lishingiz mumkin. Bu, masalan, pod ichidagi jarayonlarni tekshirish yoki loglarni ko'rish uchun foydalidir. Agar bash mavjud bo'lmasa, sh ni ishlatishingiz mumkin:
```
kubectl exec -it -n <namespace> <pod-name> -- /bin/sh
```
### pod yaratish
Pod yaratish uchun quyidagi buyruqlarni ishlatishingiz mumkin:
```
kubectl apply -f <pod-definition.yaml>
```  
yoki 
```
kubectl run <pod-name> --image=<image-name> -n <namespace>
```
Bu buyruqlar yordamida siz yangi podlarni yaratishingiz mumkin. Bu, masalan, yangi ilovani sinash yoki mavjud ilovaning yangi versiyasini ishga tushirish uchun foydalidir.

## yaratlgan podni ko'rish uchun quyidagi buyruqlarni ishlatishingiz mumkin:
```
kubectl get pods -o wide 
```
