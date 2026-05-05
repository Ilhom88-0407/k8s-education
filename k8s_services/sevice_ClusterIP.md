## ClusterIP va servis yaratamiz.
Bizda xozir nginx-deploy nomli deploymant mavjud va biz unga bog'langan servis yaratamiz. Servis yaratish uchun quyidagi buyruqni ishlatamiz:
```
root@test-server-k8s-1:~# kubectl expose deploy nginx-deploy --port=8080 --target-port=80
service/nginx-deploy exposed  ## yu servis to'g'ri yaratilganligini bildiradi.
```
Ushbu buyruq bilan biz nginx-deploy deploymentini tashqi muxitdan 8080 porti orqali kelgan qabul qilib ichku muxudga (podlar tomon) 80 portga yo'naltirishni amalga oshiramiz. Bu, masalan, nginx serverini tashqi dunyo bilan aloqa qilish uchun ishlatamiz.
```
 Servis yaratgandan so'ng, uning holatini tekshirish uchun quyidagi buyruqni ishlatishingiz mumkin:
```
root@test-server-k8s-1:~# kubectl get services -n default
NAME           TYPE        CLUSTER-IP    EXTERNAL-IP   PORT(S)    AGE
kubernetes     ClusterIP   10.96.0.1     <none>        443/TCP    90s
nginx-deploy   ClusterIP   10.101.7.48   <none>        8080/TCP   17s
root@test-server-k8s-1:~# kubectl get services
NAME           TYPE        CLUSTER-IP    EXTERNAL-IP   PORT(S)    AGE
kubernetes     ClusterIP   10.96.0.1     <none>        443/TCP    117s
nginx-deploy   ClusterIP   10.101.7.48   <none>        8080/TCP   44s
```
Biz nginx-deploy servisini yaratganimizda unga  ClusterIP "10.101.7.48" avtomatik ravishda berilganligini ko'rishingiz mumkin. 
Va biz ushbu ClusterIP orqali servisni tekshirib olishimiz mumkin.
```
root@test-server-k8s-1:~# curl http://10.101.7.48:8080
```
Bu yerda natijani ko'rishingiz mumkin.
```
root@test-server-k8s-1:~# curl http://10.101.7.48:8080
<!DOCTYPE html>
<html>
<head>
<title>Welcome to nginx!</title>
<style>
html { color-scheme: light dark; }
body { width: 35em; margin: 0 auto;
font-family: Tahoma, Verdana, Arial, sans-serif; }
</style>
</head>
<body>
<h1>Welcome to nginx!</h1>
<p>If you see this page, nginx is successfully installed and working.
Further configuration is required for the web server, reverse proxy,
API gateway, load balancer, content cache, or other features.</p>

<p>For online documentation and support please refer to
<a href="https://nginx.org/">nginx.org</a>.<br/>
To engage with the community please visit
<a href="https://community.nginx.org/">community.nginx.org</a>.<br/>
For enterprise grade support, professional services, additional
security features and capabilities please refer to
<a href="https://f5.com/nginx">f5.com/nginx</a>.</p>

<p><em>Thank you for using nginx.</em></p>
</body>
</html>
```
