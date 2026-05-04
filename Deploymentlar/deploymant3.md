### PODlarning IP manzillarini va portlarini ko'rish
Podlarning IP manzillarini va portlarini ko'rish uchun quyidagi buyruqni ishlatamiz:
``` 
kubectl get pods -n <namespace> -o wide
Misol uchun, `default` namespace ichida podlarning IP manzillarini va portlarini ko'rish uchun quyidagi buyruqni ishlatamiz:
server001:> kubectl get pods -n default -o wide
______________________________________________________________________________
NAME                            READY   STATUS    RESTARTS   AGE   IP               NODE                NOMINATED NODE   READINESS GATES
nginx-deploy-75c8b7c74b-5ckvw   1/1     Running   0          10s   172.16.91.66     test-server-k8s-3   <none>           <none>
nginx-deploy-75c8b7c74b-9svsz   1/1     Running   0          23s   172.16.78.129    test-server-k8s-2   <none>           <none>
nginx-deploy-75c8b7c74b-db9j9   1/1     Running   0          25s   172.16.91.65     test-server-k8s-3   <none>           <none>
nginx-deploy-75c8b7c74b-kf7zk   1/1     Running   0          25s   172.16.138.221   test-server-k8s-1   <none>           <none>
nginx-deploy-75c8b7c74b-srbxn   1/1     Running   0          25s   172.16.78.130    test-server-k8s-2   <none>           <none>
  
``` 
Bu yerda `IP` ustunida har bir podning IP manzillarini ko'rishingiz mumkin. Bu, masalan, podlarga to'g'ridan-to'g'ri murojaat qilish yoki ularning portlarini tekshirish uchun foydalidir.

## Podlarni to'liq ishga tushganini tekshirish biz serverni ichiga kirib tekshirishimiz mumkin, yoki quyidagi buyruqni ishlatamiz:
```
kubectl exec -it <pod-name> -n <namespace> -- /bin/bash
Misol uchun, `nginx-deploy-5c689d4b9f-5l6j8` nomli podning ichiga kirish uchun quyidagi buyruqni ishlatamiz:
server001:> kubectl exec -it nginx-deploy-5c689d4b9f-5l6j8 -n default -- /bin/bash
```
Bu buyruq yordamida siz `nginx-deploy-5c689d4b9f-5l6j8` nomli podning ichiga kirishingiz mumkin. Bu, masalan, podning ichidagi fayllarni tekshirish yoki uning ishga tushganligini tekshirish uchun foydalidir.

## PODlarning IP manzillar;
PODlarning IP manziliga serverni ichidan kirib bo'lmaydi, chunki PODlar ichki tarmoqqa ega va ular faqat klaster ichida mavjud. Agar siz PODlarga tashqaridan kirishni xohlasangiz, siz Service yoki Ingress resurslarini yaratishingiz kerak bo'ladi. Bu, masalan, ilovangizni tashqaridan kirish uchun ochish yoki uning portlarini boshqarish uchun foydalidir.
![POD IP addresses](image-4.png)

