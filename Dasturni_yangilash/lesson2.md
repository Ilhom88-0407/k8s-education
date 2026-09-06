# NodeJS dasturini yangilaymiz

> 🎯 **Bu darsda nimani o'rganamiz:**
> - `kubectl set image` bilan Deployment'ni yangilash
> - `kubectl rollout status` bilan jarayonni kuzatish
> - Rolling update davomida eski va yangi Pod'lar birga ishlashi
NodeJS dasturini obnavleniya qilishdan oldin yangilanish protsesini ko'rib tursih uchun quyidagi komandalarni kiritib olamiz:
```bash
kubectl rollout status deployment/k8s-web-hello
```
NodeJS dasturini yangilash uchun quyidagi komandani kirgizamiz:
```bash
kubectl set image deployment k8s-web-hello k8s=mrpocker88/k8s:ver2
misol uchun
kubectl set image deployment k8s-web-hello k8s=mrpocker88/k8s-web-hello:1.0.2
```
shundan keyin Web_brauzerga kirib tekshirildi:
![Brauzerda 194.107.115.75:31990 manzili ochilgan va sahifada "VERSION 3: Hello from the k8s-web-hello-554b8c5484-xvl9w" yozuvi ko'rinadi](image.png)

```
C:\Users\admin>curl http://194.107.115.75:31990/
<h1>VERSION 3: Hello from the k8s-web-hello-554b8c5484-fnz8n</h1>
```
Agar biz quyidagi komandani ishga tushirilsa bizning repligalarimiz yangisiga o'zgarishini ko'rishimiz mumkin:
```
kubectl rollout status deployment/k8s-web-hello
```

![kubectl set image buyrug'i "deployment.apps/k8s-web-hello image updated" javobini qaytardi, keyingi kubectl rollout status esa 7 replikadan 3 tasi yangilanganini ko'rsatyapti](image-1.png)
![kubectl rollout status chiqishi: "Waiting for deployment k8s-web-hello rollout to finish" xabari takrorlanib, yangilangan replikalar soni 3 dan 4 ga o'tyapti](image-2.png)
Quida bizning podlarimiz yangi NodeJS dasturida ishlayotganini ko'rishimiz mumkin.
![kubectl get pods chiqishi: eski ReplicaSet (56f7558d6c) ning 7 ta podi Terminating holatida, yangi ReplicaSet (9f9658788) ning 7 ta podi esa Running holatida — rolling update aynan shunday ko'rinadi](image-3.png)

## 🧪 Mustaqil topshiriqlar

> Taxminiy vaqt: 20 daqiqa.

**1-topshiriq · oson.** `kubectl set image` bilan yangi versiyani chiqaring.

<details><summary>O'zingizni tekshiring</summary>

```bash
kubectl rollout status deployment k8s-web-hello
# "successfully rolled out"
```
</details>

**2-topshiriq · o'rta.** Yangilanish paytida `kubectl get pods --watch`
bilan kuzating. Eski va yangi Pod'lar bir vaqtda bo'ladimi?

<details><summary>O'zingizni tekshiring</summary>

```bash
kubectl get rs -l app=k8s-web-hello
# Ikkita ReplicaSet: biri kamayib, ikkinchisi o'sib boradi
```
</details>

**3-topshiriq · qiyin.** Mavjud bo'lmagan tegga yangilang. **Avval ayting:**
ishlab turgan ilova uziladimi?

<details><summary>O'zingizni tekshiring</summary>

```bash
kubectl set image deployment/k8s-web-hello k8s-web-hello=nginx:9.99-yoq
kubectl get pods
# Eski podlar ISHLAB TURADI. Yangisi ImagePullBackOff da qoladi va
# maxUnavailable chegarasi eskilarini himoya qiladi.
kubectl rollout undo deployment k8s-web-hello
```
</details>

## ❓ Savol-Javob

**Savol:** Yangilanish qotib qoldi. Nima qilay?
**Javob:** `kubectl rollout status` `ProgressDeadlineExceeded` desa —
`kubectl describe pod` bilan yangi Pod'ning muammosini toping, keyin
`kubectl rollout undo`.

**Savol:** Yangilanishni to'xtatib turish mumkinmi?
**Javob:** Ha: `kubectl rollout pause deployment <nom>`, keyin
`kubectl rollout resume`.

**Savol:** `set image` va manifestni tahrirlash — qaysi biri?
**Javob:** `set image` tez, lekin manifestda eski teg qoladi. Ishlab
chiqarishda manifestni tahrirlab `apply` qiling.

## 📌 CKA imtihon uchun maslahat

```bash
kubectl set image deployment/<nom> <konteyner>=<image>:<teg> --record
kubectl rollout status deployment/<nom>
kubectl rollout undo deployment/<nom> --to-revision=2
```

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
⬅️ [Oldingi dars](Lesson1.md) · [Bo'lim indeksi](README.md) · ➡️ [lesson3.md](lesson3.md)
