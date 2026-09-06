# Yangilangan Deployment'ni tahlil qilish

> 🎯 **Bu darsda nimani o'rganamiz:**
> - Yangilanishdan keyin `describe` da nima o'zgarganini o'qish
> - ReplicaSet'lar tarixi va `rollout history`
> - Orqaga qaytish (`rollout undo`)
Analiz uchun quyidagi komandadan foydalanamiz:
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

## Orqaga qaytish

```bash
kubectl rollout history deployment k8s-web-hello
kubectl rollout undo deployment k8s-web-hello
kubectl rollout undo deployment k8s-web-hello --to-revision=2
```

`undo` yangi ReplicaSet yaratmaydi — u **eski ReplicaSet'ni qayta
masshtablaydi**. Shuning uchun u juda tez ishlaydi.

## 🧪 Mustaqil topshiriqlar

> Taxminiy vaqt: 15 daqiqa.

**1-topshiriq · oson.** `rollout history` bilan revizyalar ro'yxatini
chiqaring.

<details><summary>O'zingizni tekshiring</summary>

```bash
kubectl rollout history deployment k8s-web-hello
```
</details>

**2-topshiriq · o'rta.** Oldingi versiyaga qayting va Pod'lardagi image
tegi o'zgarganini tasdiqlang.

<details><summary>O'zingizni tekshiring</summary>

```bash
kubectl get deployment k8s-web-hello \
  -o jsonpath='{.spec.template.spec.containers[0].image}{"\n"}'
```
</details>

**3-topshiriq · qiyin.** `revisionHistoryLimit` ni 2 ga tushiring va uch
marta yangilang. **Avval ayting:** nechta eski ReplicaSet qoladi?

<details><summary>O'zingizni tekshiring</summary>

```bash
kubectl get rs -l app=k8s-web-hello
# 2 ta eski + 1 ta joriy
```
</details>

## ❓ Savol-Javob

**Savol:** `rollout undo` dan keyin revision raqami nima bo'ladi?
**Javob:** U kamaymaydi — yangi raqam qo'shiladi. Masalan 3-revizyadan
2-ga qaytsangiz, natija 4-revizya bo'ladi.

**Savol:** Barcha eski ReplicaSet'lar 0 replika bilan turibdi. O'chiraymi?
**Javob:** Kerak emas, ular resurs yemaydi. Lekin ularni o'chirsangiz,
o'sha revizyalarga `undo` qila olmaysiz.

## 📖 Asosiy atamalar

| Atama | Ma'nosi |
|---|---|
| **Rolling update** | Pod'larni bittalab almashtirib, uzilishsiz yangilash |
| **`kubectl set image`** | Deployment'dagi image'ni almashtiruvchi buyruq |
| **`kubectl rollout status`** | Yangilanish tugadimi yoki qotib qoldimi |
| **`kubectl rollout undo`** | Oldingi revizyaga qaytish |
| **Revision** | Deployment shablonining versiya raqami |
| **`maxSurge` / `maxUnavailable`** | Yangilanish paytidagi qo'shimcha va yo'q Pod'lar chegarasi |

## 🔗 Manbalar

- [Updating a Deployment](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/#updating-a-deployment)
- [kubectl rollout](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands#rollout)
- [Rolling Back a Deployment](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/#rolling-back-a-deployment)

---
⬅️ [Oldingi dars](lesson2.md) · [Bo'lim indeksi](README.md) · ➡️ [lesson4.md](lesson4.md)
