# Deploymant uchun bizda 2 ta yaml fayl mavjud va bu fayllar o'zaro qo'liq bo'lishi kerak.
- birinchi yaml fayl bu k8s-web-hello-deployment.yaml
- ikkinchi yaml fayl bu nginx.yaml
## Endi bo'lsa ushbu ikkita deploymentni ishga tushiramiz
```bash
kubectl apply -f k8s-web-hello-deployment.yaml -f nginx.yaml
service/k8s-web-to-nginx created
deployment.apps/k8s-web-to-nginx created
service/nginx created
deployment.apps/nginx created
```
Endi bo'lsa deployment va servislarni tekshirib olamiz
```bash
root@test-server-k8s-1:~/lesson21# kubectl get deployment
NAME               READY   UP-TO-DATE   AVAILABLE   AGE
k8s-web-to-nginx   0/3     3            0           8s
nginx              0/5     5            0           8s
root@test-server-k8s-1:~/lesson21# kubectl get service
NAME               TYPE           CLUSTER-IP      EXTERNAL-IP   PORT(S)          AGE
k8s-web-to-nginx   LoadBalancer   10.96.157.129   <pending>     3333:30807/TCP   14s
kubernetes         ClusterIP      10.96.0.1       <none>        443/TCP          7d5h
nginx              ClusterIP      10.109.39.5     <none>        80/TCP           14s
root@test-server-k8s-1:~/lesson21#
```
Bu yerda biz deploymentlarni 3 ta replikada yaralganini ko'rishimiz mumkin va k8s-web-to-nginx hamda nginx servislarini ko'rishimiz mumkin.


```bash
root@test-server-k8s-1:~/lesson21# kubectl get pods
NAME                                READY   STATUS    RESTARTS   AGE
k8s-web-to-nginx-7b4dbf47f8-6pqgw   1/1     Running   0          5m47s
k8s-web-to-nginx-7b4dbf47f8-s5zwm   1/1     Running   0          5m47s
k8s-web-to-nginx-7b4dbf47f8-w8gdk   1/1     Running   0          5m47s
nginx-86d76f4b8-68fn5               1/1     Running   0          5m47s
nginx-86d76f4b8-lmklw               1/1     Running   0          5m47s
nginx-86d76f4b8-vtrmm               1/1     Running   0          5m47s
nginx-86d76f4b8-xndxx               1/1     Running   0          5m47s
nginx-86d76f4b8-z29qj               1/1     Running   0          5m47s
```
Bu yerda biz deploymentlarni 3 ta replikada yaralganini ko'rishimiz mumkin va k8s-web-to-nginx hamda nginx servislarini ko'rishimiz mumkin.

```bash
root@test-server-k8s-1:~/lesson21# kubectl describe pod nginx-86d76f4b8-68fn5
Name:             nginx-86d76f4b8-68fn5
Namespace:        default
Priority:         0
Service Account:  default
Node:             test-server-k8s-2/192.168.16.109
Start Time:       Tue, 12 May 2026 13:38:42 +0000
Labels:           app=nginx
                  pod-template-hash=86d76f4b8
Annotations:      cni.projectcalico.org/containerID: 42b3ad4b3797c2ce74d4f4664c3df5cef2434d3416e48189db94a713683b58ac
                  cni.projectcalico.org/podIP: 172.16.78.168/32
                  cni.projectcalico.org/podIPs: 172.16.78.168/32
Status:           Running
IP:               172.16.78.168
IPs:
  IP:           172.16.78.168
Controlled By:  ReplicaSet/nginx-86d76f4b8
Containers:
  nginx:
    Container ID:   containerd://37d3d89da251376de35071650020d5cc846ce9a23d76b659fd06c5ef59db3d0e
    Image:          nginx
    Image ID:       docker.io/library/nginx@sha256:1881968aff6f7cdcc4b888c00a11f4ce241ad7ec957e0cb4a9e19e93a3ff87ea
    Port:           80/TCP
    Host Port:      0/TCP
    State:          Running
      Started:      Tue, 12 May 2026 13:39:03 +0000
    Ready:          True
    Restart Count:  0
    Limits:
      cpu:     125m
      memory:  128Mi
    Requests:
      cpu:        125m
      memory:     128Mi
    Environment:  <none>
    Mounts:
      /var/run/secrets/kubernetes.io/serviceaccount from kube-api-access-z2bb5 (ro)
Conditions:
  Type                        Status
  PodReadyToStartContainers   True
  Initialized                 True
  Ready                       True
  ContainersReady             True
  PodScheduled                True
Volumes:
  kube-api-access-z2bb5:
    Type:                    Projected (a volume that contains injected data from multiple sources)
    TokenExpirationSeconds:  3607
    ConfigMapName:           kube-root-ca.crt
    Optional:                false
    DownwardAPI:             true
QoS Class:                   Guaranteed
Node-Selectors:              <none>
Tolerations:                 node.kubernetes.io/not-ready:NoExecute op=Exists for 300s
                             node.kubernetes.io/unreachable:NoExecute op=Exists for 300s
Events:
  Type    Reason     Age    From               Message
  ----    ------     ----   ----               -------
  Normal  Scheduled  8m25s  default-scheduler  Successfully assigned default/nginx-86d76f4b8-68fn5 to test-server-k8s-2
  Normal  Pulling    8m25s  kubelet            spec.containers{nginx}: Pulling image "nginx"
  Normal  Pulled     8m5s   kubelet            spec.containers{nginx}: Successfully pulled image "nginx" in 10.451s (20.304s including waiting). Image size: 62964090 bytes.
  Normal  Created    8m5s   kubelet            spec.containers{nginx}: Container created
  Normal  Started    8m5s   kubelet            spec.containers{nginx}: Container started
```
Bu yerda podni qanday ishga tushganini ko'rishimiz mumkin.

Brouzerda http://194.107.115.75:30807/ kiritsangiz ekaranda : 
<Hello from the k8s-web-to-nginx-7b4dbf47f8-s5zwm> ko'rishingiz mumkin.
Agarda http://194.107.115.75:30807/nginx kiritsangiz:
```html
Welcome to nginx!
If you see this page, nginx is successfully installed and working. Further configuration is required for the web server, reverse proxy, API gateway, load balancer, content cache, or other features.

For online documentation and support please refer to nginx.org.
To engage with the community please visit community.nginx.org.
For enterprise grade support, professional services, additional security features and capabilities please refer to f5.com/nginx.

Thank you for using nginx.
```
Yozuvini ko'rishingiz mumkin.