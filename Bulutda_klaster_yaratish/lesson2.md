# Klasterda yangi deploymentlarni yaratish va boshqarish

> 🎯 **Bu darsda nimani o'rganamiz:**
> - Bulut klasterida Deployment yaratish
> - Lokal va bulut klasteri orasidagi farqlar
1. Birinchi bo'lib bizda mavjud barcha deloymentlarni o'chirib tashlaymiz:
bizda mavjud deployment va servislarni tekshirib olaminz
## Endi bo'lsa quyidagi buyruqni kiriting va barcha deployment va servislarni o'chirib tashlaymiz
```bash
PS D:\project AI\k8s> kubectl.exe delete all --all 
pod "k8s-web-to-nginx-7b4dbf47f8-6pqgw" deleted from default namespace
pod "k8s-web-to-nginx-7b4dbf47f8-9nqs2" deleted from default namespace
pod "k8s-web-to-nginx-7b4dbf47f8-fqw84" deleted from default namespace
pod "k8s-web-to-nginx-7b4dbf47f8-g8h6z" deleted from default namespace
pod "k8s-web-to-nginx-7b4dbf47f8-js4cp" deleted from default namespace
pod "k8s-web-to-nginx-7b4dbf47f8-krbv4" deleted from default namespace
pod "k8s-web-to-nginx-7b4dbf47f8-m4bfb" deleted from default namespace
pod "k8s-web-to-nginx-7b4dbf47f8-s5zwm" deleted from default namespace
pod "k8s-web-to-nginx-7b4dbf47f8-w8gdk" deleted from default namespace
pod "k8s-web-to-nginx-7b4dbf47f8-xwjvs" deleted from default namespace
pod "nginx-86d76f4b8-68fn5" deleted from default namespace
pod "nginx-86d76f4b8-lmklw" deleted from default namespace
pod "nginx-86d76f4b8-vtrmm" deleted from default namespace
pod "nginx-86d76f4b8-xndxx" deleted from default namespace
pod "nginx-86d76f4b8-z29qj" deleted from default namespace
service "k8s-web-to-nginx" deleted from default namespace
service "kubernetes" deleted from default namespace
service "nginx" deleted from default namespace
deployment.apps "k8s-web-to-nginx" deleted from default namespace
deployment.apps "nginx" deleted from default namespace
```
yana qayta tekshirib olamiz
```bash
PS D:\project AI\k8s> kubectl.exe get all
NAME                 TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)   AGE
service/kubernetes   ClusterIP   10.96.0.1    <none>        443/TCP   78s
```
Endi bizda faqatgina `kubernetes` servisi qoldi, boshqa barcha resurslar o'chirilgan. ✅

Endi bo'lsa biz yaratgan ikkita deployment va servisni qayta yaratamiz:
```bash
PS D:\project AI\k8s\2_xil_YAML_yaratish> kubectl.exe apply -f k8s-web-to-nginx.yaml -f nginx.yaml
service/k8s-web-to-nginx created
deployment.apps/k8s-web-to-nginx created
service/nginx created
deployment.apps/nginx created
```
Tekshirish:
```bash
PS D:\project AI\k8s\2_xil_YAML_yaratish> kubectl.exe get all                                     
NAME                                    READY   STATUS    RESTARTS   AGE
pod/k8s-web-to-nginx-7b4dbf47f8-6cc2q   1/1     Running   0          7s
pod/k8s-web-to-nginx-7b4dbf47f8-g86js   1/1     Running   0          7s
pod/k8s-web-to-nginx-7b4dbf47f8-gqr57   1/1     Running   0          7s
pod/nginx-86d76f4b8-9g4kj               1/1     Running   0          6s
pod/nginx-86d76f4b8-bkjlp               1/1     Running   0          6s
pod/nginx-86d76f4b8-gd84c               1/1     Running   0          6s
pod/nginx-86d76f4b8-rvkzz               1/1     Running   0          6s
pod/nginx-86d76f4b8-snbvv               1/1     Running   0          6s

NAME                       TYPE           CLUSTER-IP      EXTERNAL-IP   PORT(S)          AGE
service/k8s-web-to-nginx   LoadBalancer   10.105.194.35   <pending>     3333:30687/TCP   7s
service/kubernetes         ClusterIP      10.96.0.1       <none>        443/TCP          3m47s
service/nginx              ClusterIP      10.99.39.13     <none>        80/TCP           7s

NAME                               READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/k8s-web-to-nginx   3/3     3            3           7s
deployment.apps/nginx              5/5     5            5           7s

NAME                                          DESIRED   CURRENT   READY   AGE
replicaset.apps/k8s-web-to-nginx-7b4dbf47f8   3         3         3       7s
replicaset.apps/nginx-86d76f4b8               5         5         5       7s
PS D:\project AI\k8s\2_xil_YAML_yaratish> 
```
Yuqoridagi natijada ko'rishimiz mumkinki, barcha podlar `Running` holatida va kerakli sonlarda mavjud. Servislar ham muvaffaqiyatli yaratilgan va `kubernetes` servisi bundan mustasno, u hali ham mavjud. ✅

## 🧪 Mustaqil topshiriq

**Topshiriq.** Bulut klasteringizda 3 replikali nginx Deployment yarating
va Pod'lar turli node'larga tushganini tekshiring.

<details><summary>O'zingizni tekshiring</summary>

```bash
kubectl get pods -o wide
# NODE ustunida kamida ikkita har xil node bo'lishi kerak
```
</details>

## ❓ Savol-Javob

**Savol:** Lokal minikube'dagi manifest bulutda ham ishlaydimi?
**Javob:** Deyarli har doim ha. Farq faqat LoadBalancer (bulutda haqiqiy
IP beriladi) va StorageClass (har provayderda o'zining nomi bor) da.

## 📖 Asosiy atamalar

| Atama | Ma'nosi |
|---|---|
| **Managed Kubernetes** | Bulut provayderi control plane'ni o'zi boshqaradigan xizmat |
| **Node pool** | Bir xil sozlamali worker node'lar guruhi |
| **kubeconfig** | Klasterga ulanish ma'lumotlari saqlanadigan fayl |
| **Kontekst (context)** | kubeconfig ichidagi "qaysi klaster + qaysi foydalanuvchi" juftligi |
| **NAT** | Ichki manzillarni tashqi IP orqali ko'rsatuvchi tarmoq mexanizmi |

## 🔗 Manbalar

- [Kubernetes on Cloud Providers](https://kubernetes.io/docs/setup/production-environment/turnkey-solutions/)
- [Organizing Cluster Access Using kubeconfig](https://kubernetes.io/docs/concepts/configuration/organize-cluster-access-kubeconfig/)
- [DigitalOcean Kubernetes](https://docs.digitalocean.com/products/kubernetes/)

---
⬅️ [Oldingi dars](lesson1.md) · [Bo'lim indeksi](README.md) · ➡️ [lesson3.md](lesson3.md)
