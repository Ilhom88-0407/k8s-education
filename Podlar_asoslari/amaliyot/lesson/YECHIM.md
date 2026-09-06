# Yechimlar — Pod asoslari

> Avval o'zingiz bajarib ko'ring. Bu yerga faqat tiqilib qolganingizda yoki
> tekshirish uchun qarang.

## 1-topshiriq · oson

`mashq-pod` nomli Pod yarating: image `nginx:1.27-alpine`, label `daraja=oson`.

```bash
kubectl run mashq-pod --image=nginx:1.27-alpine --labels=daraja=oson
```

YAML orqali:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: mashq-pod
  labels:
    daraja: oson
spec:
  containers:
    - name: nginx
      image: nginx:1.27-alpine
```

Tekshirish:

```bash
kubectl get pod mashq-pod --show-labels
```

## 2-topshiriq · o'rta

Pod'ning IP manzilini toping va boshqa Pod'dan unga `curl` bilan murojaat qiling.

```bash
# 1. IP manzilni olamiz
kubectl get pod mashq-pod -o jsonpath='{.status.podIP}{"\n"}'

# 2. Vaqtinchalik Pod ochib, o'sha IP ga so'rov yuboramiz
kubectl run sinov --rm -it --image=curlimages/curl:8.10.1 --restart=Never \
  -- curl -s http://<yuqoridagi-IP>
```

nginx'ning "Welcome to nginx!" sahifasi qaytadi.

**Nima uchun boshqa Pod'dan?** Pod IP'si klaster ichidagi manzil — sizning
kompyuteringizdan unga to'g'ridan-to'g'ri kirib bo'lmaydi.

## 3-topshiriq · qiyin

`02-ikki-konteynerli-pod.yaml` dagi Pod'ni qo'llang. `kuzatuvchi` konteyner
`yozuvchi` yozgan qatorlarni ko'ryaptimi? Nima uchun ular bir-birining faylini
ko'ra oladi?

```bash
kubectl apply -f 02-ikki-konteynerli-pod.yaml
kubectl logs sidecar-namuna -c kuzatuvchi -f
```

**Javob:** ikkala konteyner bitta `emptyDir` volume'ini `/umumiy` yo'liga
ulagan. `emptyDir` — Pod bilan birga yaratiladigan bo'sh papka; Pod ichidagi
har qanday konteyner uni `volumeMounts` orqali o'ziga ulab olishi mumkin.

⚠️ **Muhim:** Pod o'chirilsa, `emptyDir` ham yo'qoladi. Ma'lumot saqlanib
qolishi kerak bo'lsa, PersistentVolume ishlatiladi.

Tekshirish — ikkala konteyner ham bitta IP'da:

```bash
kubectl get pod sidecar-namuna -o jsonpath='{.status.podIP}{"\n"}'
kubectl exec sidecar-namuna -c yozuvchi -- wget -qO- localhost:80 || \
  echo "80-portda hech kim tinglamayapti — bu kutilgan natija"
```

## Tozalash

```bash
bash tozalash.sh
```
