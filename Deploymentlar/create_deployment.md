## Deployment bu nima?
Deployment - bu Kubernetes resursi bo'lib, u sizga ilovalarni boshqarish va ularni yangilash imkonini beradi. Deployment yordamida siz ilovalaringizni avtomatik ravishda ko'paytirishingiz, yangilashingiz va kerak bo'lganda tiklashingiz mumkin. Deploymentlar, odatda, podlarni yaratish va boshqarish uchun ishlatiladi, shuning uchun ular ilovalarni ishga tushirish va ularni yangilash uchun qulay vositadir. 
!["rasmda misol ko'rsatilgan"](image.png)
### Deployment yaratish uchun quyidagi buyruqni ishlatamiz:
```bash
kubectl apply -f <deployment-definition.yaml>
```
yoki 
```bash
kubectl create deployment <deployment-name> --image=<image-name> -n <namespace>

misol uchun nginx image'idan foydalanib, nginx-deploy nomli yangi deployment yaratish uchun quyidagi buyruqni ishlatamiz:

server001:> kubectl create deployment nginx-deploy --image=nginx -n default
```
Bu buyruqlar yordamida siz yangi deploymentlarni yaratishingiz mumkin. Bu, masalan, yangi ilovani sinash yoki mavjud ilovaning yangi versiyasini ishga tushirish uchun foydalidir.
### Deploymentni ko'rish uchun quyidagi buyruqlarni ishlatishingiz mumkin:
```
kubectl get deployments -n <namespace>
kubectl get deployments -A
```
### deployment'ni qo'lda kirish uchun quyidagi buyruqlarni ishlatishingiz mumkin:
```
server001:> kubectl create deployment nginx-deploy --image=nginx
```
Bu buyruq yordamida siz `nginx` image'idan foydalanib, `nginx-deploy` nomli yangi deployment yaratishingiz mumkin. Bu, masalan, nginx serverini sinash yoki o'rganish uchun foydalidir.
### yaratilgan deployment'ni ko'rish uchun quyidagi buyruqlarni ishlatishingiz mumkin:
```
server001:> kubectl get deployments -o wide 
```
## deployment'ni detallarini ko'rish uchun quyidagi buyruqlarni ishlatishingiz mumkin:
``` 
server001:> kubectl describe deployment <deployment-name> -n <namespace>
```
misol uchun:
```
server001:> kubectl describe deployment nginx-deploy -n default
```
Bu buyruq yordamida siz deployment'ning detallarini ko'rishingiz mumkin. Bu, masalan, deployment'ning hozirgi holatini tekshirish yoki uning konfiguratsiyasini ko'rish uchun foydalidir.

"kubectl describe deployment " komandasini quyidagi ma'lumotlarni ko'rsatadi:
- Deployment'ning nomi va namespace
- Deployment'ning hozirgi holati (masalan, nechta podlar ishga tushgan, nechta podlar kerakli holatda)
- Deployment'ning strategiyasi (masalan, RollingUpdate yoki Recreate)    
- Deployment'ning image'i va uning versiyasi
- Deployment'ning resurs talablari (masalan, CPU va xotira)
- Deployment'ning yangilanish tarixi va uning hozirgi versiyasi  
- Deployment'ning hozirgi va kerakli holati (masalan, nechta podlar ishga tushgan, nechta podlar kerakli holatda)

![kubectl describe deploy my-nginx-deploy chiqishi: Labels app=my-nginx-deploy, Replicas 1 desired / 1 updated / 1 available, StrategyType RollingUpdate va Pod Template ichida nginx konteyneri](image-1.png)

