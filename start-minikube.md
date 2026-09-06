# 🚀 minikube bilan boshlash

Bu darslikdagi deyarli barcha amaliyotni o'z kompyuteringizda bajarish
mumkin. Buning uchun **minikube** — bitta mashinada ishlaydigan kichik
Kubernetes klasteri yetarli.

> 🎯 **Bu qo'llanmada nimani o'rganamiz:**
> - minikube'ni ishga tushirish va to'xtatish
> - `kubectl` uchun qisqa `k` taxallusi (alias) yaratish
> - Klaster ishlayotganini tekshiradigan birinchi buyruqlar
> - Birinchi Pod'ni yaratish

## 1. Talab qilinadigan dasturlar

| Dastur | Nima uchun | Tekshirish |
|---|---|---|
| Docker (yoki boshqa driver) | minikube klasterni konteyner ichida ko'taradi | `docker version` |
| minikube | klasterning o'zi | `minikube version` |
| kubectl | klaster bilan gaplashish vositasi | `kubectl version --client` |

O'rnatish yo'riqnomasi: [minikube start](https://minikube.sigs.k8s.io/docs/start/)
va [kubectl o'rnatish](https://kubernetes.io/docs/tasks/tools/).

## 2. Klasterni ishga tushirish

```bash
minikube start
```

Birinchi marta ishga tushganda minikube kerakli image'larni yuklab oladi —
bu bir necha daqiqa davom etishi mumkin. Keyingi safar ancha tez ochiladi.

Klaster tayyorligini tekshiramiz:

```bash
kubectl cluster-info
kubectl get nodes
```

`kubectl get nodes` da bitta node `Ready` holatida ko'rinishi kerak:

```text
NAME       STATUS   ROLES           AGE   VERSION
minikube   Ready    control-plane   1m    v1.31.0
```

## 3. `k` taxallusini yaratish

`kubectl` so'zini kuniga yuz marta yozish charchatadi. Qisqartiramiz:

```bash
alias k=kubectl
```

Bu taxallus faqat joriy terminal seansida ishlaydi. Doimiy qilish uchun uni
shell konfiguratsiyangizga qo'shing:

```bash
# bash uchun
echo "alias k=kubectl" >> ~/.bashrc && source ~/.bashrc

# zsh uchun
echo "alias k=kubectl" >> ~/.zshrc && source ~/.zshrc
```

💡 CKA imtihonida ham birinchi ish shu — taxallusni sozlash bir necha
daqiqa vaqt tejaydi.

## 4. Namespace'larni ko'rish

Namespace — klaster ichidagi mantiqiy bo'lim. Kubernetes'ning o'z tizim
komponentlari `kube-system` namespace'ida ishlaydi.

```bash
kubectl get namespaces
```

```text
NAME              STATUS   AGE
default           Active   2m
kube-node-lease   Active   2m
kube-public       Active   2m
kube-system       Active   2m
```

Tizim podlarini ko'rish:

```bash
kubectl get pods -n kube-system
```

⚠️ **Diqqat:** namespace bayrog'i `-n` yoki `--namespace` (birlikda).
`--namespaces` degan bayroq **mavjud emas**. Barcha namespace'lardagi
podlarni ko'rish uchun `-A` (yoki `--all-namespaces`) ishlating:

```bash
kubectl get pods -A
```

## 5. Birinchi Pod

```bash
kubectl run my-nginx-pod --image=nginx:1.27-alpine
```

Bu buyruqda:

- `my-nginx-pod` — yaratilayotgan Pod'ning nomi;
- `--image=nginx:1.27-alpine` — qaysi image'dan konteyner ko'tarilishi.

> 💡 Image'ni doim versiya tegi bilan yozing. Tegsiz `nginx` bugun bir
> versiyani, ertaga boshqasini tortadi — natija takrorlanmaydigan bo'lib
> qoladi.

Pod ko'tarilganini tekshiramiz:

```bash
kubectl get pods
```

## 6. To'xtatish va tozalash

```bash
kubectl delete pod my-nginx-pod   # faqat podni o'chirish

minikube stop                     # klasterni to'xtatish (ma'lumot saqlanadi)
minikube delete                   # klasterni butunlay o'chirish
```

## 7. Foydali qo'shimchalar

```bash
minikube dashboard                # brauzerda web-interfeys
minikube addons list              # mavjud qo'shimchalar
minikube addons enable metrics-server
minikube tunnel                   # LoadBalancer servislarga tashqi IP berish
```

`minikube tunnel` alohida terminalda ochiq turishi kerak — u yopilsa,
LoadBalancer servisning tashqi IP'si ham yo'qoladi. Bu haqda batafsil:
[Servislar/lesson31.md](Servislar/lesson31.md).

## 🔗 Manbalar

- [minikube — rasmiy hujjatlar](https://minikube.sigs.k8s.io/docs/)
- [kubectl Cheat Sheet](https://kubernetes.io/docs/reference/kubectl/quick-reference/)
- [Namespace'lar](https://kubernetes.io/docs/concepts/overview/working-with-objects/namespaces/)

---
➡️ Klaster tayyor bo'lgach, birinchi darsdan boshlang:
[Podlar_asoslari](Podlar_asoslari/)
