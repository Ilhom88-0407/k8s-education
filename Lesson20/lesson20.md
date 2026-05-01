## 1. serverlarni IP manzillarini ko'rish
```
kubectl get nodes -o wide
```
Misol uchun:
```
NAME                STATUS   ROLES           AGE   VERSION   INTERNAL-IP
test-server-k8s-1   Ready    control-plane   10d   v1.35.x   192.168.16.196
test-server-k8s-2   Ready    <none>          10d   v1.35.x   192.168.16.197
```
## 2. SSH orqali serverga kirish
```
ssh root@192.168.16.197
```
agar root foydalanuvchisi bilan kirish imkoni bo'lmasa, o'zingizga kerakli foydalanuvchi nomini ishlating:
```
ssh username@192.168.16.197
```
## 3. agar sizga pod ichiga kirish kerak bo'lsa

 pod nomini va namespace ni bilishingiz kerak, keyin quyidagi buyruqni ishlatishingiz mumkin:
```
kubectl get pods -A
kubectl exec -it -n <namespace> <pod-name> -- /bin/bash
```
Agar bash mavjud bo'lmasa, sh ni ishlatishingiz mumkin:
```
kubectl exec -it -n <namespace> <pod-name> -- /bin/sh
```
## 4. Agar siz Kubernetes debug qilish uchun node ichiga kirish kerak bo'lsa

Ushbu komndadan foydalanishingiz mumkin:
```
kubectl debug node/<node-name> -it --image=busybox
```
Официально kubectl debug node/... используется для отладки нodы, контейнер запускается с доступом к host namespaces, а файловая система нodы монтируется в /host.

После входа:
```
chroot /host
```