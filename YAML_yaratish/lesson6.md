# servis va deplomantlarni o'chirish 
Birinchi bo'lib servis va deploymentlarni tekshirib olamiz
```bash
root@test-server-k8s-1:~# kubectl get deployments
NAME            READY   UP-TO-DATE   AVAILABLE   AGE
k8s-web-hello   10/10   10           10          4d23h
root@test-server-k8s-1:~# kubectl get services
NAME            TYPE           CLUSTER-IP      EXTERNAL-IP   PORT(S)          AGE
k8s-web-hello   LoadBalancer   10.100.61.176   <pending>     3030:30760/TCP   3d23h
kubernetes      ClusterIP      10.96.0.1       <none>        443/TCP          7d1h
```
endi bo'lsa quidagi komandalar bilan servis va deplomantlarni o'chiramiz
```bash
root@test-server-k8s-1:~# kubectl delete -f deployment.yaml -f service.yaml
deployment.apps "k8s-web-hello" deleted from default namespace
service "k8s-web-hello" deleted from default namespace
```
Endi bo'sa barcha servis va deplomantlar ni qayta tekshirib olamiz
```bash
root@test-server-k8s-1:~# kubectl get deployments
No resources found in default namespace.
root@test-server-k8s-1:~# kubectl get services
NAME         TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)   AGE
kubernetes   ClusterIP   10.96.0.1    <none>        443/TCP   7d1h
```
Bu yerda servis va deplomantlar o'chirilganligini ko'rishimiz mumkin
