# Yaratilgan servis va Deploymentlarni o'chirish 

> 🎯 **Bu darsda nimani o'rganamiz:**
> - Yaratilgan Deployment va Service'ni to'g'ri o'chirish
> - O'chirishdan keyin nima qolganini tekshirish
1. servisni o'chirish uchun birinchi servislarni ko'rib olamiz va o'zimimga kerak bo'lmagan servisni o'chirib tashlaymiz.
```bash
root@test-server-k8s-1:~# kubectl get services
NAME            TYPE           CLUSTER-IP      EXTERNAL-IP   PORT(S)          AGE
k8s-web-hello   LoadBalancer   10.107.19.197   <pending>     3333:31990/TCP   4h38m
kubernetes      ClusterIP      10.96.0.1       <none>        443/TCP          30h
root@test-server-k8s-1:~# kubectl delete service k8s-web-hello
service "k8s-web-hello" deleted from default namespace
root@test-server-k8s-1:~# kubectl get services
NAME         TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)   AGE
kubernetes   ClusterIP   10.96.0.1    <none>        443/TCP   30h
root@test-server-k8s-1:~#
```
Yuqorida servislarni <kubectl get services> buyruq orqali ko'rib oldik
undan so'nf  <kubectl delete service k8s-web-hello> buyruqdan foydalangan xolda servisni o'chirib tashladik
uchunchi buyruq orqali servis o'chirilganligiga ishonch xosilqilib oldik.

2. Edni bo'lsa Deploymentno o'chiramiz
``` bash
root@test-server-k8s-1:~# kubectl get deployment
NAME            READY   UP-TO-DATE   AVAILABLE   AGE
k8s-web-hello   10/10   10           10          4h44m
root@test-server-k8s-1:~# kubectl delete deployment k8s-web-hello
deployment.apps "k8s-web-hello" deleted from default namespace
root@test-server-k8s-1:~# kubectl get deployment
No resources found in default namespace.
```
Bu yerda biz deployment ni ko'rib oldik va ochirib tashladik.

3. PODlarni o'chirilganligini tekshirib olamiz
```bash
root@test-server-k8s-1:~# kubectl get pods
No resources found in default namespace.
```
Bu yerda ko'rishimiz mumkinki <default namespace>da umuman PODlar yo'q

## 🧪 Mustaqil topshiriqlar

> Taxminiy vaqt: 10 daqiqa.

**1-topshiriq · oson.** Deployment va Service'ni o'chiring, keyin
`kubectl get all` bilan tozalanganini tasdiqlang.

<details><summary>O'zingizni tekshiring</summary>

```bash
kubectl get all
# Faqat service/kubernetes qolishi kerak
```
</details>

**2-topshiriq · o'rta.** ReplicaSet'lar ham o'chganini tekshiring.

<details><summary>O'zingizni tekshiring</summary>

```bash
kubectl get rs
# No resources found
```
</details>

**3-topshiriq · qiyin.** Deployment'ni `--cascade=orphan` bilan o'chiring.
**Avval ayting:** ReplicaSet va Pod'lar nima bo'ladi?

<details><summary>O'zingizni tekshiring</summary>

```bash
kubectl get rs,pods
# ReplicaSet va podlar QOLADI — endi ularning egasi yo'q
```
</details>

## ❓ Savol-Javob

**Savol:** Deployment o'chirilganda Service ham o'chadimi?
**Javob:** Yo'q. Service alohida obyekt — uni qo'lda o'chirish kerak.

**Savol:** O'chirishni orqaga qaytarish mumkinmi?
**Javob:** Yo'q. Shuning uchun manifestlar git'da saqlanadi — qayta
yaratish uchun `kubectl apply -f` yetarli.

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
⬅️ [Oldingi dars](lesson3.md) · [Bo'lim indeksi](README.md) · ➡️ Keyingi bo'lim: [Ikkita_deployment_YAML](../Ikkita_deployment_YAML/)
