# Yaratgan servisimizdan foydalanish uchun DNS nomidan foydalanishimiz mumkin. Bizning servisimizning nomi nginx va u default namespace’da joylashgan, shuning uchun biz unga nginx deb murojaat qilishimiz mumkin.
```bash
kubectl get svc nginx
```
```bash
NAME    TYPE        CLUSTER-IP    EXTERNAL-IP   PORT(S)   AGE
nginx   ClusterIP   10.109.39.5   <none>        80/TCP    16h
```
Bu yerda biz nginx servisining ClusterIP manzilini ko'rishimiz mumkin, bulardan foydalanib servisimizga murojaat qilishimiz mumkin.

```bash
curl http://nginx
```
Bu yerda biz nginx servisiga murojaat qilganimizda, nginx servisining ClusterIP manziliga murojaat qilgan bo'lamiz va nginx servisining porti 80 bo'lganligi uchun http://nginx:80 deb murojaat qilgan bo'lamiz. Bu yerda biz nginx servisining IP manzilini ko'rishimiz mumkin, bulardan foydalanib servisimizga murojaat qilishimiz mumkin.

```bash
curl http://10.109.39.5
```
Bu yerda biz nginx servisining ClusterIP manzilini ko'rishimiz mumkin, bulardan foydalanib servisimizga murojaat qilishimiz mumkin. Bu yerda biz nginx servisining IP manzilini ko'rishimiz mumkin, bulardan foydalanib servisimizga murojaat qilishimiz mumkin.
```bash
root@test-server-k8s-1:~# curl http://10.109.39.5
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
Bu yerda biz nginx servisining IP manzilini ko'rishimiz mumkin, bulardan foydalanib servisimizga murojaat qilishimiz mumkin. Bu yerda biz nginx servisining IP manzilini ko'rishimiz mumkin, bulardan foydalanib servisimizga murojaat qilishimiz mumkin.


