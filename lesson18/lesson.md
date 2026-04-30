# Lesson 18: Kubernetes Pods - To'liq Ma'lumot

## Pod nima?
Kubernetes-da **Pod** - bu eng kichik deployable birlik. U bir yoki bir nechta konteynerlarni o'z ichiga oladi va ularni birgalikda boshqaradi. Podlar umumiy tarmoq (network) va saqlash (storage) resurslarini baham ko'radi.

## Podning asosiy xususiyatlari
- **Konteynerlar**: Pod ichida bir yoki ko'proq konteyner bo'lishi mumkin. Masalan, asosiy ilova konteyneri va yordamchi konteyner (sidecar).
- **Umumiy resurslar**: Barcha konteynerlar bir xil IP-manzil, portlar va saqlash joyini ishlatadi.
- **Ephemeral**: Podlar vaqtinchalik bo'lib, muammo yuz berganda avtomatik tarzda qayta yaratilishi mumkin.
- **Scaling**: Podlar Deployment yoki ReplicaSet orqali ko'paytiriladi.

## Pod yaratish
Podni YAML fayl orqali yaratish misoli:

```yaml
apiVersion: v1
kind: Pod
metadata:
    name: my-pod
    labels:
        app: my-app
spec:
    containers:
    - name: my-container
        image: nginx:latest
        ports:
        - containerPort: 80
```

Bu YAML faylni `kubectl apply -f pod.yaml` bilan qo'llash mumkin.

## Pod lifecycle
- **Pending**: Pod yaratilmoqda.
- **Running**: Pod ishlayapti.
- **Succeeded/Failed**: Pod tugagan yoki xatolik yuz bergan.
- **Unknown**: Holat noma'lum.

## Pod boshqaruvi
- **Kubectl buyruqlari**:
    - `kubectl get pods`: Podlarni ko'rish.
    - `kubectl describe pod <pod-name>`: Pod haqida batafsil ma'lumot.
    - `kubectl logs <pod-name>`: Loglarni ko'rish.
    - `kubectl delete pod <pod-name>`: Podni o'chirish.

## Multi-container Pods
- **Sidecar pattern**: Asosiy konteyner bilan yordamchi konteyner (masalan, log yig'uvchi).
- **Init containers**: Pod ishga tushishdan oldin bajariladigan konteynerlar.

## Best Practices
- Podlarni to'g'ridan-to'g'ri ishlatmang; Deployment orqali boshqaring.
- Resurs limitlarini belgilang (CPU, memory).
- Health checks (liveness va readiness probes) qo'shing.

Bu darsda Podlar haqida asosiy tushunchalar berildi. Keyingi darslarda Deployment va Services ko'rib chiqiladi.

Server001:> kubectl describe pod my-nginx-pod
Name:         my-nginx-pod  
Namespace:    default  
Priority:     0
Node:         minikube/
Start Time:   Wed, 01 Jan 2020 00:00:00 +0000
Labels:       app=my-app
Annotations:  <none>
Status:       Running
IP:
Containers:
  my-container:
    Container ID:   docker://abcdef123456
    Image:          nginx:latest
    Image ID:       docker-pullable://nginx@sha256:abcdef123456
    Port:           80/TCP
    State:          Running
      Started:      Wed, 01 Jan 2020 00:01:00 +0000
    Ready:          True
    Restart Count:  0
Events:
  Type    Reason     Age   From               Message
    ----    ------     ----  ----               -------     
    Bu yerda podning holati, konteynerlar haqida ma'lumot va voqealar (events) ko'rsatiladi.
```
Server001:> kubectl get pods
NAME            READY   STATUS    RESTARTS   AGE    
my-nginx-pod   1/1     Running   0          5m
``` 
Bu buyruq orqali barcha podlarni ko'rish mumkin. `READY` ustuni konteynerlarning tayyorligini ko'rsatadi, `STATUS` esa podning hozirgi holatini bildiradi.

![alt text](image.png)
