# Yechimlar — ishlab turgan Pod bilan ishlash

## 1-topshiriq · oson

```bash
kubectl exec sinov-nginx -- nginx -v
```

```text
nginx version: nginx/1.27.3
```

`--` belgisi muhim: undan keyingi hamma narsa **konteyner ichida** bajariladi,
`kubectl` uni o'ziga bayroq deb qabul qilmaydi.

## 2-topshiriq · o'rta

Birinchi terminalda:

```bash
kubectl port-forward pod/sinov-nginx 8080:80
```

Ikkinchi terminalda:

```bash
curl -s http://localhost:8080 | head -4
kubectl logs sinov-nginx --tail=3
```

Log'da so'rov ko'rinadi:

```text
127.0.0.1 - - [.....] "GET / HTTP/1.1" 200 615 "-" "curl/8.x" "-"
```

Diqqat: log'dagi mijoz IP'si `127.0.0.1` — chunki so'rov `port-forward`
tunneli orqali keldi, tashqi tarmoqdan emas.

## 3-topshiriq · qiyin

**Kutilgan javob:** xato beradi.

```bash
kubectl exec -it sinov-nginx -- /bin/bash
```

```text
OCI runtime exec failed: exec failed: unable to start container process:
exec: "/bin/bash": stat /bin/bash: no such file or directory: unknown
```

**Sabab:** `nginx:1.27-alpine` Alpine Linux asosida qurilgan. Alpine'da
`bash` o'rniga `busybox` ning yengil `sh` qobig'i bo'ladi — image hajmini
kichik saqlash uchun.

Ishlaydigan variant:

```bash
kubectl exec -it sinov-nginx -- /bin/sh
```

Qaysi qobiqlar borligini tekshirish:

```bash
kubectl exec sinov-nginx -- ls /bin/ | grep -E '^(sh|bash|ash)$'
```

> 💡 Universal usul: `kubectl exec -it <pod> -- sh` dan boshlang. `sh`
> deyarli har qanday Linux image'ida bor.

## Tozalash

```bash
bash tozalash.sh
```
