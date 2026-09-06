# Servis va deploymentlarni o'chirish

> 🎯 **Bu darsda nimani o'rganamiz:**
> - Manifest orqali yaratilgan obyektlarni to'g'ri o'chirish
> - Bir buyruqda bir necha manifestni o'chirish
> - O'chirishdan keyin nima qolganini tekshirish
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
endi bo'lsa quyidagi komandalar bilan servis va deploymentlarni o'chiramiz
```bash
root@test-server-k8s-1:~# kubectl delete -f deployment.yaml -f service.yaml
deployment.apps "k8s-web-hello" deleted from default namespace
service "k8s-web-hello" deleted from default namespace
```
Endi bo'sa barcha servis va deploymentlar ni qayta tekshirib olamiz
```bash
root@test-server-k8s-1:~# kubectl get deployments
No resources found in default namespace.
root@test-server-k8s-1:~# kubectl get services
NAME         TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)   AGE
kubernetes   ClusterIP   10.96.0.1    <none>        443/TCP   7d1h
```
Bu yerda servis va deploymentlar o'chirilganligini ko'rishimiz mumkin

## 🧪 Mustaqil topshiriqlar

> Taxminiy vaqt: 10 daqiqa.

**1-topshiriq · oson.** `kubectl delete -f` bilan ikkala manifestni
birdan o'chiring.

<details><summary>O'zingizni tekshiring</summary>

```bash
kubectl get all
# Faqat service/kubernetes qolishi kerak
```
</details>

**2-topshiriq · o'rta.** Butun `amaliyot/lesson1/` papkasini bitta buyruq
bilan o'chiring.

<details><summary>O'zingizni tekshiring</summary>

```bash
kubectl delete -f amaliyot/lesson1/
```
</details>

**3-topshiriq · qiyin.** Deployment'ni o'chiring, lekin Service'ni
qoldiring. **Avval ayting:** `kubectl get endpoints` nima ko'rsatadi?

<details><summary>O'zingizni tekshiring</summary>

```bash
kubectl get endpoints k8s-web-hello
# ENDPOINTS ustuni <none> — podlar yo'q, lekin Service turibdi
```
</details>

## ❓ Savol-Javob

**Savol:** `kubectl delete -f` faylni ham o'chiradimi?
**Javob:** Yo'q. U faqat klasterdagi obyektlarni o'chiradi, manifest fayli
diskda qoladi.

**Savol:** Manifest o'zgargan bo'lsa, `delete -f` ishlaydimi?
**Javob:** U obyektni **nomi va turi** bo'yicha topadi. Nom o'zgarmagan
bo'lsa ishlaydi.

**Savol:** Barcha obyektlarni birdan o'chirish mumkinmi?
**Javob:** `kubectl delete all --all` — lekin u ConfigMap va Secret'larni
qoldiradi. Ehtiyot bo'ling, buyruq orqaga qaytmaydi.

## 📌 CKA imtihon uchun maslahat

```bash
kubectl delete -f fayl.yaml
kubectl delete -f papka/                     # papkadagi hamma manifest
kubectl delete deploy,svc -l app=web         # label bo'yicha
kubectl delete pod --all -n <namespace>
```

Tez o'chirish uchun `--grace-period=0 --force`, lekin faqat Pod qotib
qolganda.

## 📖 Asosiy atamalar

| Atama | Ma'nosi |
|---|---|
| **`delete -f`** | Manifestda tasvirlangan obyektlarni o'chirish |
| **`--all`** | Berilgan turdagi barcha obyektlar |
| **Cascade delete** | Egasi o'chirilganda bog'liqlari ham o'chishi |

## 🔗 Manbalar

- [kubectl delete](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands#delete)
- [Garbage Collection](https://kubernetes.io/docs/concepts/architecture/garbage-collection/)

---
⬅️ [Oldingi dars](lesson5.md) · [Bo'lim indeksi](README.md) · ➡️ Keyingi bo'lim: [Deploymentlar](../Deploymentlar/)
