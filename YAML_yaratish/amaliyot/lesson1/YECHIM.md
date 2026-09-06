# Yechimlar — YAML manifestlar

## 1-topshiriq · oson

`01-deployment.yaml` da:

```yaml
spec:
  replicas: 3
```

```bash
kubectl apply -f 01-deployment.yaml
kubectl get deployment k8s-web-hello -o jsonpath='{.spec.replicas}{"\n"}'
```

## 2-topshiriq · o'rta

`livenessProbe` konteyner **tirikligini** tekshiradi. Javob bermasa,
kubelet konteynerni qayta ishga tushiradi.

```yaml
containers:
  - name: k8s-web-hello
    image: mrpocker88/k8s-web-hello:1.0.2
    ports:
      - containerPort: 3000
    livenessProbe:
      httpGet:
        path: /
        port: 3000
      initialDelaySeconds: 10   # ilova ko'tarilishiga vaqt beramiz
      periodSeconds: 10         # har 10 soniyada tekshiramiz
      failureThreshold: 3       # 3 marta muvaffaqiyatsiz -> qayta ishga tushirish
```

```bash
kubectl apply -f 01-deployment.yaml
kubectl describe deployment k8s-web-hello | grep -i liveness
```

**`livenessProbe` va `readinessProbe` farqi:**

| Probe | Muvaffaqiyatsiz bo'lsa |
|---|---|
| `livenessProbe` | Konteyner **qayta ishga tushiriladi** |
| `readinessProbe` | Pod Service ro'yxatidan **chiqariladi**, lekin ishlab turadi |

`initialDelaySeconds` ni juda kichik qo'ymang — aks holda sekin
ko'tariladigan ilova cheksiz qayta ishga tushaveradi.

## 3-topshiriq · qiyin

**Kutilgan javob:** `kubectl apply` manifestni rad etadi.

```yaml
spec:
  selector:
    matchLabels:
      app: boshqa-nom          # ← farqli
  template:
    metadata:
      labels:
        app: k8s-web-hello     # ← farqli
```

```text
The Deployment "k8s-web-hello" is invalid: spec.template.metadata.labels:
Invalid value: map[string]string{"app":"k8s-web-hello"}:
`selector` does not match template `labels`
```

**Nima uchun Kubernetes buni taqiqlaydi:** `selector` Deployment "o'z"
Pod'larini qaysi label bo'yicha topishini belgilaydi, `template.labels`
esa yangi Pod'larga qanday label qo'yilishini. Ular mos kelmasa, Deployment
o'zi yaratgan Pod'larni topa olmaydi — cheksiz yangi Pod yaratib turardi.

Bu tekshiruv `apply` bosqichidayoq amalga oshadi, shuning uchun bunday
manifest klasterga umuman tushmaydi.

## Tozalash

```bash
bash tozalash.sh
```
