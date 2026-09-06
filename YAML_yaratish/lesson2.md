# YAML faylning Kubernetes klasterida qo'llanilishi

Kubernetes klasterida `Deployment` yaratish uchun `YAML` fayl yaratishni o'rganishga mo'ljallangan.
Hozirda biz yaratgan <deployment.yaml> fayli mavjud va biz uni kubernetes klasterida ishga tushiramiz:
buning uchun quyidagi buyruqni ishlatamiz:

```bash
kubectl apply -f deployment.yaml
```
Bu buyruq yordamida siz kubernetes klasteriga `deployment` yaratishingiz mumkin.
```bash
root@test-server-k8s-1:~# kubectl apply -f deployment.yaml
deployment.apps/k8s-web-hello created
-------------------------------------------------------------------------------
root@test-server-k8s-1:~# kubectl get deployment
NAME            READY   UP-TO-DATE   AVAILABLE   AGE
k8s-web-hello   5/5     5            5           15s
-------------------------------------------------------------------------------
root@test-server-k8s-1:~# kubectl get pods
NAME                             READY   STATUS    RESTARTS   AGE
k8s-web-hello-7c47cb8cd8-b7752   1/1     Running   0          24s
k8s-web-hello-7c47cb8cd8-bnwsv   1/1     Running   0          24s
k8s-web-hello-7c47cb8cd8-c7spn   1/1     Running   0          24s
k8s-web-hello-7c47cb8cd8-cknxt   1/1     Running   0          24s
k8s-web-hello-7c47cb8cd8-npmqs   1/1     Running   0          24s
-------------------------------------------------------------------------------
root@test-server-k8s-1:~# kubectl describe deployment
Name:                   k8s-web-hello
Namespace:              default
CreationTimestamp:      Thu, 07 May 2026 09:19:45 +0000
Labels:                 <none>
Annotations:            deployment.kubernetes.io/revision: 1
Selector:               app=k8s-web-hello
Replicas:               5 desired | 5 updated | 5 total | 5 available | 0 unavailable
StrategyType:           RollingUpdate
MinReadySeconds:        0
RollingUpdateStrategy:  25% max unavailable, 25% max surge
Pod Template:
  Labels:  app=k8s-web-hello
  Containers:
   k8s-web-hello:
    Image:      mrpocker88/k8s-web-hello:1.0.2
    Port:       3000/TCP
    Host Port:  0/TCP
    Limits:
      cpu:         250m
      memory:      128Mi
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
OldReplicaSets:  <none>
NewReplicaSet:   k8s-web-hello-7c47cb8cd8 (5/5 replicas created)
Events:
  Type    Reason             Age   From                   Message
  ----    ------             ----  ----                   -------
  Normal  ScalingReplicaSet  46s   deployment-controller  Scaled up replica set k8s-web-hello-7c47cb8cd8 from 0 to 5
```
bu yerda biz deploymentni Kubernetes klasterida yaratdik va uning holatini tekshirib oldik.

