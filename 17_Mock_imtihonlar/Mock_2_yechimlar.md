# Dars 322 — Mock Exam 2: Yechimlar

> 🎯 **Bu imtihon haqida qisqacha:**
> - Bu — CKA kursidagi ikkinchi sinov imtihonining to'liq yechimlari darsi
> - Mavzular qamrovi juda keng: StorageClass, sidecar konteynerlar, Ingress, rolling update, CSR + RBAC, Service DNS, static pod, HPA, Gateway API, Helm va NetworkPolicy
> - Har bir savolda avvalo TO'G'RI klasterga o'tishni unutmang (`ssh cluster1-controlplane` kabi) — imtihonda eng ko'p yo'qotiladigan ball aynan shu e'tiborsizlikdan keladi
> - Ustoz deyarli har savolda kubernetes.io hujjatlaridan tayyor namunani olib, uni moslashtiradi — bu imtihonda vaqtni tejashning asosiy usuli

Oddiy o'xshatish: mock imtihon — haydovchilik imtihonidan oldingi mashq maydoni. Yo'l qoidalarini (buyruqlarni) bilish yetarli emas, ularni vaqt bosimi ostida, adashmasdan qo'llay olish kerak. Shu dars — o'sha mashq maydonining "instruktor bilan birga aylanib chiqish" qismi.

> 📝 **Eslatma:** Videoda ustoz 8-savoldan keyin to'g'ridan-to'g'ri "10-savol" deb davom etadi — 9-savol yechimi videoda alohida ko'rsatilmagan. Shuning uchun quyida savollar videodagi raqamlash bo'yicha berildi: 1–8, 10, 11, 12 (jami 11 ta yechim).

---

## 1-savol: Default StorageClass yaratish

**Shart:** `cluster1` control plane'da `local-sc` nomli StorageClass yarating va uni klasterning default StorageClass'i qilib belgilang (volume expansion yoqilgan, binding mode — `WaitForFirstConsumer`).

Avval kerakli klasterga o'tamiz, keyin hujjatlardan (kubernetes.io → "storage class" qidiruvi) namuna YAML olib, moslashtiramiz:

```bash
ssh cluster1-controlplane
vi local-sc.yaml
```

```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: local-sc
  annotations:
    storageclass.kubernetes.io/is-default-class: "true"
provisioner: rancher.io/local-path
allowVolumeExpansion: true
volumeBindingMode: WaitForFirstConsumer
```

```bash
kubectl apply -f local-sc.yaml
```

**Tushuntirish:** StorageClass'ni "default" qilishning yagona yo'li — `storageclass.kubernetes.io/is-default-class: "true"` annotatsiyasi. Savolda `reclaimPolicy` haqida hech narsa deyilmagan, shuning uchun namunadagi ortiqcha qatorlarni (reclaimPolicy, mountOptions va h.k.) o'chirib tashlaymiz — YAML qanchalik toza bo'lsa, xato ehtimoli shunchalik kam.

> ⚠️ **Tez-tez qilinadigan xato:** annotatsiyani unutish yoki qiymatni qo'shtirnoqsiz `true` deb yozish. Annotatsiya qiymati string bo'lishi kerak: `"true"`. Annotatsiyasiz StorageClass yaratiladi, lekin "default" bo'lmaydi — savol yarim bajarilgan hisoblanadi.

---

### 2-savol: Sidecar konteynerli logging Deployment

**Shart:** `logging-ns` namespace'ida `logging-deployment` nomli Deployment (1 replica) yarating: asosiy `app-container` (busybox) log faylga yozadi, sidecar `log-agent` (busybox) esa o'sha faylni `tail -f` qilib o'qib turadi.

Bu savolning "tuzog'i" shundaki, ikkala konteyner ham `/var/log/app/app.log` fayli bilan ishlaydi, lekin har bir konteynerning fayl tizimi ALOHIDA. Ularni bog'lash uchun umumiy volume kerak. Ma'lumot vaqtinchalik (scratch) bo'lgani uchun `emptyDir` yetarli:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: logging-deployment
  namespace: logging-ns
