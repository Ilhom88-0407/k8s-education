# Dars 324 — Mock Exam 3: Barcha savollarning yechimlari

> 🎯 **Bu imtihon haqida qisqacha:**
> - Mock Exam 3 — CKA kursining eng oxirgi va eng "aralash" sinov imtihoni: 14 ta savol bor.
> - Mavzular: kubeadm uchun tizim sozlamalari, RBAC, StorageClass, ConfigMap, PriorityClass, NetworkPolicy, Taint/Toleration, PV/PVC troubleshooting, kubeconfig tuzatish, control plane troubleshooting, HPA, Gateway API, Helm va JSONPath.
> - Ustozning bosh maslahati: **rasmiy hujjatlar (kubernetes.io) imtihon paytida ochiq bo'ladi** — qaysi mavzu qayerda turishini oldindan bilib oling, chunki hamma YAML'ni yoddan yozib bo'lmaydi.
> - Yana bir oltin qoida: resurs nomlarini (pod, deployment, ClusterRole...) hech qachon qo'lda termang — **savol matnidan nusxa oling**. Imtihon tekshiruvi aynan shu nomni qidiradi, bitta harf xatosi ball yo'qotishga olib keladi.

Oddiy o'xshatish: mock imtihon — haydovchilik imtihonidan oldingi mashq maydoni. Bu yerda yiqilsangiz hech narsa yo'qotmaysiz, lekin har bir xatodan saboq olasiz. Keling, 14 ta savolni birma-bir yechamiz.

---

### 1-savol: kubeadm uchun tarmoq parametrlarini sozlash

**Masala:** Siz kubeadm yordamida yangi klaster tayyorlayotgan administratorsiz. Tizimda quyidagi tarmoq parametrlarini yoqing va o'zgarishlar **reboot'dan keyin ham saqlanishini** ta'minlang (IPv4 forwarding va bridge trafigini iptables'dan o'tkazish).

**Yechim:**

```bash
# /etc/sysctl.d/ ichida doimiy konfiguratsiya faylini yaratamiz
cat <<EOF | sudo tee /etc/sysctl.d/k8s.conf
net.bridge.bridge-nf-call-iptables  = 1
net.ipv4.ip_forward                 = 1
EOF

# Parametrlarni reboot qilmasdan darhol qo'llaymiz
sudo sysctl --system

# Tekshirib olamiz
sysctl net.ipv4.ip_forward
# net.ipv4.ip_forward = 1
```

**Tushuntirish:** Har qanday yangi Kubernetes serverida container runtime ishlashidan oldin shu ikki funksiya yoqilgan bo'lishi shart. Buyruqlarni yodlash shart emas — kubernetes.io'da "kubeadm" deb qidirsangiz, **"Creating a cluster with kubeadm" → "Container Runtimes"** sahifasida tayyor buyruqlar turadi. Ularni nusxalab terminalga tashlash kifoya. Parametrlar `/etc/sysctl.d/k8s.conf` faylga yozilgani uchun reboot'dan keyin ham saqlanadi, `sysctl --system` esa ularni hozirning o'zida ishga tushiradi.

⚠️ **Tez-tez qilinadigan xato:** Parametrni faqat `sysctl -w` bilan yoqib qo'yish — bu reboot'dan keyin yo'qoladi. Savol "persist reboots" deganda albatta faylga yozish kerak.

---

### 2-savol: ServiceAccount, ClusterRole va ClusterRoleBinding (RBAC)

**Masala:** `pvviewer` nomli ServiceAccount yarating; unga klasterdagi barcha PersistentVolume'larni ko'rish (list) huquqini beruvchi `pvviewer-role` ClusterRole va `pvviewer-role-binding` ClusterRoleBinding yarating. So'ng default namespace'da `redis` image'li, shu ServiceAccount biriktirilgan `pvviewer` nomli pod yarating.

**Yechim:** Bu yerda 3 ta ish bor: akkaunt → huquq → biriktirish, keyin pod.

```bash
# 1) ServiceAccount yaratamiz
kubectl create serviceaccount pvviewer
kubectl get serviceaccount        # pvviewer paydo bo'lganini ko'ramiz

# 2) ClusterRole — PersistentVolume'larni list qilish huquqi bilan
kubectl create clusterrole pvviewer-role \
  --resource=persistentvolumes --verb=list
kubectl describe clusterrole pvviewer-role

# 3) ClusterRoleBinding — rolni ServiceAccount'ga bog'laymiz
kubectl create clusterrolebinding pvviewer-role-binding \
  --clusterrole=pvviewer-role \
  --serviceaccount=default:pvviewer
kubectl describe clusterrolebinding pvviewer-role-binding
```

