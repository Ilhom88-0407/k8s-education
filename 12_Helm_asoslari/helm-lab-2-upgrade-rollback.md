# Helm Lab 2 — Upgrade va Rollback

> 🎯 **Bu laboratoriyada nimani mashq qilamiz:**
> - Release'ni yangilash va revision tarixini kuzatish
> - `helm rollback` bilan oldingi holatga qaytish
> - `helm history` chiqishini o'qish

Helm release'larni yangilash (upgrade), tarixini ko'rish (history) va orqaga qaytarish (rollback) bo'yicha lab savollari, javoblari va CLI buyruqlar.

---

## 1. Nechta nginx release bor?

**Savol:** How many releases of `nginx` can you see in the cluster now?

```bash
helm list -A
```

Chiqish:
```
NAME          NAMESPACE  REVISION  STATUS    CHART         APP VERSION
dazzling-web  default    3         deployed  nginx-12.0.4  1.22.0
```

**Javob:** `1` (dazzling-web)

---

## 2. Bitnami repozitoriysini qo'shish

**Savol:** Add `bitnami` helm chart repository to the cluster.
URL: `https://charts.bitnami.com/bitnami`

```bash
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo list
```

---

## 3. Nechta nginx revision bor?

**Savol:** How many revisions of `nginx` exists in the cluster?

```bash
helm history dazzling-web
```

Chiqish:
```
REVISION  UPDATED                   STATUS      CHART         APP VERSION  DESCRIPTION
1         Thu Aug 27 11:47:37 2026  superseded  nginx-12.0.4  1.22.0       Install complete
2         Thu Aug 27 11:47:40 2026  superseded  nginx-12.0.5  1.22.0       Upgrade complete
3         Thu Aug 27 11:47:42 2026  deployed    nginx-12.0.4  1.22.0       Upgrade complete
```

**Javob:** `3`

> `helm list` dagi REVISION ustuni ham buni ko'rsatadi.

---

## 4. Hozir ishlayotgan nginx versiyasi

**Savol:** Which version of `nginx` is currently running in the cluster?

**Variantlar:** 1.21.6 / 1.22.0 / 1.19.4 / 1.20.6

**Javob:** `1.22.0` (APP VERSION ustunidan)

---

## 5. nginx'ni yangi versiyaga upgrade qilish

**Savol:** The DevOps team has decided to upgrade the `nginx` version to `1.27.x` and use the Helm chart version `18.3.6` from the Bitnami repository.

```bash
helm upgrade dazzling-web bitnami/nginx --version 18.3.6
```

Tekshirish:
```bash
helm list
```

Chiqish:
```
NAME          NAMESPACE  REVISION  STATUS    CHART         APP VERSION
dazzling-web  default    4         deployed  nginx-18.3.6  1.27.4
```

> `--version` — chart versiyasini belgilaydi (app versiyasini emas).

---

## 6. Upgrade qilingan versiya

**Savol:** To which version is the `nginx` currently upgraded?

**Variantlar:** 1.21.2 / 1.27.4 / 1.21.0 / 1.19.10

**Javob:** `1.27.4`

---

## 7. Oldingi versiyaga rollback qilish

**Savol:** Oops!.. There seems to be a minor issue in the website and the DevOps Team is asked to rollback the nginx to previous version!

```bash
helm rollback dazzling-web 3
```

> Revision ko'rsatilmasa (`helm rollback dazzling-web`) — avtomatik bitta oldingi revisionga qaytaradi.

Tekshirish:
```bash
helm history dazzling-web
```

Chiqish:
```
REVISION  STATUS      CHART         APP VERSION  DESCRIPTION
1         superseded  nginx-12.0.4  1.22.0       Install complete
2         superseded  nginx-12.0.5  1.22.0       Upgrade complete
3         superseded  nginx-12.0.4  1.22.0       Upgrade complete
4         superseded  nginx-18.3.6  1.27.4       Upgrade complete
5         deployed    nginx-12.0.4  1.22.0       Rollback to 3
```

> Rollback yangi revision (5) yaratadi — eski revisionlar o'chirilmaydi.

---

## Foydali buyruqlar xulosasi

| Buyruq | Vazifa |
|---|---|
| `helm list -A` | Barcha namespace'lardagi release'lar |
| `helm history <release>` | Release revisionlari tarixi |
| `helm upgrade <release> <repo>/<chart> --version <v>` | Belgilangan chart versiyasiga upgrade |
| `helm upgrade <release> <repo>/<chart>` | Eng so'nggi chart versiyasiga upgrade |
| `helm rollback <release> <revision>` | Ko'rsatilgan revisionga qaytarish |
| `helm rollback <release>` | Bitta oldingi revisionga qaytarish |
| `helm search repo <chart> --versions` | Chart'ning barcha versiyalarini ko'rish |
| `helm status <release>` | Release holati |

## 🔗 Manbalar

- [Helm — Upgrade and Rollback](https://helm.sh/docs/intro/using_helm/#helm-upgrade-and-helm-rollback-upgrading-a-release-and-recovering-on-failure)
- [helm rollback](https://helm.sh/docs/helm/helm_rollback/)
- [helm history](https://helm.sh/docs/helm/helm_history/)

---
⬅️ [Bo'lim indeksi](README.md)