Agarda biz yaml fayilida o'zgartirishlar kiritgan bo'lsak quyidagi buyruqni ishlatamiz:
```bash 
kubectl apply -f deployment.yaml
```
misol uchun bizning `deployment.yaml` faylida <replicas: 5> ni <replicas: 10> ga <image: mrpocker88/k8s-web-hello:1.0.2> ni esa <image: mrpocker88/k8s-web-hello:1.0.3> ga o'zgartirdik va uni Kubernetes klasterida yaratishimiz mumkin.
Edi bo'lsa analiz qilib ko'ramiz o'zgarishlarni
```bash
root@test-server-k8s-1:~# kubectl apply -f deployment.yaml
deployment.apps/k8s-web-hello configured
root@test-server-k8s-1:~# kubectl get pods
NAME                             READY   STATUS              RESTARTS   AGE
k8s-web-hello-7c47cb8cd8-96tnn   0/1     ContainerCreating   0          1s
k8s-web-hello-7c47cb8cd8-9kx4s   1/1     Running             0          4s
k8s-web-hello-7c47cb8cd8-ctdpm   1/1     Running             0          3s
k8s-web-hello-7c47cb8cd8-d84b2   1/1     Running             0          4s
k8s-web-hello-7c47cb8cd8-d89g9   1/1     Running             0          4s
k8s-web-hello-7c47cb8cd8-dbzkn   1/1     Running             0          3s
k8s-web-hello-7c47cb8cd8-dvrt5   1/1     Running             0          2s
k8s-web-hello-7c47cb8cd8-kftpv   1/1     Running             0          4s
k8s-web-hello-7c47cb8cd8-n5xfh   0/1     ContainerCreating   0          2s
k8s-web-hello-7c47cb8cd8-rsdqq   1/1     Running             0          4s
k8s-web-hello-7dfdc85b77-659qw   0/1     Error               0          102s
k8s-web-hello-7dfdc85b77-cj5kd   1/1     Terminating         0          4s
k8s-web-hello-7dfdc85b77-g9fhz   0/1     Error               0          98s
k8s-web-hello-7dfdc85b77-k7trw   1/1     Terminating         0          36s
k8s-web-hello-7dfdc85b77-qhx57   1/1     Terminating         0          95s
k8s-web-hello-7dfdc85b77-tdcv4   1/1     Terminating         0          4s
root@test-server-k8s-1:~# kubectl describe deployment
Name:                   k8s-web-hello
Namespace:              default
CreationTimestamp:      Thu, 07 May 2026 09:19:45 +0000
Labels:                 <none>
Annotations:            deployment.kubernetes.io/revision: 3
Selector:               app=k8s-web-hello
Replicas:               10 desired | 10 updated | 10 total | 10 available | 0 unavailable
StrategyType:           RollingUpdate
MinReadySeconds:        0
RollingUpdateStrategy:  25% max unavailable, 25% max surge
Pod Template:
  Labels:  app=k8s-web-hello
  Containers:
   k8s-web-hello:
    Image:      mrpocker88/k8s-web-hello:1.0.2
    Port:       3000/TCP
    Host Port:  0/TCP
    Limits:
      cpu:         250m
      memory:      128Mi
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
OldReplicaSets:  k8s-web-hello-7dfdc85b77 (0/0 replicas created)
NewReplicaSet:   k8s-web-hello-7c47cb8cd8 (10/10 replicas created)
Events:
  Type    Reason             Age                From                   Message
  ----    ------             ----               ----                   -------
  Normal  ScalingReplicaSet  109s               deployment-controller  Scaled down replica set k8s-web-hello-7c47cb8cd8 from 20 to 3
  Normal  ScalingReplicaSet  109s               deployment-controller  Scaled up replica set k8s-web-hello-7dfdc85b77 from 0 to 1
  Normal  ScalingReplicaSet  105s               deployment-controller  Scaled down replica set k8s-web-hello-7c47cb8cd8 from 3 to 2
  Normal  ScalingReplicaSet  105s               deployment-controller  Scaled up replica set k8s-web-hello-7dfdc85b77 from 1 to 2
  Normal  ScalingReplicaSet  102s               deployment-controller  Scaled down replica set k8s-web-hello-7c47cb8cd8 from 2 to 1
  Normal  ScalingReplicaSet  102s               deployment-controller  Scaled up replica set k8s-web-hello-7dfdc85b77 from 2 to 3
  Normal  ScalingReplicaSet  97s                deployment-controller  Scaled down replica set k8s-web-hello-7c47cb8cd8 from 1 to 0
  Normal  ScalingReplicaSet  43s                deployment-controller  Scaled up replica set k8s-web-hello-7dfdc85b77 from 3 to 5
  Normal  ScalingReplicaSet  11s                deployment-controller  Scaled up replica set k8s-web-hello-7dfdc85b77 from 5 to 10
  Normal  ScalingReplicaSet  8s (x14 over 11s)  deployment-controller  (combined from similar events): Scaled down replica set k8s-web-hello-7dfdc85b77 from 1 to 0
```
<Scaled up replica set k8s-web-hello-7dfdc85b77 from 5 to 10> bu yerda '10' ta pod yaratilgan va '5' ta pod o'chirilgan.