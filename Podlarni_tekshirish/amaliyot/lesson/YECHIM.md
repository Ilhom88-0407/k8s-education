# Yechimlar — Pod holatini o'qish

## 1-topshiriq · oson

```bash
kubectl run buzuq --image=nginx:9.99-yoq
kubectl get pod buzuq
```

```text
NAME    READY   STATUS             RESTARTS   AGE
buzuq   0/1     ImagePullBackOff   0          40s
```

Sabab `describe` chiqishining eng oxirida:

```bash
kubectl describe pod buzuq | tail -8
```

```text
Warning  Failed   Failed to pull image "nginx:9.99-yoq": ... not found
Warning  Failed   Error: ErrImagePull
Normal   BackOff  Back-off pulling image "nginx:9.99-yoq"
```

**`ErrImagePull` va `ImagePullBackOff` farqi:** birinchisi — birinchi urinish
muvaffaqiyatsiz tugadi. Ikkinchisi — Kubernetes bir necha marta urinib
ko'rdi va endi urinishlar oralig'ini uzaytiryapti.

Odatdagi sabablar: image nomi yoki tegi xato, registry xususiy va
`imagePullSecrets` berilmagan, tarmoqqa chiqish yo'q.

Tozalash: `kubectl delete pod buzuq`

## 2-topshiriq · o'rta

```bash
IP=$(kubectl get pod my-nginx-pod -o jsonpath='{.status.podIP}')
echo "$IP"

kubectl run sinov --rm -it --image=curlimages/curl:8.10.1 --restart=Never \
  -- curl -s "http://$IP"
```

`<title>Welcome to nginx!</title>` qaytadi.

O'z kompyuteringizdan `curl http://$IP` **ishlamaydi** — Pod tarmog'i
(`10.244.0.0/16`) klaster ichidagi virtual tarmoq, sizning marshrutlash
jadvalingizda u yo'q.

## 3-topshiriq · qiyin

```bash
kubectl run yiqiluvchi --image=busybox:1.37 -- sh -c 'sleep 5; exit 1'
```

**Kutilgan javob:** konteyner har 5 soniyada yiqiladi, `RESTARTS` o'sib
boradi, `STATUS` esa `CrashLoopBackOff` ga o'tadi.

```bash
kubectl get pod yiqiluvchi -w
```

```text
NAME         READY   STATUS             RESTARTS      AGE
yiqiluvchi   1/1     Running            0             5s
yiqiluvchi   0/1     Error              0             10s
yiqiluvchi   1/1     Running            1 (3s ago)    13s
yiqiluvchi   0/1     CrashLoopBackOff   1 (5s ago)    18s
```

Sababni topish:

```bash
kubectl describe pod yiqiluvchi | grep -A5 'Last State'
```

```text
Last State:     Terminated
  Reason:       Error
  Exit Code:    1
```

**`CrashLoopBackOff` — bu holat emas, jazolash mexanizmi.** Kubernetes
qayta urinishlar oralig'ini 10s → 20s → 40s → ... → 5 daqiqagacha uzaytiradi,
shunda yiqiluvchi ilova klasterni yuklab yubormaydi.

Log'ni ko'rish (joriy konteyner hali ko'tarilmagan bo'lishi mumkin):

```bash
kubectl logs yiqiluvchi --previous
```

Tozalash: `kubectl delete pod yiqiluvchi`
