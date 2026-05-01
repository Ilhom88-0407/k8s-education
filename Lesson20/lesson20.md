## 1. Посмотреть IP нод
kubectl get nodes -o wide

Пример:
```
NAME                STATUS   ROLES           AGE   VERSION   INTERNAL-IP
test-server-k8s-1   Ready    control-plane   10d   v1.35.x   192.168.16.196
test-server-k8s-2   Ready    <none>          10d   v1.35.x   192.168.16.197
```
## 2. Зайти на нужную ноду обычным SSH
```
ssh root@192.168.16.197
```
или если пользователь не root:
```
ssh username@192.168.16.197
```
## 3. Если хотите зайти внутрь Pod

Это делается не через kubeadm, а через kubectl exec:
```
kubectl get pods -A
kubectl exec -it -n <namespace> <pod-name> -- /bin/bash
```
Если bash нет:
```
kubectl exec -it -n <namespace> <pod-name> -- /bin/sh
```
## 4. Если хотите debug самой ноды через Kubernetes

Можно использовать:
```
kubectl debug node/<node-name> -it --image=busybox
```
Официально kubectl debug node/... используется для отладки ноды, контейнер запускается с доступом к host namespaces, а файловая система ноды монтируется в /host.

После входа:
```
chroot /host
```