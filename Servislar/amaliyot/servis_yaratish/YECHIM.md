# Yechimlar — Servislar bo'limi

## servis_yaratish.md

### 1-topshiriq · oson

```bash
kubectl apply -f 01-deployment.yaml
kubectl apply -f 02-clusterip.yaml
kubectl get svc web-clusterip -o jsonpath='{.spec.clusterIP}{"\n"}'
```

### 2-topshiriq · o'rta

```bash
kubectl run t --rm -it --image=curlimages/curl:8.10.1 --restart=Never \
  -- curl -s http://web-clusterip | grep -o '<title>.*</title>'
```

```text
<title>Welcome to nginx!</title>
```

DNS nomi ishlaydi, chunki CoreDNS har Service uchun
`<nom>.<namespace>.svc.cluster.local` yozuvini yaratadi. Bir namespace
ichida qisqa nom yetarli.

### 3-topshiriq · qiyin

**Kutilgan javob:** `Endpoints` bo'sh qoladi.

```bash
kubectl patch svc web-clusterip -p '{"spec":{"selector":{"app":"yoq-bunday"}}}'
kubectl describe svc web-clusterip | grep -i endpoints
```

```text
Endpoints:  <none>
```

Service o'zi ishlab turadi, ClusterIP ham joyida — lekin unga so'rov
yuborsangiz ulanish rad etiladi, chunki yo'naltiradigan Pod yo'q.

**Bu Kubernetes'dagi eng ko'p uchraydigan nosozlik.** Service ishlamayotgan
bo'lsa, birinchi tekshiradigan narsa — `Endpoints`.

Tuzatish:

```bash
kubectl patch svc web-clusterip -p '{"spec":{"selector":{"app":"web"}}}'
kubectl get endpoints web-clusterip
```

## service_ClusterIP.md

### 3-topshiriq · qiyin

**Kutilgan javob:** ishlamaydi.

ClusterIP (`10.x.x.x`) — klasterning ichki Service tarmog'idagi manzil.
U sizning kompyuteringizning marshrutlash jadvalida yo'q, shuning uchun
brauzer unga yeta olmaydi.

Ko'rish uchun uchta yo'l:

```bash
# 1. port-forward — eng oson
kubectl port-forward service/web-mashq 8080:9090

# 2. turini NodePort ga o'zgartirish
kubectl patch svc web-mashq -p '{"spec":{"type":"NodePort"}}'

# 3. klaster ichidan sinash
kubectl run t --rm -it --image=curlimages/curl:8.10.1 --restart=Never \
  -- curl -s http://web-mashq:9090
```

## lesson30.md (NodePort)

### 3-topshiriq · qiyin

**Kutilgan javob:** xato beradi.

```text
The Service "ikkinchi" is invalid: spec.ports[0].nodePort:
Invalid value: 30080: provided port is already allocated
```

NodePort **butun klaster bo'ylab noyob**: bitta port raqamini ikki Service
egallay olmaydi. Node'da o'sha portni faqat bitta kube-proxy qoidasi
ushlab turishi mumkin.

Yechim: boshqa raqam bering yoki `nodePort` ni umuman yozmang — Kubernetes
bo'shini o'zi tanlaydi.

## lesson31.md (LoadBalancer)

### 3-topshiriq · qiyin

**Kutilgan javob:** NodePort **bor**.

```bash
kubectl get svc web-lb -o jsonpath='{.spec.ports[0].nodePort}{"\n"}'
```

Sababi: Service turlari bir-birining ustiga qo'yiladi.

```
LoadBalancer  =  NodePort  +  tashqi IP
NodePort      =  ClusterIP +  node porti
```

Shuning uchun LoadBalancer Service'da uchala kirish yo'li ham mavjud:
ClusterIP, NodePort va (bulut bo'lsa) tashqi IP.

Bu bare-metal klasterda juda foydali: `EXTERNAL-IP` doim `<pending>`
bo'lsa ham, NodePort orqali ilova ishlab turaveradi.

## Lesson32.md

### 3-topshiriq · qiyin

**Kutilgan javob:** Pod'lar **qoladi**.

```bash
kubectl delete deployment web --cascade=orphan
kubectl get pods -l app=web
```

Pod'lar joyida turadi, lekin ularning `ownerReferences` maydoni endi
hech kimga ishora qilmaydi — ya'ni ular **egasiz**. Endi bittasini
o'chirsangiz, hech kim yangisini yaratmaydi.

Tekshirish:

```bash
kubectl get pod <nom> -o jsonpath='{.metadata.ownerReferences}{"\n"}'
```

Bu bayroq amalda kamdan-kam kerak: masalan Deployment'ni boshqa nom bilan
qayta yaratmoqchi bo'lganda, ishlab turgan Pod'larni uzmaslik uchun.

## Tozalash

```bash
bash tozalash.sh
```
