# Yechimlar — Kubernetes Dashboard

## 1-topshiriq · oson

```bash
kubectl get deployments -A --no-headers | wc -l
```

Dashboard'da yuqoridagi `Workloads` kartochkasi shu sonni ko'rsatadi.
Agar farq bo'lsa, Dashboard'da namespace filtri qo'yilgan bo'lishi mumkin —
yuqoridagi ochiluvchi ro'yxatdan "All namespaces" ni tanlang.

## 2-topshiriq · o'rta

```bash
kubectl -n kubernetes-dashboard create token admin-user --duration=24h
```

Standart muddat — 1 soat. `--duration` maksimal qiymati apiserver'ning
`--service-account-max-token-expiration` bayrog'i bilan cheklanadi
(odatda 24 soat).

Token muddatini tekshirish (uchinchi tomon vositasisiz):

```bash
TOKEN=$(kubectl -n kubernetes-dashboard create token admin-user --duration=24h)
echo "$TOKEN" | cut -d. -f2 | base64 -d 2>/dev/null | python3 -c \
  'import sys,json,datetime; d=json.load(sys.stdin); print(datetime.datetime.fromtimestamp(d["exp"]))'
```

## 3-topshiriq · qiyin

**Kutilgan javob:** obyektlar ko'rinadi, lekin o'zgartirib bo'lmaydi.

```bash
kubectl delete clusterrolebinding admin-user
kubectl create clusterrolebinding dashboard-viewer \
  --clusterrole=view \
  --serviceaccount=kubernetes-dashboard:admin-user
```

Dashboard'da:

- ro'yxatlar va tafsilotlar ochiladi;
- "Delete", "Edit" va "Scale" tugmalari xato beradi;
- **Secret'lar umuman ko'rinmaydi** — `view` roli ularni o'z ichiga olmaydi.

Buyruq bilan tekshirish:

```bash
kubectl auth can-i delete pods \
  --as=system:serviceaccount:kubernetes-dashboard:admin-user
# no

kubectl auth can-i list pods \
  --as=system:serviceaccount:kubernetes-dashboard:admin-user
# yes

kubectl auth can-i list secrets \
  --as=system:serviceaccount:kubernetes-dashboard:admin-user
# no
```

**`kubectl auth can-i` — RBAC bilan ishlashning eng foydali buyrug'i.**
U klasterni o'zgartirmasdan huquqlarni tekshiradi.

Barcha huquqlarni ko'rish:

```bash
kubectl auth can-i --list \
  --as=system:serviceaccount:kubernetes-dashboard:admin-user
```

## Tayyor rollar

| ClusterRole | Nimaga ruxsat beradi |
|---|---|
| `view` | O'qish (Secret'lardan tashqari) |
| `edit` | O'qish va o'zgartirish (RBAC'dan tashqari) |
| `admin` | Namespace ichida to'liq huquq, RBAC ham |
| `cluster-admin` | Butun klasterda cheksiz huquq |

Har doim eng kam huquqdan boshlang va kerak bo'lgandagina kengaytiring.