spec:
  replicas: 1
  selector:
    matchLabels:
      app: logger
  template:
    metadata:
      labels:
        app: logger
    spec:
      containers:
      - name: app-container
        image: busybox
        command: ["sh", "-c", "while true; do echo 'log entry' >> /var/log/app/app.log; sleep 5; done"]
        volumeMounts:
        - name: log-volume
          mountPath: /var/log/app
      - name: log-agent
        image: busybox
        command: ["sh", "-c", "tail -f /var/log/app/app.log"]
        volumeMounts:
        - name: log-volume
          mountPath: /var/log/app
      volumes:
      - name: log-volume
        emptyDir: {}
```

```bash
kubectl apply -f question2.yaml
kubectl get pod -n logging-ns
# Sidecar haqiqatan loglarni o'qiyaptimi — tekshiramiz:
kubectl logs <pod-nomi> -n logging-ns -c log-agent -f
```

**Tushuntirish:** `command` maydoni image'ning default buyrug'ini bekor qilib, o'zimiznikini ishga tushiradi. `emptyDir` volume ikkala konteynerda ham AYNAN bir xil yo'lga (`/var/log/app`) mount qilinadi — natijada bu ikkala konteyner uchun bitta umumiy papka bo'lib qoladi. `kubectl logs -c log-agent` chiqishida yozuvlar oqib kelayotgani — yechim to'g'ri ishlayotganining isboti.

> ⚠️ **Tez-tez qilinadigan xato:** volume va volumeMounts'siz yechim topshirish. Volumesiz `log-agent` konteyneri `/var/log/app/app.log` faylini KO'RMAYDI — chunki bu fayl faqat `app-container` ichida mavjud. Pod ichidagi konteynerlar fayl almashishi uchun har doim umumiy volume kerak.

---

### 3-savol: Ingress resursi yaratish

**Shart:** `ingress-ns` namespace'ida ishlab turgan `web-app` Deployment'i `webapp-svc` servisi orqali ochilgan. Xuddi shu namespace'da `web-app-ingress` nomli Ingress yarating: host `kodekloud-ingress.app`, path `/` (Prefix turi), trafik servisning 80-portiga yo'naltirilsin.

Avval mavjud resurslarni tekshirib olamiz (bu odat — ishlamayotgan narsaga Ingress qurishdan asraydi):

```bash
kubectl get deploy -n ingress-ns
kubectl get svc -n ingress-ns
# ingressClassName sifatida nimani yozishni bilish uchun:
kubectl get ingressclass
# Natija: nginx
```

Endi hujjatlardan Ingress namunasini olib, moslashtiramiz:

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: web-app-ingress
  namespace: ingress-ns
spec:
  ingressClassName: nginx
  rules:
  - host: kodekloud-ingress.app
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: webapp-svc
            port:
              number: 80
```

```bash
kubectl apply -f question3.yaml
# Tekshirish:
curl http://kodekloud-ingress.app/
```

**Tushuntirish:** `curl` natijasida nginx'ning standart sahifasi kelsa — Ingress qoidamiz trafikni to'g'ri yo'naltiryapti. Ingress'ni binoning resepshni deb tasavvur qiling: mehmon (so'rov) qaysi nom (host) va qaysi yo'lak (path) bilan kelganiga qarab, kerakli xonaga (Service) yo'naltiriladi.

> ⚠️ **Tez-tez qilinadigan xato:** hujjatlardagi namunada turgan `ingressClassName: nginx-example` qiymatini o'zgartirmasdan qoldirish. Har doim `kubectl get ingressclass` bilan klasteringizdagi REAL class nomini aniqlang — bu yerda u `nginx`.

---

### 4-savol: Deployment yaratish va rolling update

