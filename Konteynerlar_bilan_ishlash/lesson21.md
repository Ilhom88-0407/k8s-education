## Nimada konteynerlarga tashqaridan kirib bo'ladi?
```
serveroo1:> kubectl get pods -o wide 
```
'podlar nimaga wide formatda ko'rsatiladi?' deb so'rashingiz mumkin. Wide formatda siz podlarning IP manzillarini ko'rishingiz mumkin, bu esa sizga kerakli podni tanlashda yordam beradi.'
Misol uchun:
```text
NAME                READY   STATUS    RESTARTS   AGE   IP           NODE               NOMINATED NODE   READINESS GATES
test-server-k8s-1   1/1     Running   0          10d      10.244.0.3   test-server-k8s-1   <none>           <none>
test-server-k8s-2   1/1     Running   0          10d      10.244.0.5   test-server-k8s-2   <none>           <none>
```
Agar sizga kerakli podni tanlashda yordam kerak bo'lsa, uning IP manzilini ko'rishingiz mumkin. Masalan, agar siz `test-server-k8s-1` podiga kirishni xohlasangiz, uning IP manzili `10.244.0.3` ekanini shu jadvaldan ko'rasiz.
Lekin podlarga tashqaridan kirish uchun sizga pod nomi va namespace kerak bo'ladi. Keyin quyidagi buyruqni ishlatishingiz mumkin:
```
kubectl exec -it -n <namespace> <pod-name> -- /bin/bash
``` 
kubernetesda 3 ta tarmoq mavjud:
1. Pod tarmog'i: Podlar o'zaro va boshqa xizmatlar bilan aloqa qilish uchun ishlatiladi.
2. Xizmat tarmog'i: Xizmatlar o'zaro va tashqi dunyo bilan aloqa qilish uchun ishlatiladi.
3. Tashqi tarmoq: Tashqi dunyo bilan aloqa qilish uchun ishlatiladi.
Agar bash mavjud bo'lmasa, sh ni ishlatishingiz mumkin:
```
kubectl exec -it -n <namespace> <pod-name> -- /bin/sh
``` 
