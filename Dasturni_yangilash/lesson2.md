# NodeJS dasturini yangilaymiz
NodeJS dasturini obnavleniya qilishdan oldin yangilanish protsesini ko'rib tursih uchun quyidagi komandalarni kiritib olamiz:
```bash
kubectl rollout status deployment/k8s-web-hello
```
NodeJS dasturini yangilash uchun quyidagi komandani kirgizamiz:
```bash
kubectl set image deployment k8s-web-hello k8s=mrpocker88/k8s:ver2
misol uchun
kubectl set image deployment k8s-web-hello k8s=mrpocker88/k8s-web-hello:1.0.2
```
shundan keyin Web_brauzerga kirib tekshirildi:
![Brauzerda 194.107.115.75:31990 manzili ochilgan va sahifada "VERSION 3: Hello from the k8s-web-hello-554b8c5484-xvl9w" yozuvi ko'rinadi](image.png)

```
C:\Users\admin>curl http://194.107.115.75:31990/
<h1>VERSION 3: Hello from the k8s-web-hello-554b8c5484-fnz8n</h1>
```
Agar biz quyidagi komandani ishga tushirilsa bizning repligalarimiz yangisiga o'zgarishini ko'rishimiz mumkin:
```
kubectl rollout status deployment/k8s-web-hello
```

![kubectl set image buyrug'i "deployment.apps/k8s-web-hello image updated" javobini qaytardi, keyingi kubectl rollout status esa 7 replikadan 3 tasi yangilanganini ko'rsatyapti](image-1.png)
![kubectl rollout status chiqishi: "Waiting for deployment k8s-web-hello rollout to finish" xabari takrorlanib, yangilangan replikalar soni 3 dan 4 ga o'tyapti](image-2.png)
Quida bizning podlarimiz yangi NodeJS dasturida ishlayotganini ko'rishimiz mumkin.
![kubectl get pods chiqishi: eski ReplicaSet (56f7558d6c) ning 7 ta podi Terminating holatida, yangi ReplicaSet (9f9658788) ning 7 ta podi esa Running holatida — rolling update aynan shunday ko'rinadi](image-3.png)

