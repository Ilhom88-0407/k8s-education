# Yaratilgan servis va Deploymentlarni o'chirish 
1. servisni o'chirish uchun birinchi servislarni ko'rib olamiz va o'zimimga kerak bo'lmagan servisni o'chirib tashlaymiz.
```bash
root@test-server-k8s-1:~# kubectl get services
NAME            TYPE           CLUSTER-IP      EXTERNAL-IP   PORT(S)          AGE
k8s-web-hello   LoadBalancer   10.107.19.197   <pending>     3333:31990/TCP   4h38m
kubernetes      ClusterIP      10.96.0.1       <none>        443/TCP          30h
root@test-server-k8s-1:~# kubectl delete service k8s-web-hello
service "k8s-web-hello" deleted from default namespace
root@test-server-k8s-1:~# kubectl get services
NAME         TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)   AGE
kubernetes   ClusterIP   10.96.0.1    <none>        443/TCP   30h
root@test-server-k8s-1:~#
```
Yuqorida servislarni <kubectl get services> buyruq orqali ko'rib oldik
undan so'nf  <kubectl delete service k8s-web-hello> buyruqdan foydalangan xolda servisni o'chirib tashladik
uchunchi buyruq orqali servis o'chirilganligiga ishonch xosilqilib oldik.

2. Edni bo'lsa Deploymentno o'chiramiz
``` bash
root@test-server-k8s-1:~# kubectl get deployment
NAME            READY   UP-TO-DATE   AVAILABLE   AGE
k8s-web-hello   10/10   10           10          4h44m
root@test-server-k8s-1:~# kubectl delete deployment k8s-web-hello
deployment.apps "k8s-web-hello" deleted from default namespace
root@test-server-k8s-1:~# kubectl get deployment
No resources found in default namespace.
```
Bu yerda biz deployment ni ko'rib oldik va ochirib tashladik.

3. PODlarni o'chirilganligini tekshirib olamiz
```bash
root@test-server-k8s-1:~# kubectl get pods
No resources found in default namespace.
```
Bu yerda ko'rishimiz mumkinki <default namespace>da umuman PODlar yo'q 