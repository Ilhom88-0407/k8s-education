# Image'ni Docker Hub'ga yuklash va Deployment yaratish

> 🎯 **Bu darsda nimani o'rganamiz:**
> - Image'ni teglash va Docker Hub'ga yuklash
> - Klaster image'ni qayerdan oladi
> - Deployment manifestida o'z image'ingizni ko'rsatish
### Endi bo'lsa biz Kubernetes klastorimizda buz yaratgan Docker imegimizni ishga tushiramiz:
```bash
kubectl run k8s-web-hello --image=<dockerhub_username>/k8s-web-hello:1.0.0 --port=3000
```
Bu buyruq k8s-web-hello nomli pod yaratadi va unga <dockerhub_username>/k8s-web-hello:1.0.0 nomli Docker image ni ishlatadi. Pod 3000 portda ishga tushadi. Endi biz pod yaratdik, endi biz uning holatini tekshirishimiz kerak. Pod holatini tekshirish uchun quyidagi buyruqni bajarishimiz kerak:
```bash 
kubectl get pods
```
Yuqoridagi buyruqda biz quyidagilarni ko'rshimiz mumkin:
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
Endi bo'lsa biz PODni deployment orqali yaratamiz. Deployment bu Kubernetes resursi bo'lib, u bizning PODlarimizni boshqarish uchun ishlatiladi. Deployment yordamida biz PODlarimizni avtomatik ravishda yangilash, ko'paytirish yoki kamaytirish imkoniyatiga ega bo'lamiz. Deployment yaratish uchun quyidagi buyruqni bajarishimiz kerak:
```bash
kubectl create deployment k8s-web-hello --image=<dockerhub_username>/k8s-web-hello:1.0.0
```
Bu buyruq k8s-web-hello nomli deployment yaratadi va unga <dockerhub_username>/k8s-web-hello:1.0.0 nomli Docker image ni ishlatadi. Endi biz deployment yaratdik, endi biz uning holatini tekshirishimiz kerak. Deployment holatini tekshirish uchun quyidagi buyruqni bajarishimiz kerak:
```bash
kubectl get deployments
```

## 🧪 Mustaqil topshiriqlar

> Taxminiy vaqt: 20 daqiqa.

**1-topshiriq · oson.** Image'ni o'z Docker Hub hisobingiz nomi bilan
teglang va yuklang.

<details><summary>O'zingizni tekshiring</summary>

```bash
docker tag k8s-web-hello:1.0.3 <foydalanuvchi>/k8s-web-hello:1.0.3
docker push <foydalanuvchi>/k8s-web-hello:1.0.3
docker pull <foydalanuvchi>/k8s-web-hello:1.0.3   # boshqa mashinadan tortiladimi
```
</details>

**2-topshiriq · o'rta.** Deployment yarating va Pod'lar image'ni
tortganini tekshiring.

<details><summary>O'zingizni tekshiring</summary>

```bash
kubectl describe pod <nom> | grep -E 'Image:|Pulled'
```
</details>

**3-topshiriq · qiyin.** Image tegini mavjud bo'lmagan raqamga
o'zgartiring. **Avval ayting:** Pod qanday `STATUS` oladi?

<details><summary>O'zingizni tekshiring</summary>

```bash
kubectl get pods
# ImagePullBackOff
kubectl describe pod <nom> | tail -6
```
</details>

## ❓ Savol-Javob

**Savol:** minikube'da lokal image'ni push qilmasdan ishlatsam bo'ladimi?
**Javob:** Ha: `eval $(minikube docker-env)` deb Docker'ni minikube ichiga
yo'naltiring, keyin `docker build` qiling. Yoki `minikube image load <nom>`.

**Savol:** Xususiy registry'dan image tortish qanday?
**Javob:** `imagePullSecrets` kerak:

```bash
kubectl create secret docker-registry regcred \
  --docker-server=<server> --docker-username=<user> --docker-password=<parol>
```

**Savol:** `imagePullPolicy` nima qiladi?
**Javob:** `IfNotPresent` (standart) — node'da bor bo'lsa tortmaydi.
`Always` — har safar tortadi. Tegi `latest` bo'lsa standart qiymat
avtomatik `Always` ga o'zgaradi.

## 📌 CKA imtihon uchun maslahat

```bash
kubectl set image deployment/<nom> <konteyner>=<image>:<teg>
kubectl create secret docker-registry regcred --docker-server=... 
```

## 📖 Asosiy atamalar

| Atama | Ma'nosi |
|---|---|
| **Image** | Ilova va uning muhitidan iborat o'zgarmas qolip |
| **Konteyner** | Ishga tushirilgan image nusxasi |
| **Dockerfile** | Image qanday qurilishini tasvirlovchi fayl |
| **Registry** | Image'lar saqlanadigan omborxona (Docker Hub, GHCR, ECR) |
| **Teg (tag)** | Image versiyasini bildiruvchi belgi: `:1.0.3` |
| **Qatlam (layer)** | Dockerfile'ning har bir buyrug'i hosil qiladigan bo'lak |

## 🔗 Manbalar

- [Dockerfile reference](https://docs.docker.com/reference/dockerfile/)
- [Images — kubernetes.io](https://kubernetes.io/docs/concepts/containers/images/)
- [Node.js Docker best practices](https://github.com/nodejs/docker-node/blob/main/docs/BestPractices.md)

---
⬅️ [Oldingi dars](lesson3.md) · [Bo'lim indeksi](README.md) · ➡️ [lesson5.md](lesson5.md)
