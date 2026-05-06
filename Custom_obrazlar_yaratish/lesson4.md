## Biz bindan oldingi darsda NodeJS dasturi uchun yaradik va uning imedgini Docker Hub ga yuklashni o'rgandik.
### Endi bo'lsa biz Kubernetes klastorimizda buz yaratgan Docker imegimizni ishga tushiramiz:
```bash
kubectl run k8s-web-hello --image=<dockerhub_username>/k8s-web-hello:1.0.0 --port=3000
```
Bu buyruq k8s-web-hello nomli pod yaratadi va unga <dockerhub_username>/k8s-web-hello:1.0.0 nomli Docker image ni ishlatadi. Pod 3000 portda ishga tushadi. Endi biz pod yaratdik, endi biz uning holatini tekshirishimiz kerak. Pod holatini tekshirish uchun quyidagi buyruqni bajarishimiz kerak:
```bash 
kubectl get pods
```
Yuqoridagi buyruqda biz quidagilarni ko'rshimiz mumkin:
```bash
root@test-server-k8s-1:~# kubectl run k8s-web-hello --image=<dockerhub_username>/k8s-web-hello:1.0.0 --port=3000
pod/k8s-web-hello created
root@test-server-k8s-1:~# kubectl get pods
NAME            READY   STATUS              RESTARTS   AGE
k8s-web-hello   0/1     ContainerCreating   0          7s
root@test-server-k8s-1:~#
```
Endi bo'lsa biz ushbu podning to'liqroq ma'lumotlarnini ko'rib chiqamiz.
```bash
kubectl describe pod k8s-web-hello
root@test-server-k8s-1:~# kubectl describe pod k8s-web-hello
Name:             k8s-web-hello
Namespace:        default
Priority:         0
Service Account:  default
Node:             test-server-k8s-2/192.168.16.109
Start Time:       Wed, 06 May 2026 08:59:53 +0000
Labels:           run=k8s-web-hello
Annotations:      cni.projectcalico.org/containerID: 361e8d6cfae3a1911bb5e62e5d59a7e67ed0c0c002555cf31fc9c0e7b0c605fb
                  cni.projectcalico.org/podIP: 172.16.78.131/32
                  cni.projectcalico.org/podIPs: 172.16.78.131/32
Status:           Running
IP:               172.16.78.131
IPs:
  IP:  172.16.78.131
Containers:
  k8s-web-hello:
    Container ID:   containerd://b7ae77052e591de2fd23831ce74c93db843c706afdfd659f23d5734c5c693964
    Image:          <dockerhub_username>/k8s-web-hello
    Image ID:       docker.io/<dockerhub_username>/64941526ee3c6dd909a2c1fbc7064731f9b0f2088b405df2db26b7
    Port:           3000/TCP
    Host Port:      0/TCP
    State:          Running
      Started:      Wed, 06 May 2026 09:00:02 +0000
    Ready:          True
    Restart Count:  0
    Environment:    <none>
    Mounts:
      /var/run/secrets/kubernetes.io/serviceaccount from kube-api-access-pkrxd (ro)
Conditions:
  Type                        Status
  PodReadyToStartContainers   True
  Initialized                 True
  Ready                       True
  ContainersReady             True
  PodScheduled                True
Volumes:
  kube-api-access-pkrxd:
    Type:                    Projected (a volume that contains injected data from multiple sources)
    TokenExpirationSeconds:  3607
    ConfigMapName:           kube-root-ca.crt
    Optional:                false
    DownwardAPI:             true
QoS Class:                   BestEffort
Node-Selectors:              <none>
Tolerations:                 node.kubernetes.io/not-ready:NoExecute op=Exists for 300s
                             node.kubernetes.io/unreachable:NoExecute op=Exists for 300s
Events:
  Type    Reason     Age    From               Message
  ----    ------     ----   ----               -------
  Normal  Scheduled  4m26s  default-scheduler  Successfully assigned default/k8s-web-hello to test-server-k8s-2
  Normal  Pulling    4m26s  kubelet            spec.containers{k8s-web-hello}: Pulling image "<dockerhub_username>/k8s-web-hello"
  Normal  Pulled     4m18s  kubelet            spec.containers{k8s-web-hello}: Successfully pulled image "<dockerhub_username>/k8s-web-hello" in 8.058s (8.058s including waiting). Image size: 61726179 bytes.
  Normal  Created    4m18s  kubelet            spec.containers{k8s-web-hello}: Container created
  Normal  Started    4m18s  kubelet            spec.containers{k8s-web-hello}: Container started

``` 
Agar biz yaratgan podimizni toxtatmoqchi bo'lsak, quyidagi buyruqni bajarishimiz kerak:
```bash
kubectl delete pod k8s-web-hello
```
Endi bo'lsa biz PODni deploymant orqali yaratamiz. Deploymant bu Kubernetes resursi bo'lib, u bizning PODlarimizni boshqarish uchun ishlatiladi. Deploymant yordamida biz PODlarimizni avtomatik ravishda yangilash, ko'paytirish yoki kamaytirish imkoniyatiga ega bo'lamiz. Deploymant yaratish uchun quyidagi buyruqni bajarishimiz kerak:
```bash
kubectl create deployment k8s-web-hello --image=<dockerhub_username>/k8s-web-hello:1.0.0
```
Bu buyruq k8s-web-hello nomli deploymant yaratadi va unga <dockerhub_username>/k8s-web-hello:1.0.0 nomli Docker image ni ishlatadi. Endi biz deploymant yaratdik, endi biz uning holatini tekshirishimiz kerak. Deploymant holatini tekshirish uchun quyidagi buyruqni bajarishimiz kerak:
```bash
kubectl get deployments
```
