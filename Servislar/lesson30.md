Bundan oldingi darsda biz ClusterIP turidagi servis yaratgan edik. Bu safar esa NodePort turidagi servis yaratamiz. NodePort turidagi servis, klaster ichidagi podlarga tashqi dunyo orqali kirish imkonini beradi. 
Ularning faqrini quida ko'rishingiz mumkin:
```
Bu 'NodePort' turidagi servisning holati:
root@test-server-k8s-1:~# kubectl get service
NAME           TYPE        CLUSTER-IP    EXTERNAL-IP   PORT(S)          AGE
kubernetes     ClusterIP   10.96.0.1     <none>        443/TCP          65m
nginx-deploy   NodePort    10.97.78.89   <none>        8080:30690/TCP   9s
root@test-server-k8s-1:~# kubectl describe service nginx-deploy -n default
Name:                     nginx-deploy
Namespace:                default
Labels:                   app=nginx-deploy
Annotations:              <none>
Selector:                 app=nginx-deploy
Type:                     NodePort          #### 'Bu yerda servisning turi NodePort ekanligini ko'rishingiz mumkin.'

Bu yerda esa 'ClusterIP' turidagi servisning holati:
root@test-server-k8s-1:~# kubectl get service
Name:                     nginx-deploy
Namespace:                default
Labels:                   app=nginx-deploy
Annotations:              <none>
Selector:                 app=nginx-deploy
Type:                     ClusterIP
```
 
## NodePort turidagi servis yaratish
Bundan oldingi darsdagi servisni o'chirib tashlaymiz va yangi servis yaratamiz. 
Buning uchun quyidagi buyruqni ishlatamiz:
```
root@test-server-k8s-1:~# kubectl delete service nginx-deploy -n default
service "nginx-deploy" deleted from default namespace
```
Endi bo'lsa yangi servis yaratamiz. Bu safar NodePort turidagi servis yaratamiz. NodePort turidagi servis, klaster ichidagi podlarga tashqi dunyo orqali kirish imkonini beradi. NodePort turidagi servis yaratish uchun quyidagi buyruqni ishlatamiz:
```
kubectl expose deployment nginx-deploy --type=NodePort --port=8080 --target-port=80 -n default

misol uchun:

root@test-server-k8s-1:~# kubectl expose deployment nginx-deploy --type=NodePort --port=8080 --target-port=80 -n default
service/nginx-deploy exposed
```
natijani bu yerda ko'rishingiz mumkin:
```
root@test-server-k8s-1:~# kubectl get service
NAME           TYPE        CLUSTER-IP    EXTERNAL-IP   PORT(S)          AGE
kubernetes     ClusterIP   10.96.0.1     <none>        443/TCP          65m
nginx-deploy   NodePort    10.97.78.89   <none>        8080:30690/TCP   9s
```
Bu yerda `nginx-deploy` servisi NodePort turida yaratilganligini va tashqi dunyo orqali 30690 porti orqali kirish mumkinligini ko'rishingiz mumkin. Masalan, nginx serverini tashqi dunyo bilan aloqa qilish uchun ishlatamiz.

`nginx-deploy` xaqida to'liqroq ma'lumotlarni ko'rish uchun quyidagi buyruqni ishlatishingiz mumkin:
```
kubectl describe service nginx-deploy -n default
```
bu  yesda biz quidagi ma'lumotlarni ko'rishimiz mumkin:
```
root@test-server-k8s-1:~# kubectl get service
NAME           TYPE        CLUSTER-IP    EXTERNAL-IP   PORT(S)          AGE
kubernetes     ClusterIP   10.96.0.1     <none>        443/TCP          65m
nginx-deploy   NodePort    10.97.78.89   <none>        8080:30690/TCP   9s
root@test-server-k8s-1:~# kubectl describe service nginx-deploy -n default
Name:                     nginx-deploy
Namespace:                default
Labels:                   app=nginx-deploy
Annotations:              <none>
Selector:                 app=nginx-deploy
Type:                     NodePort
IP Family Policy:         SingleStack
IP Families:              IPv4
IP:                       10.97.78.89
IPs:                      10.97.78.89
Port:                     <unset>  8080/TCP
TargetPort:               80/TCP
NodePort:                 <unset>  30690/TCP
Endpoints:                172.16.91.66:80,172.16.91.65:80,172.16.78.129:80 + 2 more...
Session Affinity:         None
External Traffic Policy:  Cluster
Internal Traffic Policy:  Cluster
Events:                   <none>
```
Bu yerda `kubectl describe service nginx-deploy -n default` buyruq yordamida `nginx-deploy` servisining batafsil ma'lumotlarini ko'rishingiz mumkin. Bu, masalan, servisning turlarini tekshirish yoki uning qaysi podlarga bog'langanligini ko'rish uchun foydalidir. Bu yerda `Endpoints` qismida servisning bog'langan podlarning IP manzillari va po'rtlari ko'rsatilgan. Bu, masalan, servisning qaysi podlarga bog'langanligini tekshirish yoki uning ichida nechta podlar ishga tushganligini ko'rsatadi.

## ClusterIP va NodePort turidagi servislarni taqqoslash
ClusterIP va NodePort turidagi servislarni taqqoslash uchun quyidagi jadvalni ko'rishingiz mumkin:
| Xususiyat | ClusterIP | NodePort |    
| --- | --- | --- |
| Turi | ClusterIP | NodePort |
| Kirish | Faqat klaster ichidan | Tashqi dunyo orqali |
| Port | Faqat klaster ichida | Tashqi dunyo orqali |
| Maqsad | Klaster ichidagi podlar orasida aloqa | Klaster ichidagi podlarga tashqi dunyo orqali kirish |
Bu yerda `ClusterIP` turidagi servis faqat klaster ichidan kirish imkonini beradi, ya'ni faqat klaster ichidagi podlar orasida aloqa qilish uchun ishlatiladi. `NodePort` turidagi servis esa tashqi dunyo orqali kirish imkonini beradi, ya'ni klaster ichidagi podlarga tashqi dunyo orqali kirish uchun ishlatiladi. Bu, masalan, nginx serverini tashqi dunyo bilan aloqa qilish uchun ishlatamiz.

tekshirish uchun quyidagi buyruqni ishlatishingiz mumkin:
```
curl http://<node-ip>:<node-port>
misol uchun:
curl http://<node-ip>:30690   
``` 
'node-ip' bu sizning serveringizning IP manzili, node-port esa NodePort turidagi servisning porti. Agar siz Unicon.uz bulutli xizmatlaridan foydalanayotgan bo'lsangiz, node-ip bu sizning serveringizning public IP (elastic IP) manzili  yoki LoadBalancer ning eIP si bo'ladi.
Agar siz Docker Desktop yoki minikube kabi lokal Kubernetes klasteridan foydalanayotgan bo'lsangiz, node-ip bu sizning lokal mashinangizning IP manzili bo'ladi. 

Docker Desktopda siz local url yaratib servisingizni tekshirishingiz mumkin.
Misol uchun:
```
minikube service nginx-deploy --url
http://1270.0.1:53787
! Becource you are using a Docker driver on darwin, the terminal needs to be open to run it.
```