Endi pod uchun YAML (`question2.yaml`):

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: pvviewer
spec:
  serviceAccountName: pvviewer
  containers:
  - name: pvviewer
    image: redis
```

```bash
kubectl apply -f question2.yaml
kubectl describe pod pvviewer | grep -i "Service Account"
# Service Account:  pvviewer
```

**Tushuntirish:** `--serviceaccount` flagining formati doim `namespace:nom` bo'ladi, shuning uchun `default:pvviewer` deb yozdik. Pod'ga akkauntni `spec.serviceAccountName` maydoni orqali biriktiramiz. PersistentVolume — klaster darajasidagi (namespace'siz) resurs, shuning uchun oddiy Role emas, aynan **ClusterRole** kerak.

⚠️ **Tez-tez qilinadigan xato:** Nomlarni qo'lda terib xato qilish. Ustoz alohida ta'kidlaydi: `pvviewer-role`, `pvviewer-role-binding` kabi nomlarni savoldan nusxa oling — validatsiya aynan shu nomlarni tekshiradi.

---

### 3-savol: StorageClass yaratish

**Masala:** `rancher-sc` nomli StorageClass yarating: provisioner `rancher.io/local-path`, volume expansion yoqilgan, volumeBindingMode esa `WaitForFirstConsumer` bo'lsin.

**Yechim:** Hujjatlardan "storage class" deb qidirib, namunaviy YAML'ni olamiz va kerakli joylarini o'zgartiramiz:

```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: rancher-sc
provisioner: rancher.io/local-path
allowVolumeExpansion: true
volumeBindingMode: WaitForFirstConsumer
```

```bash
kubectl apply -f question3.yaml
kubectl get sc rancher-sc
```

**Tushuntirish:** Hujjatdagi namunada ortiqcha maydonlar (default annotatsiya, `reclaimPolicy`, `mountOptions`, `parameters`) bo'ladi — savol ularni talab qilmagani uchun olib tashlaymiz. Faqat 3 ta shart bajarilishi kerak: to'g'ri provisioner, `allowVolumeExpansion: true` va `WaitForFirstConsumer`. Keraksiz maydonni qoldirsangiz ham ko'pincha zarar qilmaydi, lekin toza YAML — kam xato degani.

---

### 4-savol: ConfigMap va uni Deployment'ga ulash

**Masala:** `cm-namespace` namespace'da `ENV=production` va `LOG_LEVEL=info` qiymatli `app-config` ConfigMap yarating. So'ng shu namespace'dagi mavjud `cm-webapp` deployment'ini ConfigMap'dagi qiymatlarni environment variable sifatida oladigan qilib o'zgartiring.

**Yechim:**

```bash
# ConfigMap'ni imperativ buyruq bilan yaratamiz
kubectl create configmap app-config -n cm-namespace \
  --from-literal=ENV=production \
  --from-literal=LOG_LEVEL=info

kubectl describe cm app-config -n cm-namespace
# Data: ENV=production, LOG_LEVEL=info

# Mavjud deployment'ni tahrirlaymiz
kubectl edit deployment cm-webapp -n cm-namespace
```

Ochilgan YAML'da container bo'limiga `envFrom` qo'shamiz:

```yaml
    spec:
      containers:
      - name: nginx
        image: nginx
        envFrom:
        - configMapRef:
            name: app-config
```

```bash
kubectl get pod -n cm-namespace
# Yangi pod bir necha soniya oldin qayta yaratilganini ko'ramiz
```

**Tushuntirish:** Kalit-qiymat juftliklari `--from-literal=KALIT=qiymat` flagi bilan beriladi (har juftlik uchun alohida flag). ConfigMap'dagi **hamma** kalitlarni birdaniga env sifatida olish uchun `envFrom` + `configMapRef` eng qisqa yo'l — har bir o'zgaruvchini alohida `valueFrom` bilan yozib o'tirish shart emas. `kubectl edit`ni saqlaganingizda deployment pod'larni avtomatik qayta yaratadi. Istasangiz `kubectl get deployment -o yaml` qilib faylga olib, tahrirlab, `apply` qilishingiz ham mumkin — natija bir xil.

---

### 5-savol: PriorityClass va pod'ga ustuvorlik berish

**Masala:** Qiymati 50000 bo'lgan `low-priority` nomli PriorityClass yarating. `low-priority` namespace'da mavjud `lp-pod` pod'ini shu klassdan foydalanadigan qilib o'zgartiring (kerak bo'lsa pod'ni qayta yarating).

**Yechim:** Hujjatlardan "Pod Priority and Preemption" sahifasidagi namunani olamiz (`question5.yaml`):

```yaml
apiVersion: scheduling.k8s.io/v1
kind: PriorityClass
metadata:
  name: low-priority