**Shart:** `nginx:1.16` image bilan 1 replicali `nginx-deploy` Deployment yarating, so'ng uni rolling update usulida `nginx:1.17` versiyaga ko'taring.

```bash
# Bazaviy YAML'ni imperativ buyruq bilan hosil qilamiz:
kubectl create deployment nginx-deploy --image=nginx:1.16 \
  --dry-run=client -o yaml > question4.yaml

kubectl apply -f question4.yaml
kubectl get deployment

# Hozirgi revision'ni ko'ramiz:
kubectl rollout history deployment nginx-deploy
kubectl rollout history deployment nginx-deploy --revision=1
# Natijada image: nginx:1.16 ekanini ko'ramiz

# Endi yangi versiyaga ko'taramiz:
kubectl set image deployment nginx-deploy nginx=nginx:1.17

# Tekshiramiz — endi 2 ta revision bor:
kubectl rollout history deployment nginx-deploy
kubectl rollout history deployment nginx-deploy --revision=2
# Natijada image: nginx:1.17
```

**Tushuntirish:** Deployment'ning yangilash strategiyasi `spec.strategy.type` maydonida turadi. `RollingUpdate` — bu DEFAULT strategiya, ya'ni YAML'da alohida yozmasak ham, Kubernetes o'zi bosqichma-bosqich (eski podlarni birdan o'chirmasdan) yangilaydi. Shuning uchun bu savolda strategiyani qo'lda yozish shart emas — `kubectl set image` buyrug'ining o'zi rolling update'ni amalga oshiradi.

> ⚠️ **Tez-tez qilinadigan xato:** `kubectl set image` sintaksisida konteyner nomini tushirib qoldirish. To'g'ri format: `kubectl set image deployment <deploy-nomi> <konteyner-nomi>=<yangi-image>`. Bu yerda konteyner nomi `nginx` (create deployment uni image nomidan avtomatik olgan).

---

### 5-savol: Yangi foydalanuvchi (CSR + Role + RoleBinding)

**Shart:** `john` nomli foydalanuvchiga klasterga kirish huquqini bering: `john-developer` nomli CSR obyekti yarating va tasdiqlang, so'ng `development` namespace'ida podlar ustida `create, list, get, update, delete` amallariga ruxsat beruvchi `developer` Role va uni john'ga bog'laydigan RoleBinding yarating. John'ning private key va sertifikat so'rovi `/root/CA/` papkasida tayyor turibdi.

**1-qadam — mavjud fayllarni ko'rib olamiz:**

```bash
cat /root/CA/john.key   # private key
cat /root/CA/john.csr   # sertifikat so'rovi (CSR fayli)
```

**2-qadam — CSR faylini base64 ga o'giramiz** (CSR obyektining `request` maydoni faqat base64 qabul qiladi, va bir qatorda bo'lishi kerak):

```bash
cat /root/CA/john.csr | base64 | tr -d "\n"
```

**3-qadam — CertificateSigningRequest obyektini yaratamiz** (hujjatlarda "Issue a Certificate for a Kubernetes API Client Using A CertificateSigningRequest" sahifasidan namuna bor):

```yaml
apiVersion: certificates.k8s.io/v1
kind: CertificateSigningRequest
metadata:
  name: john-developer
spec:
  signerName: kubernetes.io/kube-apiserver-client
  request: <base64-kodlangan-csr-bir-qatorda>
  usages:
  - digital signature
  - key encipherment
  - client auth
```

```bash
kubectl apply -f question5.yaml
kubectl get csr
# john-developer holati: Pending

# Tasdiqlaymiz:
kubectl certificate approve john-developer
kubectl get csr
# Endi holati: Approved,Issued

# Tayyor sertifikatni ko'rish (status.certificate maydonida, base64 holda):
kubectl get csr john-developer -o yaml
```

**4-qadam — Role va RoleBinding** (ikkala obyektni bitta faylda `---` bilan ajratib yozish mumkin):

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: developer
  namespace: development
