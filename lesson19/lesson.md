## NGINX POD larning  faoliyatini tekshirish

```bash
> kubectl get pods  ##> podlarni ko'rish uchun
NAME            READY   STATUS    RESTARTS   AGE
my-nginx-pod   1/1     Running   0          5m
```
Bu buyruq orqali barcha podlarni ko'rish mumkin. `READY` ustuni konteynerlarning tayyorligini ko'rsatadi, `STATUS` esa podning hozirgi holatini bildiradi.
![alt text](image.png)

```
Server001:> kubectl describe pod my-nginx-pod
Name:         my-nginx-pod  
Namespace:    default  
Priority:     0
Node:         minikube/
Start Time:   Wed, 01 Jan 2020 00:00:00 +0000
Labels:       app=my-app
Annotations:  <none>
Status:       Running
IP:           10.244.0.3
IPs:
    IP: 10.244.0.3
Containers:
  my-container:
    Container ID:   docker://abcdef123456
    Image:          nginx:latest
    Image ID:       docker-pullable://nginx@sha256:abcdef123456
    Port:           80/TCP
    State:          Running
      Started:      Wed, 01 Jan 2020 00:01:00 +0000
    Ready:          True
    Restart Count:  0
```
Agar biz ping 10.244.0.3 ga ping bersak, ping muvofaqiyatsiz bo'ladi, chunki bu IP podning ichki IP manzili hisoblanadi va faqat klaster ichida ko'rinadi.


```
Server001:> kubectl ssh ### qilsak bir terminalga kiramiz va shu terminalda ping berishimiz mumkin
minikube:~$ ping 10.244.0.3
PING successful
```
```
Agar biz ssh qilib kirib burl qilsak
minikube:~$ curl http://10.244.0.3 ## qilsak nginx serveridan javob olamiz
``` 

 