value: 50000
globalDefault: false
description: "This is a lower priority class."
```

```bash
kubectl apply -f question5.yaml

# Pod'ning joriy konfiguratsiyasini faylga olamiz
kubectl get pod lp-pod -n low-priority -o yaml > question5-pod.yaml
vi question5-pod.yaml
```

Faylda `spec` ostiga qo'shamiz va **eski `priority: 0` qatorini o'chiramiz**:

```yaml
spec:
  priorityClassName: low-priority
  # priority: 0   <-- BU QATORNI O'CHIRISH SHART!
```

```bash
# Pod'ni o'chirib qayta yaratish o'rniga bitta buyruq:
kubectl replace -f question5-pod.yaml --force
kubectl get pod -n low-priority
# lp-pod   1/1   Running
```

**Tushuntirish:** Ishlab turgan pod'ning `spec`ini o'zgartirib bo'lmaydi, shuning uchun `replace --force` ishlatamiz — u eski pod'ni o'chirib, yangisini yaratadi.

⚠️ **Tez-tez qilinadigan xato:** `-o yaml` bilan olingan faylda eski poddan qolgan `priority: 0` maydoni bo'ladi. Uni o'chirmasangiz shunday xato olasiz:

```
Error: pods "lp-pod" is forbidden: the integer value of priority (0) must not
be provided in pod spec; priority admission controller computed 50000 from
the given PriorityClass name
```

Xato matnini o'qing — u hamma narsani aytib turibdi: `priorityClassName` bergan bo'lsangiz, `priority` raqamini qo'lda berish taqiqlanadi (uni admission controller o'zi hisoblaydi). Yechim: `priority: 0` qatorini o'chirib, qayta apply qilish.

---

### 6-savol: NetworkPolicy bilan kiruvchi trafikni ochish

**Masala:** `np-test-1` pod'i va `np-test-service` service'i yaratilgan, lekin service'ga kiruvchi ulanishlar ishlamayapti. `ingress-to-nptest` nomli NetworkPolicy yaratib, service'ga 80-port orqali kiruvchi ulanishlarga ruxsat bering.

**Yechim:** Avval pod'ning label'ini aniqlaymiz — policy'ni aynan unga "yopishtirish" uchun:

```bash
kubectl get pod np-test-1 --show-labels
# LABELS: run=np-test-1
```

Hujjatlardan "network policy" namunasini olib, faqat keragini qoldiramiz (`question6.yaml`):

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: ingress-to-nptest
  namespace: default
spec:
  podSelector:
    matchLabels:
      run: np-test-1
  policyTypes:
  - Ingress
  ingress:
  - ports:
    - protocol: TCP
      port: 80
```

```bash
kubectl apply -f question6.yaml
```