rules:
- apiGroups: [""]
  resources: ["pods"]
  verbs: ["create", "list", "get", "update", "delete"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: john-developer-rolebinding
  namespace: development
subjects:
- kind: User
  name: john
  apiGroup: rbac.authorization.k8s.io
roleRef:
  kind: Role
  name: developer
  apiGroup: rbac.authorization.k8s.io
```

```bash
kubectl apply -f question5-rbac.yaml

# Tekshirish — john nomidan huquqlarni sinaymiz:
kubectl auth can-i create pods --as=john -n development
# yes
kubectl auth can-i create pods --as=john -n default
# no  (boshqa namespace'da huquq yo'q — to'g'ri!)
```

**Tushuntirish:** Bu savol autentifikatsiya (sen kimsan?) va avtorizatsiya (senga nima mumkin?) ikkalasini birlashtiradi. CSR obyekti tasdiqlangach, Kubernetes john uchun sertifikat chiqaradi — bu uning "pasporti". Role + RoleBinding esa "ruxsatnomasi". Pod'lar core API guruhiga kirgani uchun `apiGroups: [""]` — bo'sh qoladi.

> ⚠️ **Tez-tez qilinadigan xato:** videoda ustozning o'zi ham shu xatoga yo'l qo'ydi — RoleBinding'da `subject` deb yozib, `unknown field "subject"` xatosini oldi. To'g'risi — ko'plikda: `subjects`. Va yana: `--as=john` bilan tekshirishni hech qachon o'tkazib yubormang — bu 10 soniyada yechim to'g'riligini isbotlaydi.

---

### 6-savol: Pod, ClusterIP Service va DNS tekshiruvi

**Shart:** `nginx-resolver` nomli pod (image: nginx) yarating va uni `nginx-resolver-service` servisi bilan KLASTER ICHIDA oching. So'ng `busybox:1.28` image yordamida servis va pod DNS nomlarini nslookup qilib, natijalarni `/root/CKA/nginx.svc` va `/root/CKA/nginx.pod` fayllariga yozing.

```bash
# Pod yaratamiz:
kubectl run nginx-resolver --image=nginx

# Servis bilan ochamiz. "Internally" degani — ClusterIP:
kubectl expose pod nginx-resolver --name=nginx-resolver-service \
  --port=80 --target-port=80 --type=ClusterIP

# Tekshiramiz:
kubectl get svc
kubectl describe svc nginx-resolver-service
# Endpoints qatorida bitta pod IP ko'rinadi
kubectl get pod -o wide
# nginx-resolver IP: 172.17.1.18 (misol)
```

**Servis DNS'ini tekshirish** — vaqtinchalik pod ishga tushirib, bitta buyruq bajaramiz (`--rm` tugagach o'zi o'chadi):

```bash
kubectl run test-nslookup --image=busybox:1.28 --rm -it --restart=Never \
  -- nslookup nginx-resolver-service > /root/CKA/nginx.svc
```

**Pod DNS'ini tekshirish** — pod IP'sidagi nuqtalar chiziqchaga almashadi va oxiriga `.default.pod` qo'shiladi:

```bash
kubectl run test-nslookup --image=busybox:1.28 --rm -it --restart=Never \
  -- nslookup 172-17-1-18.default.pod > /root/CKA/nginx.pod
```

**Tushuntirish:** DNS — klasterning telefon kontaktlar kitobi: nom aytasiz, IP oladi. Servislar `<servis-nomi>.<namespace>.svc.cluster.local` shaklida, podlar esa `<ip-chiziqcha-bilan>.<namespace>.pod` shaklida yoziladi. `busybox:1.28` versiyasi ataylab tanlangan — yangi busybox versiyalarida nslookup xatolik berishi mumkin.

> ⚠️ **Tez-tez qilinadigan xato:** savol matnidagi "expose it internally" so'ziga e'tibor bermay NodePort yaratish. "Internally" (faqat klaster ichidan) — bu ClusterIP degani. NodePort/LoadBalancer — tashqi dunyo uchun. Imtihonda savol matnidagi har bir so'z ataylab tanlangan bo'ladi.

---

### 7-savol: Static pod yaratish

**Shart:** `cluster1-node01` nodesida `nginx-critical` nomli static pod (image: nginx) yarating — u xatolik yuz berganda avtomatik qayta ishga tushishi kerak. Manifest yo'li: `/etc/kubernetes/manifests`.

```bash
# Control plane'da pod YAML'ini tayyorlab olamiz:
kubectl run nginx-critical --image=nginx \
  --dry-run=client -o yaml > static.yaml
cat static.yaml   # mazmunini nusxalab olamiz

# Worker nodega o'tamiz:
ssh cluster1-node01

# Manifest papkasiga faylni joylashtiramiz:
vi /etc/kubernetes/manifests/static.yaml
# (nusxalangan YAML'ni shu yerga qo'yamiz va saqlaymiz)

# Nodedan chiqib, control plane'dan tekshiramiz:
exit
kubectl get pod -o wide
# NAME                            ...   NODE
# nginx-critical-cluster1-node01  ...   cluster1-node01
```

**Tushuntirish:** Static pod — API server emas, to'g'ridan-to'g'ri o'sha nodedagi kubelet boshqaradigan pod. Kubelet `/etc/kubernetes/manifests` papkasini doim kuzatib turadi: fayl paydo bo'lsa — pod yaratadi, pod o'lsa — qayta tiriltiradi (savoldagi "avtomatik qayta ishga tushsin" talabi shu bilan o'z-o'zidan bajariladi). Static pod nomiga node nomi avtomatik qo'shiladi: `nginx-critical-cluster1-node01` — bu uni oddiy poddan ajratib turadigan belgi.

> ⚠️ **Tez-tez qilinadigan xato:** manifest faylini control plane'da qoldirish. Savol qaysi nodeda static pod so'ragan bo'lsa, fayl AYNAN O'SHA nodening `/etc/kubernetes/manifests` papkasida turishi shart — kubelet faqat o'z nodesidagi papkani o'qiydi.

---

### 8-savol: HorizontalPodAutoscaler (memory bo'yicha)

**Shart:** `backend` namespace'idagi `backend-deployment` uchun `backend-hpa` nomli HPA yarating: o'rtacha xotira ishlatilishi 65% da ushlab turilsin, minimal 3, maksimal 15 replica. `/root/web-app-hpa.yaml` faylida bazaviy konfiguratsiya berilgan — uni to'ldiramiz.

```bash
vi /root/web-app-hpa.yaml
```

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: backend-hpa
  namespace: backend
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: backend-deployment
  minReplicas: 3
  maxReplicas: 15
  metrics:
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 65
```

```bash
kubectl apply -f /root/web-app-hpa.yaml

# Tekshiramiz:
kubectl describe hpa backend-hpa -n backend
# Min replicas: 3, Max replicas: 15
# Metrics: resource memory ... 65%
```

**Tushuntirish:** HPA — avtomatik "smenali ishchi yollovchi": yuk oshsa podlar sonini ko'paytiradi, kamaysa qisqartiradi. Odatda misollar CPU bo'yicha bo'ladi, bu savolda esa MEMORY so'ralgan — `metrics` bo'limida `name: memory` va `target.type: Utilization`, `averageUtilization: 65` yozamiz. `scaleTargetRef` — qaysi Deployment'ni boshqarishini ko'rsatadi.

> ⚠️ **Tez-tez qilinadigan xato:** `averageUtilization: 65` o'rniga `65%` deb yozish (bu maydon son qabul qiladi, foiz belgisisiz), yoki odatdagi CPU misolini ko'chirib, `name: cpu` ni memory'ga almashtirishni unutish.

---

### 10-savol: Gateway'ni HTTPS ga o'tkazish

**Shart:** `cka5673` namespace'idagi mavjud `web-gateway` ni `kodekloud.com` uchun 443-portda HTTPS trafik qabul qiladigan qilib o'zgartiring. TLS sertifikat `kodekloud-tls` nomli Secret'da saqlangan. (Videodagi raqamlash bo'yicha — 10-savol.)

