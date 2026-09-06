### Birinchi deployment yakuni bo'yicha xulosa
Biz birinchi deploymentni yaratdik va unga servis yaratdik. Servisning turi 'ClusterIP' edi. Bu turdagi servis klaster ichidagi podlarga kirish imkonini beradi, lekin tashqi dunyo orqali kirish mumkin emas.
Endi bo'sa barcha yaratgan servis va deploymentlarimizni tashlaymiz.
```
root@test-server-k8s-1:~# kubectl delete deployment nginx-deploy -n default
deployment.apps "nginx-deploy" deleted
root@test-server-k8s-1:~# kubectl delete service nginx-deploy -n default
service "nginx-deploy" deleted from default namespace   
```


