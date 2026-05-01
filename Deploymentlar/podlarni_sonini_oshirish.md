### Deployment orqali podlarni sonini oshirish
Bu bo'limda biz deploymant orqali podlarni sonini oshirishni ko'rib chiqamiz. Deploymant, Kubernetesda podlarni boshqarish uchun ishlatiladigan resurs turi bo'lib, u podlarni yaratish, yangilash va o'chirishni avtomatik ravishda boshqaradi. Deploymant yordamida siz podlarni sonini oshirish yoki kamaytirish orqali ilovangizning yukini boshqarishingiz mumkin.
### Deploymentdagi podalrni sonini ko'paytirish uchun quyidagi buyruqni ishlatamiz:
```
kubectl ger deployments -n <namespace>

yoki aniq bir deploymantni ko'rish uchun:

kubectl get deployment nginx-deploy -n default
```
ichida quidaki ma'lumotlarni ko'rishingiz mumkin:
```
NAME           READY   UP-TO-DATE   AVAILABLE   AGE
nginx-deploy   1/1     1            1           10m
```

### Podlarni sonini oshirish uchun quyidagi buyruqni ishlatamiz:
``` 
kubectl scale deployment <deploymant-name> --replicas=<soni> -n <namespace>

ushbu komanda yordamida nginx-deploy podlar sonini 5 taga oshiramiz:

server001:> kubectl scale deployment nginx-deploy --replicas=5 -n default
```
Bu buyruq yordamida siz `nginx-deploy` deploymantidagi podlar sonini 5 taga oshirishingiz mumkin. Bu, masalan, ilovangizning yukini boshqarish yoki ko'proq foydalanuvchilarni qo'llab-quvvatlash uchun foydalidir.
### Podlarni sonini oshirgandan so'ng, deploymantning hozirgi holatini tekshirish uchun quyidagi buyruqni ishlatishingiz mumkin:
```
kubectl get deployment nginx-deploy -n default
_____________________________________________________________________________
NAME           READY   UP-TO-DATE   AVAILABLE   AGE
nginx-deploy   5/5     5            5           15m
```
Bu yerda `READY` ustunida 5/5 ko'rsatilgan, bu deploymantdagi barcha 5 podning ishga tushganligini va mavjudligini bildiradi. Bu, masalan, deploymantning hozirgi holatini tekshirish yoki uning yangilangan konfiguratsiyasini ko'rish uchun foydalidir.
### Podlarni sonini oshirgandan so'ng, deploymantning ichidagi podlarni ko'rish uchun quyidagi buyruqni ishlatishingiz mumkin:
```
kubectl get pods -n default
______________________________________________________________________________
NAME                                READY   STATUS    RESTARTS   AGE
nginx-deploy-5c689d4b9f-5l6j8   1/1     Running   0          2m
nginx-deploy-5c689d4b9f-6h8j9   1/1     Running   0          2m             
nginx-deploy-5c689d4b9f-7k9l0   1/1     Running   0          2m
``` 
Bu yerda `nginx-deploy-5c689d4b9f-5l6j8`, `nginx-deploy-5c689d4b9f-6h8j9` va `nginx-deploy-5c689d4b9f-7k9l0` nomli 3 ta podning ishga tushganligini ko'rishingiz mumkin. Bu, masalan, deploymantning hozirgi holatini tekshirish yoki uning ichida nechta podlar ishga tushganligini ko'rish mumkin. 
### Deploymantnidebug qilish uchun quyidagi buyruqni ishlatishingiz mumkin:
```
kubectl describe deployment <deploymant-name> -n <namespace>
_______________________________________________________________________________
NaME:                   nginx-deploy
Namespace:              default
CreationTimestamp:      2024-06-01T12:00:00Z
Labels:                app=nginx
Annotations:           deployment.kubernetes.io/revision: 1
Selector:              app=nginx
Replicas:              5 desired | 5 updated | 5 total | 5 available | 0 unavailable
StrategyType:          RollingUpdate
Conditions:
  Type           Status  Reason                   Message
  ----           ------  ------                   -------
  Available      True    MinimumReplicasAvailable   Deployment has minimum availability.
  Progressing    True    NewReplicaSetAvailable     ReplicaSet "nginx-deploy-5c689d4b9f" has successfully progressed.
OldReplicaSet:  nginx-deploy-5c689d4b9f (1/1 replicas created)
NewReplicaSet:  nginx-deploy-5c689d4b9f (5/5 replicas created)
Events:
  Type    Reason             Age   From                   Message
  ----    ------             ----  ----                   -------
  Normal  ScalingReplicaSet  2m    deployment-controller  Scaled up replica set nginx-deploy-5c689d4b9f to 1
  Normal  ScalingReplicaSet  2m    deployment-controller  Scaled up replica set nginx-deploy-5c689d4b9f to 4 from 1
  Normal  ScalingReplicaSet  2m    deployment-controller  Scaled up replica set nginx-deploy-5c689d4b9f to 5 from 4
```
Bu buyruq yordamida siz deploymantning detallarini ko'rishingiz mumkin. Bu, masalan, deploymantning hozirgi holatini tekshirish yoki uning konfiguratsiyasini ko'rish uchun foydalidir. Bu yerda siz deploymantning nomi, namespace, yaratilgan vaqti, label va annotationlari, selector, replicas soni, strategiyasi, shartlari va hodisalarini ko'rishingiz mumkin. Bu ma'lumotlar yordamida siz deploymantning hozirgi holatini tahlil qilishingiz yoki uning yangilanish tarixini ko'rishingiz mumkin.