NewReplicaSet: nginx-deploy-5c689d4b9f bu yangi yaratilgan ReplicaSet nomi bo'lib, u deployment tomonidan boshqariladi. Bu ReplicaSet, deployment'ning hozirgi versiyasini ifodalaydi va uning ichida nechta podlar ishga tushganligini ko'rsatadi. Agar siz deployment'ni yangilagan bo'lsangiz, yangi ReplicaSet yaratiladi va eski ReplicaSet arxivlanadi. Bu, masalan, deployment'ning yangilanish tarixini ko'rish yoki uning hozirgi holatini tekshirish uchun foydalidir.
![describe chiqishining oxiri: NewReplicaSet my-nginx-deploy-785cb5c9f4 (1/1 replicas created) va Events bo'limida deployment-controller ning ScalingReplicaSet hodisasi](image-2.png)
Agar siz kubectl get pods -n default komandasini ishlatsangiz, siz deployment tomonidan boshqarilayotgan podlarni ko'rishingiz mumkin. Bu, masalan, deployment'ning hozirgi holatini tekshirish yoki uning ichida nechta podlar ishga tushganligini ko'rish uchun foydalidir.
![podlar](image-3.png)
bu yerda:
```text
NAME                            READY   STATUS    RESTARTS   AGE
nginx-deploy-5c689d4b9f-5l6j8   1/1     Running   0          2m
nginx-deploy-5c689d4b9f-6h8j9   1/1     Running   0          2m
nginx-deploy-5c689d4b9f-7k9l0   1/1     Running   0          2m
```
Bu yerda `nginx-deploy-5c689d4b9f-5l6j8`, `nginx-deploy-5c689d4b9f-6h8j9` va `nginx-deploy-5c689d4b9f-7k9l0` 
nomli uchta po'dni ko'rib turibsiz, ularning 'nginx-deploy-5c689d4b9f' qismi deployment nomidan kelib chiqqan va '-5l6j8', '-6h8j9' va '-7k9l0' qismlari esa podning noyob identifikatorlari. Har bir podning holati 'Running' bo'lib, bu ularning muvaffaqiyatli ishga tushganligini ko'rsatadi. 'READY' ustuni 1/1 bo'lib, bu har bir podda bitta konteyner borligini va u konteynerning hammasi ishga tushganligini bildiradi. 'RESTARTS' ustuni 0 bo'lib, bu podlarda hech qanday qayta ishga tushirishlar sodir bo'lmaganligini ko'rsatadi. 'AGE' ustuni 2m bo'lib, bu podlarning 2 daqiqadan beri ishga tushganligini bildiradi.

deployment'da PODlar aloxida labellar bilan ajiratilgan bo'ladi, bu labellar yordamida siz deployment tomonidan boshqarilayotgan podlarni osongina aniqlay olasiz. Masalan, agar siz `kubectl get pods -n default --selector=app=nginx` komandasini ishlatsangiz, siz faqat `app=nginx` label'iga ega bo'lgan podlarni ko'rishingiz mumkin. Bu, masalan, deployment'ning hozirgi holatini tekshirish yoki uning ichida nechta podlar ishga tushganligini ko'rish uchun foydalidir.

Agar siz PODni:
```
Server001:> kubectl describe pod nginx-deploy-5c689d4b9f-5l6j8 -n default
```
qilib tekshirsangiz ichida:
```
Labels:         app=nginx       ## bu yerda app=nginx deployment bilan boylangan label'ni ko'rishingiz mumkin 
                pod-template-hash=5c689d4b9f ## by yerda pod-template-hash=5c689d4b9f deployment tomonidan berilgan ID
Conrolled By:  ReplicaSet/nginx-deploy-5c689d4b9f ## bu yerda ReplicaSet/nginx-deploy-5c689d4b9f deployment tomonidan boshqarilayotgan ReplicaSet nomi ko'rishingiz mumkin
Events:        ## pod qanday ishga tushganligini ko'rsa bo'ladi
    Type    Reason     Age   From               Message
    ----    ------     ----  ----               -------
    Normal  Scheduled  2m    default-scheduler  Successfully assigned default/nginx-deploy-5c689d4b9f-5l6j8 to test-server-k8s-1
    Normal  Pulling    2m    kubelet            Pulling image "nginx:latest"
    Normal  Pulled     2m    kubelet            Successfully pulled image "nginx:latest" in 1.23456789s
    Normal  Created    2m    kubelet            Created container nginx
    Normal  Started    2m    kubelet            Started container nginx
```
larni ko'rishingiz mumkin.
