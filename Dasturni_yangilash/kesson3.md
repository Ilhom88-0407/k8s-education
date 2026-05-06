## Klein endi yaratilgan deploymentni analiz qilib chiqamiz.
Analiz uchun quidagi komandadan foydalanamiz:
```
root@test-server-k8s-1:~# kubectl describe deployment k8s-web-hello
Name:                   k8s-web-hello
Namespace:              default
CreationTimestamp:      Wed, 06 May 2026 09:17:08 +0000
Labels:                 app=k8s-web-hello
Annotations:            deployment.kubernetes.io/revision: 4
Selector:               app=k8s-web-hello
Replicas:               5 desired | 5 updated | 5 total | 5 available | 0 unavailable
StrategyType:           RollingUpdate
MinReadySeconds:        0
RollingUpdateStrategy:  25% max unavailable, 25% max surge
Pod Template:
  Labels:  app=k8s-web-hello
  Containers:
   k8s:
    Image:         mrpocker88/k8s-web-hello:1.0.2
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
OldReplicaSets:  k8s-web-hello-77d545f465 (0/0 replicas created), k8s-web-hello-64fd9ff6f8 (0/0 replicas created), k8s-web-hello-6ff5fbd4c9 (0/0 replicas created)
NewReplicaSet:   k8s-web-hello-554b8c5484 (5/5 replicas created)
Events:
  Type    Reason             Age                From                   Message
  ----    ------             ----               ----                   -------
  Normal  ScalingReplicaSet  132m               deployment-controller  Scaled up replica set k8s-web-hello-64fd9ff6f8 from 0 to 2
  Normal  ScalingReplicaSet  132m               deployment-controller  Scaled down replica set k8s-web-hello-77d545f465 from 5 to 4
  Normal  ScalingReplicaSet  132m               deployment-controller  Scaled up replica set k8s-web-hello-64fd9ff6f8 from 2 to 3
  Normal  ScalingReplicaSet  132m               deployment-controller  Scaled down replica set k8s-web-hello-77d545f465 from 4 to 3
  Normal  ScalingReplicaSet  132m               deployment-controller  Scaled up replica set k8s-web-hello-64fd9ff6f8 from 3 to 4
  Normal  ScalingReplicaSet  132m               deployment-controller  Scaled down replica set k8s-web-hello-77d545f465 from 3 to 2
  Normal  ScalingReplicaSet  132m               deployment-controller  Scaled up replica set k8s-web-hello-64fd9ff6f8 from 4 to 5
  Normal  ScalingReplicaSet  132m               deployment-controller  Scaled down replica set k8s-web-hello-77d545f465 from 2 to 1
  Normal  ScalingReplicaSet  132m               deployment-controller  Scaled down replica set k8s-web-hello-77d545f465 from 1 to 0
  Normal  ScalingReplicaSet  61m                deployment-controller  Scaled up replica set k8s-web-hello-6ff5fbd4c9 from 0 to 2
  Normal  ScalingReplicaSet  61m                deployment-controller  Scaled down replica set k8s-web-hello-64fd9ff6f8 from 5 to 4
  Normal  ScalingReplicaSet  61m                deployment-controller  Scaled up replica set k8s-web-hello-6ff5fbd4c9 from 2 to 3
  Normal  ScalingReplicaSet  59m                deployment-controller  Scaled down replica set k8s-web-hello-6ff5fbd4c9 from 3 to 0
  Normal  ScalingReplicaSet  59m                deployment-controller  Scaled up replica set k8s-web-hello-554b8c5484 from 0 to 3
  Normal  ScalingReplicaSet  59m                deployment-controller  Scaled down replica set k8s-web-hello-64fd9ff6f8 from 4 to 3
  Normal  ScalingReplicaSet  59m                deployment-controller  Scaled up replica set k8s-web-hello-554b8c5484 from 3 to 4
  Normal  ScalingReplicaSet  59m                deployment-controller  Scaled down replica set k8s-web-hello-64fd9ff6f8 from 3 to 2
  Normal  ScalingReplicaSet  59m                deployment-controller  Scaled up replica set k8s-web-hello-554b8c5484 from 4 to 5
  Normal  ScalingReplicaSet  59m (x2 over 59m)  deployment-controller  (combined from similar events): Scaled down replica set k8s-web-hello-64fd9ff6f8 from 1 to 0
```
Menda mavjud 5 ta replikali deploymentni o'zgarishini ko'rishimiz mumkin.
<OldReplicaSets:  k8s-web-hello-77d545f465> buni ko'rib chiqamiz.
bu yerda <k8s-web-hello> deploymentni nomi <77d545f465> esa replikaning raqami
agar biz kubectl get pods qilsak:
```bash
root@test-server-k8s-1:~#  kubectl get pods
NAME                             READY   STATUS    RESTARTS   AGE
k8s-web-hello-554b8c5484-6442k   1/1     Running   0          61m
k8s-web-hello-554b8c5484-fnz8n   1/1     Running   0          61m
```
bu yerda <k8s-web-hello-554b8c5484-> deployemnt_nomi+replikaning indeksi <6442k> Bunisi esa Podlarga beriladigaon indeks

Agar biz deploymentdagi replikalarni sonini 10 taga oshirish kerak bo'lsa quidaki gomandani kiritamiz:
```bash
kubectl scale deployment k8s-web-hello --replicas=10
```
```bash
root@test-server-k8s-1:~# kubectl get pods
NAME                             READY   STATUS    RESTARTS   AGE
k8s-web-hello-554b8c5484-6442k   1/1     Running   0          87m
k8s-web-hello-554b8c5484-9m6zw   1/1     Running   0          12s
k8s-web-hello-554b8c5484-fnz8n   1/1     Running   0          87m
k8s-web-hello-554b8c5484-hpbp7   1/1     Running   0          87m
k8s-web-hello-554b8c5484-j6hnp   1/1     Running   0          12s
k8s-web-hello-554b8c5484-l927r   1/1     Running   0          12s
k8s-web-hello-554b8c5484-q8tvk   1/1     Running   0          87m
k8s-web-hello-554b8c5484-s8tjt   1/1     Running   0          12s
k8s-web-hello-554b8c5484-xvl9w   1/1     Running   0          87m
k8s-web-hello-554b8c5484-z8dsw   1/1     Running   0          12s
```