**Tushuntirish:** Yo'nalishni pod nuqtai nazaridan o'ylang: bizga **kiruvchi** (incoming) trafik kerak — demak bu **Ingress** qoidasi, egress'ga oid hamma narsani namunadan o'chirib tashlaymiz. `ingress` qoidasida `from` bo'limini yozmadik — bu "istalgan poddan, faqat 80-port bo'lsa bo'ldi" degani. `podSelector` esa policy'ni `run=np-test-1` label'li podga bog'laydi (service o'zi trafikni shu podga uzatadi).

---

### 7-savol: Taint va Toleration

**Masala:** `node01` worker node'ga taint qo'yib, unga oddiy yuklar rejalashtirilmasin. So'ng taint'ga chidamsiz `dev-redis` pod'ini (image: `redis:alpine`) va node01'ga tusha oladigan, toleration'li `prod-redis` pod'ini yarating. Taint: `env_type=production:NoSchedule`.

**Yechim:**

```bash
# 1) Node'ga taint qo'yamiz: kalit=qiymat:effekt
kubectl taint node node01 env_type=production:NoSchedule

kubectl describe node node01 | grep -i taint
# Taints: env_type=production:NoSchedule

# 2) Toleration'siz oddiy pod
kubectl run dev-redis --image=redis:alpine
```

Toleration'li pod uchun YAML (`question7.yaml`) — buni imperativ buyruq bilan yozib bo'lmaydi:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: prod-redis
spec:
  containers:
  - name: prod-redis
    image: redis:alpine
  tolerations:
  - key: env_type
    operator: Equal
    value: production
    effect: NoSchedule
```

```bash
kubectl apply -f question7.yaml

# Natijani tekshiramiz — pod'lar qaysi node'ga tushdi?
kubectl get pod -o wide
# dev-redis    ...   controlplane   <-- taint'dan qochdi
# prod-redis   ...   node01         <-- toleration tufayli kirdi
```

**Tushuntirish:** Taint — node darvozasiga osilgan "begonalarga kirish mumkin emas" tablosi. Toleration — shu tabloni "o'qiy oladigan" maxsus ruxsatnoma. `dev-redis`da ruxsatnoma yo'q, shuning uchun scheduler uni boshqa node'ga (bu klasterda control plane'ga) joylashtirdi. `prod-redis`ning toleration'i taint bilan aynan mos: key `env_type`, value `production`, effect `NoSchedule`, operator `Equal`.

---

### 8-savol: PVC nima uchun bog'lanmayapti? (Troubleshooting)

**Masala:** `storage-ns` namespace'dagi `app-pvc` PersistentVolumeClaim mavjud `app-pv` PersistentVolume'ga bog'lanmayapti (Pending). Sababini toping va tuzating. **PV resursini o'zgartirish mumkin emas.**

**Yechim:**

```bash
kubectl get pv
# NAME     CAPACITY   ACCESS MODES   STATUS      ...
# app-pv   1Gi        RWO            Available

kubectl get pvc -n storage-ns
# NAME      STATUS    ...
# app-pvc   Pending

kubectl get pvc app-pvc -n storage-ns -o yaml
# accessModes:
# - ReadWriteMany     <-- PV esa ReadWriteOnce!
```

Sabab topildi: **access mode mos emas** — PV `ReadWriteOnce` (RWO), PVC esa `ReadWriteMany` (RWX) so'rayapti. PV'ga tegish mumkin emas, demak PVC'ni to'g'rilaymiz:

```bash
# PVC konfiguratsiyasini faylga olamiz
kubectl get pvc app-pvc -n storage-ns -o yaml > question8.yaml

# Faylda accessModes ni ReadWriteOnce ga o'zgartiramiz, so'ng:
kubectl delete pvc app-pvc -n storage-ns
kubectl apply -f question8.yaml

kubectl get pvc -n storage-ns
# NAME      STATUS   VOLUME   ...
# app-pvc   Bound    app-pv
```

**Tushuntirish:** PVC va PV — kalit va qulf. Bog'lanish uchun hamma shartlar mos kelishi kerak: hajm (PV sig'imi PVC so'rovidan katta yoki teng), **accessModes**, storageClass, selector'lar. Bu yerda hajm mos edi (1Gi), lekin access mode farq qilardi. PVC'ning accessModes maydoni yaratilgandan keyin o'zgarmas (immutable), shuning uchun uni o'chirib qayta yaratdik.

---

### 9-savol: Buzilgan kubeconfig faylni tuzatish

**Masala:** `/root/CKA/super.kubeconfig` faylida xatolik bor — toping va tuzating.

**Yechim:** Avval muammoni o'z ko'zimiz bilan ko'ramiz:

```bash
kubectl get node --kubeconfig /root/CKA/super.kubeconfig
# E0101 ... couldn't get current server API group list:
# dial tcp 192.168.9.84:9999: connect: connection refused
```

Fayl `9999`-portga ulanmoqchi, lekin ulanish rad etilyapti. Faylni ochib ko'ramiz:

```bash
cat /root/CKA/super.kubeconfig
# ...
# clusters:
# - cluster:
#     server: https://controlplane:9999    <-- shubhali port!
```

kube-apiserver aslida qaysi portda ishlayotganini tekshiramiz:

```bash
sudo netstat -tulnp | grep kube-apiserver
# tcp   ...   :::6443   LISTEN   .../kube-apiserver
```

Demak apiserver `6443`da, fayl esa `9999`ga qaragan. Faylda portni tuzatamiz:

```bash
vi /root/CKA/super.kubeconfig
# server: https://controlplane:6443  qilib o'zgartiramiz

kubectl get node --kubeconfig /root/CKA/super.kubeconfig
# NAME           STATUS   ...     <-- endi ishlaydi!
```

**Tushuntirish:** kube-apiserver standart holatda **6443**-portda tinglaydi — bu raqamni yodda tuting. Lekin ustoz to'g'ri yondashuvni ko'rsatadi: "balki maxsus konfiguratsiya bordir" deb taxmin qilmasdan, `netstat` bilan haqiqiy portni **tekshirib** ko'rdi.

⚠️ **Tez-tez qilinadigan xato:** "Buzilgan, tuzat" tipidagi savollarda darhol faylni titkilashga tushish. To'g'ri tartib: avval buyruqni ishlatib **xatoni ko'rish** → xato matnidan sababni o'qish → keyin tuzatish. Xato xabari (`connection refused` + IP:port) muammoni o'zi aytib turadi.

---

### 10-savol: Deployment 3 ga kengaymayapti (control plane troubleshooting)

**Masala:** `nginx-deploy` deployment'ining replikalarini 3 taga oshiring va hammasi muammosiz ishga tushishiga erishing. Muammo chiqsa — tuzating.

**Yechim:**

```bash
kubectl get deployment nginx-deploy
# READY 1/1

kubectl scale deployment nginx-deploy --replicas=3
kubectl get deployment nginx-deploy
# READY 1/3    <-- biroz kutsak ham 3 ga chiqmayapti!
```

Diagnostika zanjiri: deployment → replicaset → control plane.

```bash
kubectl describe deployment nginx-deploy
# Events: faqat "Scaled up replica set ... to 1" (8 daqiqa oldin)
# 1 -> 3 haqida hech qanday hodisa YO'Q!

kubectl describe rs <nginx-deploy-rs>
# ReplicaSet'ga ham 3 ga chiqish buyrug'i kelmagan

# Deployment/RS konfiguratsiyasi to'g'ri-yu, lekin ishlamayaptimi?
# Demak muammo control plane'da:
kubectl get pod -n kube-system
# kube-controller-manager-controlplane   0/1   ImagePullBackOff
```

Topildi! Controller manager ishlamayapti. U static pod, manifesti `/etc/kubernetes/manifests/`da:

```bash
vi /etc/kubernetes/manifests/kube-controller-manager.yaml
# image: registry.k8s.io/kube-contro1ler-manager:v1.31.0
#                                  ^ "1" raqami — "l" harfi o'rniga!
```

Fayl ichida `contro1ler` (raqamli "1" bilan) yozilgan joylar bir nechta: `image`, container `command` va boshqa qatorlarda. **Hammasini** `controller` ga to'g'rilab, saqlaymiz — kubelet static pod'ni avtomatik qayta yaratadi:

```bash
kubectl get pod -n kube-system
# kube-controller-manager-controlplane   1/1   Running

kubectl get deploy nginx-deploy
# READY 3/3   <-- controller uyg'ondi va ishini bajardi

kubectl get pod
# 3 ta nginx-deploy pod'i Running
```

**Tushuntirish:** Deployment o'z-o'zidan hech narsa qilmaydi — uni **kube-controller-manager** kuzatib, "replikalar 3 ta bo'lsin" degan xohishni amalga oshiradi. Controller o'lik bo'lsa, `scale` buyrug'i etcd'ga yoziladi-yu, lekin hech kim uni bajarmaydi. Ustozning qoidasi: *"Deployment/ReplicaSet konfiguratsiyasi to'g'ri, lekin hech narsa o'zgarmayotgan bo'lsa — control plane'ga qarang."*

⚠️ **Tez-tez qilinadigan xato:** Manifestdagi typo'ni faqat bitta joyda (masalan, `image`da) tuzatib qo'yish. Xato fayl bo'ylab bir necha joyda takrorlangan — hammasini topib to'g'rilamasangiz pod baribir ishga tushmaydi.

---

### 11-savol: Custom metrikali HorizontalPodAutoscaler

**Masala:** `api` namespace'dagi `api-deployment` uchun HPA yarating: `requests_per_second` nomli custom metrika bo'yicha, pod'lar bo'ylab o'rtacha qiymat 1000 bo'lsin; minimal replika — 1, maksimal — 20. (Metrika metrics-server'da yo'qligi haqidagi xatolarni e'tiborsiz qoldiring.)

**Yechim:** Custom metrika uchun `kubectl autoscale` buyrug'i yetmaydi — YAML yozamiz (`question11.yaml`):

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: api-hpa
  namespace: api
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: api-deployment
  minReplicas: 1
  maxReplicas: 20
  metrics:
  - type: Pods
    pods:
      metric:
        name: requests_per_second
      target:
        type: AverageValue
        averageValue: "1000"
```

```bash
kubectl apply -f question11.yaml
kubectl describe hpa api-hpa -n api
# Metrics: "requests_per_second" on pods: <unknown> / 1k
# (unknown — normal, chunki metrika hali yig'ilmayapti)
```

**Tushuntirish:** Buni bo'laklarga ajratamiz: `scaleTargetRef` — "nimani kengaytiramiz" (bizning deployment); `minReplicas`/`maxReplicas` — chegara; `metrics`da `type: Pods` — metrika har bir poddan olinadi va **o'rtachasi** hisoblanadi; `AverageValue: 1000` — o'rtacha shu qiymatdan oshsa HPA replikalarni ko'paytiradi. CPU bo'lmagan, custom metrikalar faqat `autoscaling/v2` API'da ishlaydi. `describe`dagi `<unknown>` xatosi savol sharti bo'yicha normal holat.

---

### 12-savol: Gateway API — trafikni 80/20 ga bo'lish

**Masala:** `web-route` nomli HTTPRoute sozlang: trafikning 80% `web-service`ga, 20% `web-service-v2`ga borsin. `web-gateway`, `web-service` va `web-service-v2` allaqachon mavjud.

**Yechim:** Avval mavjud resurslarni tekshiramiz:

```bash
kubectl get service          # web-service, web-service-v2 bor
kubectl get gateway          # web-gateway bor
```

Endi HTTPRoute (`question12.yaml`):

```yaml
apiVersion: gateway.networking.k8s.io/v1
kind: HTTPRoute
metadata:
  name: web-route
  namespace: default
spec:
  parentRefs:
  - name: web-gateway
    namespace: default
  rules:
  - matches:
    - path:
        type: PathPrefix
        value: /
    backendRefs:
    - name: web-service
      port: 80
      weight: 80
    - name: web-service-v2
      port: 80
      weight: 20
```

```bash
kubectl apply -f question12.yaml
```

**Tushuntirish:** HTTPRoute — Gateway API dunyosidagi "yo'l xaritasi": `parentRefs` uni qaysi darvozaga (gateway'ga) bog'lashni aytadi, `matches` qaysi so'rovlar tushishini belgilaydi (`/` prefiksi — hamma so'rov), `backendRefs`dagi `weight` esa trafikni foizlarga bo'ladi: 80 va 20. Bu — canary deployment'ning klassik usuli: yangi versiyaga avval ozgina trafik beriladi.

---

### 13-savol: Helm chart'ni tekshirish, o'rnatish va eskisini o'chirish

**Masala:** Klasterda Helm orqali o'rnatilgan `webpage-server-01` ilovasi bor. Yangi versiya chart'i `/root/new-version` katalogida. Chart'ni avval validatsiya qiling, so'ng o'rnating va eski versiyani o'chirib tashlang.

**Yechim:**

```bash
# 1) Chart'ni validatsiya qilamiz
helm lint /root/new-version
# ==> Linting /root/new-version
# 1 chart(s) linted, 0 chart(s) failed    <-- chart sog'lom

# 2) O'rnatamiz (savol aniq nom talab qilmagan — helm o'zi nom yaratsin)
helm install --generate-name /root/new-version
# NAME: new-version-17...

helm list
# Ikkala relizni ko'ramiz: eski webpage-server-01 va yangisi

# 3) Eski versiyani o'chiramiz
helm uninstall webpage-server-01
helm list
# Faqat yangi reliz qoldi
```

**Tushuntirish:** `helm lint` — chart'dagi sintaksis va tuzilish xatolarini o'rnatishdan **oldin** ushlab beradigan tekshiruv (`0 chart(s) failed` — hammasi joyida degani). `helm install`ga reliz nomini o'zingiz berishingiz yoki `--generate-name` bilan avtomatik yaratishingiz mumkin — savol aniq nom bermagan bo'lsa, ikkalasi ham to'g'ri. Ishlash tartibi muhim: avval yangisini o'rnatib, ishlaganiga ishonch hosil qilib, keyingina eskisini `helm uninstall` qilamiz.

---

### 14-savol: Pod CIDR tarmog'ini JSONPath bilan olish

**Masala:** Klasterning pod CIDR tarmog'ini aniqlab (bu CNI plaginini sozlashda kerak bo'ladi), natijani `/root/pod-cidr.txt` fayliga yozing.

