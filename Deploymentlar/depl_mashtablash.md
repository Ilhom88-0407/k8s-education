### Nginx deploymentni mashtablash bo'yicha yakuniy qo'llanma
Biz sizlar bilan Nginx deployment yaratdik va uni Kubernetes klasterida ishga tushirdik. xozir esa ushbu deploymentni ko'rib chiqamiz.
```
root@test-server-k8s-1:~# kubectl get deployments
NAME           READY   UP-TO-DATE   AVAILABLE   AGE
nginx-deploy   5/5     5            5           2d18h
root@test-server-k8s-1:~# kubectl describe deploy nginx-deploy
Name:                   nginx-deploy
Namespace:              default
CreationTimestamp:      Fri, 01 May 2026 13:46:30 +0000
Labels:                 app=nginx-deploy
Annotations:            deployment.kubernetes.io/revision: 3
Selector:               app=nginx-deploy
Replicas:               5 desired | 5 updated | 5 total | 5 available | 0 unavailable
StrategyType:           RollingUpdate
MinReadySeconds:        0
RollingUpdateStrategy:  25% max unavailable, 25% max surge
Pod Template:
  Labels:       app=nginx-deploy
  Annotations:  kubectl.kubernetes.io/restartedAt: 2026-05-01T14:20:45Z
  Containers:
   nginx:
    Image:         nginx
    Port:          <none>
    Host Port:     <none>
    Environment:   <none>
    Mounts:        <none>
  Volumes:         <none>
  Node-Selectors:  <none>
  Tolerations:     <none>
Conditions:
  Type           Status  Reason
  ----           ------  ------
  Available      True    MinimumReplicasAvailable
  Progressing    True    NewReplicaSetAvailable
OldReplicaSets:  nginx-deploy-8b9dbd8c9 (0/0 replicas created), nginx-deploy-7b875bc49c (0/0 replicas created)
NewReplicaSet:   nginx-deploy-75c8b7c74b (5/5 replicas created)
Events:          <none>
```
Bu yerda `kubectl describe deploy nginx-deploy` buyruq yordamida `nginx-deploy` deploymentining batafsil ma'lumotlarini ko'rishingiz mumkin. Bu, masalan, deploymentning strategiyasi, shabloni, shartlari va hodisalarini tekshirish uchun foydalidir.

## depolymantni ichidan bitta PODni o'chirish uchun quyidagi buyruqni ishlatishingiz mumkin:
```
kubectl delete pod <pod-name> -n <namespace>
misol uchun:
kubectl delete pod nginx-deploy-5c689d4b9f-5l6j8 -n default
```
Bu buyruq yordamida siz `nginx-deploy-5c689d4b9f-5l6j8` nomli podni o'chirishingiz mumkin. Bu, masalan, deploymantning yangilanishini tekshirish yoki uning ichida nechta podlar ishga tushganligini ko'rish uchun foydalidir. O'chirilgan pod avtomatik ravishda deploymant tomonidan yangilari bilan almashtiriladi, bu esa deploymantning doimiy ravishda ishlashini ta'minlaydi.
## Natijani bu yerda ko'rishingiz mumkin: 
```
root@test-server-k8s-1:~# kubectl get pods -n default
NAME                            READY   STATUS    RESTARTS   AGE
nginx-deploy-75c8b7c74b-5ckvw   1/1     Running   0          3d15h
nginx-deploy-75c8b7c74b-9svsz   1/1     Running   0          3d15h
nginx-deploy-75c8b7c74b-db9j9   1/1     Running   0          3d15h
nginx-deploy-75c8b7c74b-kf7zk   1/1     Running   0          3d15h
nginx-deploy-75c8b7c74b-srbxn   1/1     Running   0          3d15h
root@test-server-k8s-1:~# kubectl delete pod nginx-deploy-75c8b7c74b-kf7zk
pod "nginx-deploy-75c8b7c74b-kf7zk" deleted from default namespace
root@test-server-k8s-1:~# kubectl get pods -n default
NAME                            READY   STATUS    RESTARTS   AGE
nginx-deploy-75c8b7c74b-5ckvw   1/1     Running   0          3d15h
nginx-deploy-75c8b7c74b-9svsz   1/1     Running   0          3d15h
nginx-deploy-75c8b7c74b-db9j9   1/1     Running   0          3d15h
nginx-deploy-75c8b7c74b-m8jhx   1/1     Running   0          10s
nginx-deploy-75c8b7c74b-srbxn   1/1     Running   0          3d15h

```