```bash
ssh cluster1-controlplane

# Mavjud gateway'ni ko'ramiz va YAML'ga chiqarib olamiz:
kubectl get gateway -n cka5673
kubectl get gateway -n cka5673 -o yaml > gateway.yaml

# Secret joyida ekanini tekshiramiz:
kubectl get secret -n cka5673
# kodekloud-tls bor — davom etamiz
vi gateway.yaml
```

Mavjud listener 80-portda HTTP edi. Uni quyidagicha o'zgartiramiz (spec'ning qolgan qismi, jumladan `gatewayClassName`, o'z holicha qoladi):

```yaml
spec:
  gatewayClassName: <mavjud-qiymat-o'zgarmaydi>
  listeners:
  - name: https
    port: 443
    protocol: HTTPS
    hostname: kodekloud.com
    tls:
      certificateRefs:
      - name: kodekloud-tls
```

```bash
kubectl apply -f gateway.yaml
```

**Tushuntirish:** Gateway API'da har bir `listener` — "qaysi eshikdan, qanday protokolda, qaysi hostname uchun trafik kiradi" degan qoida. HTTPS uchun uchta narsa o'zgaradi: `port: 443`, `protocol: HTTPS` va `tls.certificateRefs` orqali sertifikat turgan Secret'ga havola. Gateway o'sha Secret'dan sertifikat va kalitni olib, TLS'ni o'zi uzadi.

