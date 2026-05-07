# YAML faylning kubernetis klastorida qo'llanilishi

Kubernetis klastorida `Deployment` yaratish uchun `YAML` fayl yaratishni o'rganishga mo'ljallangan.
Xozirda biz yaratgan <deployment.yaml> fayli mavjud va biz uni kubernetes klasterida ishga tushiramiz:
buning uchun quidagi buyruqni ishlatamiz:

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
bu yerda biz deploymentni kubernetis klastorida yaratdik va uning holatini tekshirib oldik.