**Yechim:** Avval qiymat qayerdaligini ko'rib olamiz:

```bash
kubectl get node controlplane -o yaml | more
# spec:
#   podCIDR: 172.17.0.0/24    <-- bizga kerakli qiymat
```

Endi uni qo'lda ko'chirmasdan, JSONPath bilan to'g'ridan-to'g'ri faylga yozamiz:

```bash
kubectl get node -o jsonpath='{.items[0].spec.podCIDR}' > /root/pod-cidr.txt

cat /root/pod-cidr.txt
# 172.17.0.0/24
```

**Tushuntirish:** `kubectl get node` ro'yxat qaytaradi, shuning uchun JSONPath `items[0]` bilan birinchi node'ni (control plane) oladi, so'ng `spec.podCIDR` maydoniga kirib boradi. Bu usul qo'lda nusxalashdan ishonchliroq — ortiqcha bo'shliq yoki xato belgisiz, aynan kerakli qiymat faylga tushadi.

---

## 💡 Umumiy xulosa jadvali

| # | Savol mavzusi | Asosiy buyruq/resurs | Esda tutish kerak |
|---|---------------|----------------------|-------------------|
| 1 | Tarmoq parametrlari (kubeadm) | `/etc/sysctl.d/k8s.conf` + `sysctl --system` | Faylga yozilmasa reboot'da yo'qoladi |
| 2 | RBAC + ServiceAccount | `create clusterrole/clusterrolebinding` | SA formati: `namespace:nom` |
| 3 | StorageClass | `provisioner`, `allowVolumeExpansion`, `volumeBindingMode` | Namunani docs'dan oling, ortiqchasini o'chiring |
| 4 | ConfigMap → env | `--from-literal`, `envFrom` + `configMapRef` | Hamma kalitlarni birdaniga olish uchun `envFrom` |
| 5 | PriorityClass | `priorityClassName` + `replace --force` | Eski `priority: 0` qatorini o'chirish shart |
| 6 | NetworkPolicy | `podSelector` + `ingress` qoidasi, port 80 | Yo'nalishni pod nuqtai nazaridan aniqlang |
| 7 | Taint/Toleration | `kubectl taint node`, `tolerations` bloki | Toleration taint bilan aynan mos bo'lsin |
| 8 | PV/PVC binding | accessModes moslash | PVC immutable — o'chirib qayta yarating |
| 9 | kubeconfig tuzatish | `--kubeconfig`, `netstat -tulnp` | apiserver standart porti — 6443 |
| 10 | Control plane trouble | `/etc/kubernetes/manifests/` | Deployment kengaymasa — controller-manager'ni tekshiring |
| 11 | HPA (custom metrika) | `autoscaling/v2`, `type: Pods`, `AverageValue` | Custom metrika faqat v2 API'da |
| 12 | Gateway API | HTTPRoute: `parentRefs` + `backendRefs` + `weight` | weight = trafik foizi (80/20) |
| 13 | Helm | `helm lint` → `install` → `uninstall` | Avval yangisi ishlasin, keyin eskisini o'chiring |
| 14 | JSONPath | `-o jsonpath='{.items[0].spec.podCIDR}'` | Qo'lda ko'chirmang — buyruq bilan yozing |

**Imtihonga tayyorgarlik bo'yicha uchta bosh saboq:**
1. **Hujjatlar — sizning eng yaqin do'stingiz.** Har mavzu docs'ning qayerida turishini oldindan o'rganing (StorageClass, NetworkPolicy, PriorityClass namunalari va h.k.).
2. **Nomlarni doim savoldan nusxalang** — validatsiya aynan shu nomni qidiradi.
3. **Troubleshooting'da tartib:** avval xatoni o'z ko'zingiz bilan ko'ring → xato matnini o'qing → sababni toping → keyin tuzating.

---
*Bu dars KodeKloud CKA kursining 324-videosi asosida tayyorlandi.*