> ⚠️ **Tez-tez qilinadigan xato:** faqat portni 443 ga o'zgartirib, `protocol` ni HTTP'ligicha qoldirish yoki `tls` bo'limini umuman yozmaslik. HTTPS listener uchun uchchala element (port + protocol + tls.certificateRefs) birga bo'lishi shart.

---

### 11-savol: Zaif image'li Helm relizini topib o'chirish

**Shart:** Klasterga turli namespace'larga bir nechta Helm chartlari o'rnatib yuborilgan. Ulardan biri zaif (vulnerable) `kodekloud/webapp-color:v1` image'ini ishlatadi. O'sha relizni toping va uninstall qiling.

```bash
# Barcha namespace'lardagi relizlarni ro'yxatlaymiz:
helm list -A
# 4 ta reliz chiqadi

# Har bir relizning yakuniy manifestini tekshirib, zaif image'ni qidiramiz:
helm get manifest <reliz-nomi> -n <namespace> | grep "webapp-color:v1"
# Qaysi relizda shu qator chiqsa — o'sha bizga kerakli "aybdor"

# Topilgan relizni o'chiramiz:
helm uninstall <reliz-nomi> -n <namespace>
```

**Tushuntirish:** `helm list -A` — o'rnatilgan barcha relizlar ro'yxati (`-A` = hamma namespace). `helm get manifest` esa reliz klasterga qanday Kubernetes obyektlarini yaratganini — yakuniy, render qilingan YAML'ni ko'rsatadi. Uni `grep` bilan filtrlasak, qidirayotgan image qaysi relizda ekani darrov ma'lum bo'ladi. Relizni `helm uninstall` bilan olib tashlash — u yaratgan barcha resurslarni birga o'chiradi.

> ⚠️ **Tez-tez qilinadigan xato:** `helm uninstall` da `-n <namespace>` ni unutish. Reliz qaysi namespace'da o'rnatilgan bo'lsa, o'chirishda ham aynan shu namespace ko'rsatilishi kerak — aks holda "release not found" xatosi keladi.

---

### 12-savol: Eng cheklovchi NetworkPolicy'ni tanlash

**Shart:** `frontend` namespace'idagi ilovalardan `backend` namespace'idagi ilovalarga trafik RUXSAT etilsin, lekin `databases` namespace'idan trafik KELMASIN. `/root` papkasida 3 ta tayyor policy fayli bor — talabga javob beradigan ENG CHEKLOVCHISINI tanlab qo'llang (mavjud policylarni o'chirmang).

```bash
# Uchala faylni ham o'qib chiqamiz:
cat /root/net-pol-1.yaml
cat /root/net-pol-2.yaml
cat /root/net-pol-3.yaml

# Namespace labellarini bilib olamiz — selectorlar shunga qarab ishlaydi:
kubectl get namespace --show-labels
# frontend namespace'ida: name=frontend
# "databases" nomli alohida label yoki mos namespace holatini ham shu yerdan ko'ramiz
```

Uchala nomzodni tahlil qilamiz:

| Policy | Nima qiladi | Xulosa |
|---|---|---|
| net-pol-1 | `backend` podlariga, `access: allowed` labelli namespace'lardan ruxsat beradi | Hech bir namespace'da bunday label yo'q — frontend'dan trafik ham o'tmaydi. Talabni bajarmaydi ❌ |
| net-pol-2 | `frontend` HAM `databases` namespace'laridan ruxsat beradi | Databases'dan trafik o'tadi — bu aynan taqiqlanishi kerak edi ❌ |
| net-pol-3 | Faqat `name: frontend` labelli namespace'dan ruxsat beradi | Frontend o'tadi, boshqa hamma (jumladan databases) bloklanadi ✅ |

```bash
kubectl apply -f /root/net-pol-3.yaml
```

**Tushuntirish:** NetworkPolicy'ning ingress qoidalari "oq ro'yxat" (whitelist) tamoyilida ishlaydi: policy podga qo'llangach, faqat ro'yxatda ko'rsatilgan manbalardan trafik o'tadi, qolgan hammasi avtomatik bloklanadi. Shuning uchun 3-policy'da databases'ni alohida taqiqlash shart emas — u ro'yxatda yo'qligi bilanoq bloklangan. Bu ham "eng cheklovchi" varianti: kerakli minimumdan boshqa hech narsaga ruxsat bermaydi.

> ⚠️ **Tez-tez qilinadigan xato:** 2-policy'ni tanlash — u ham "frontend'dan ruxsat beradi", lekin qo'shimcha ravishda databases'ga ham eshik ochib qo'yadi. Savol "eng cheklovchi" (most restrictive) variantni so'raganda, har bir qo'shimcha ruxsat — noto'g'ri javob belgisi.

---

## 💡 Umumiy xulosa jadvali

| Savol | Mavzu | Kalit buyruq/tushuncha | Asosiy tuzoq |
|---|---|---|---|
| 1 | Default StorageClass | `is-default-class: "true"` annotatsiyasi | Annotatsiyani unutish |
| 2 | Sidecar + umumiy log | `emptyDir` + ikkala konteynerda bir xil `mountPath` | Volumesiz sidecar faylni ko'rmaydi |
| 3 | Ingress | `kubectl get ingressclass` → to'g'ri class nomi | Namunadagi `nginx-example`ni qoldirish |
| 4 | Rolling update | `kubectl set image deployment <d> <c>=<image>` | RollingUpdate default — qo'lda yozish shart emas |
| 5 | CSR + RBAC | `base64 \| tr -d "\n"`, `kubectl certificate approve`, `auth can-i --as` | `subject` emas — `subjects` |
| 6 | ClusterIP + DNS | `kubectl expose`, `nslookup` (busybox:1.28) | "internally" = ClusterIP, NodePort emas |
| 7 | Static pod | Fayl → o'sha nodedagi `/etc/kubernetes/manifests` | Faylni control plane'da qoldirish |
| 8 | HPA (memory) | `metrics` → `resource: memory`, `averageUtilization: 65` | CPU namunasini moslamay ko'chirish |
| 10 | Gateway HTTPS | `port: 443` + `protocol: HTTPS` + `tls.certificateRefs` | Uchtadan bittasini unutish |
| 11 | Helm | `helm list -A`, `helm get manifest \| grep` | Uninstall'da `-n` ni unutish |
| 12 | NetworkPolicy | Ingress = oq ro'yxat; eng cheklovchisini tanlash | Ortiqcha ruxsatli policy'ni tanlash |

## 📌 CKA imtihon uchun maslahat

- **Klasterni tekshiring:** har savol boshida so'ralgan klasterga SSH qiling — noto'g'ri klasterda bajarilgan mukammal yechim 0 ball.
- **Hujjatlardan namuna oling:** YAML'ni noldan yozmang — kubernetes.io'dan namunani ko'chirib, moslang. Ustoz shu usul bilan har savolda 1-2 daqiqa tejaydi.
- **Har yechimni tekshirib qo'ying:** `kubectl get/describe`, `kubectl logs`, `curl`, `auth can-i` — 15-20 soniyalik tekshiruv yo'qotilgan balldan arzon.
- **Savol so'zlariga sinchkov bo'ling:** "internally", "most restrictive", "default" kabi so'zlar — javobning yo'nalishini belgilaydigan maxfiy kalitlar.

## 📖 Asosiy atamalar

| Atama | Oddiy tushuntirish |
|---|---|
| StorageClass | Disk (volume) qanday va qayerdan ajratilishini belgilovchi "tarif rejasi" |
| Sidecar container | Asosiy konteynerga yordamchi bo'lib, u bilan bitta podda ishlaydigan qo'shimcha konteyner |
| emptyDir | Pod yashab turganda mavjud bo'ladigan vaqtinchalik umumiy papka |
| CSR (CertificateSigningRequest) | Yangi foydalanuvchi sertifikatini imzolash uchun klasterga beriladigan ariza |
| Static pod | API serversiz, to'g'ridan-to'g'ri kubelet boshqaradigan pod |
| HPA | Yukka qarab pod sonini avtomatik oshirib-kamaytiruvchi mexanizm |
| Gateway API | Ingress'ning zamonaviy avlodi — trafik kirish qoidalarini listener'lar orqali boshqaradi |
| Helm release | Helm chart'ning klasterga o'rnatilgan bitta nusxasi |
| NetworkPolicy | Podlar orasidagi tarmoq trafigiga ruxsat/taqiq qo'yuvchi "xavfsizlik devori" qoidasi |

## 🔗 Manbalar

- [Storage Classes](https://kubernetes.io/docs/concepts/storage/storage-classes/)
- [Sidecar Containers va umumiy volume](https://kubernetes.io/docs/concepts/workloads/pods/sidecar-containers/)
- [Ingress](https://kubernetes.io/docs/concepts/services-networking/ingress/)
- [Deployment rolling update](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/#updating-a-deployment)
- [CertificateSigningRequests](https://kubernetes.io/docs/reference/access-authn-authz/certificate-signing-requests/)
- [RBAC (Role va RoleBinding)](https://kubernetes.io/docs/reference/access-authn-authz/rbac/)
- [DNS for Services and Pods](https://kubernetes.io/docs/concepts/services-networking/dns-pod-service/)
- [Static Pods](https://kubernetes.io/docs/tasks/configure-pod-container/static-pod/)
- [HorizontalPodAutoscaler](https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/)
- [Gateway API](https://kubernetes.io/docs/concepts/services-networking/gateway/)
- [Helm hujjatlari](https://helm.sh/docs/)
- [Network Policies](https://kubernetes.io/docs/concepts/services-networking/network-policies/)

---
*Bu dars KodeKloud CKA kursining 322-videosi asosida tayyorlandi.*
