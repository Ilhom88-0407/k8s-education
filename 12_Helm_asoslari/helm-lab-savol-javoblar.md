# Helm Lab — Savollar va Javoblar

Kubernetes klasterida Helm bilan ishlash bo'yicha lab savollari, javoblari va ishlatilgan CLI buyruqlar.

---

## 1. Helm paketi nima deb ataladi?

**Savol:** The helm package that contains all of the resource definitions necessary to run an application, tool, or service inside of a Kubernetes cluster is known as a ...

**Variantlar:** map / list / chart / brew

**Javob:** `chart`

> Chart — Kubernetes'da ilovani ishga tushirish uchun kerakli barcha resurs ta'riflarini (Deployment, Service, ConfigMap va h.k.) o'z ichiga olgan Helm paketi.

---

## 2. Bitta chart'ni bir klasterga bir necha marta o'rnatib bo'lmaydi?

**Savol:** We cannot install the same chart multiple times on the same Kubernetes Cluster.

**Javob:** `False`

> Bitta chart'ni bir necha marta o'rnatish mumkin — har bir o'rnatish alohida **release** bo'ladi va o'z nomi bilan ajratiladi:
> ```bash
> helm install app1 bitnami/nginx
> helm install app2 bitnami/nginx
> ```

---

## 3. Artifact Hub'dan chart qidirish buyrug'i

**Savol:** Which command is used to search for a `wordpress` helm chart package from the Artifact Hub?

**Javob:** `helm search hub wordpress`

```bash
helm search hub wordpress
```

> `helm search hub` — Artifact Hub'dan qidiradi.
> `helm search repo` — lokal qo'shilgan repolardan qidiradi.

---

## 4. Consul chart'ining APP VERSION'i

**Savol:** Search for a `consul` helm chart package from the Artifact Hub and identify the APP VERSION for the Official HashiCorp Consul Chart.

**Variantlar:** 2.0.3 / 1.10.2 / 0.36.0 / 1.9.0

```bash
helm search hub consul
```

**Javob:** `1.10.2`

> Diqqat: `0.36.0` — bu CHART VERSION, `1.10.2` — APP VERSION. Ularni adashtirmang.

---

## 5. Bitnami repozitoriysini qo'shish

**Savol:** Add `bitnami` helm chart repository in the controlplane node.
URL: `https://charts.bitnami.com/bitnami`

```bash
helm repo add bitnami https://charts.bitnami.com/bitnami
```

Tekshirish:
```bash
helm repo list
```

---

## 6. Qo'shilgan repodan chart qidirish

**Savol:** Which command is used to search for the `wordpress` package from the newly added bitnami repository?

**Javob:** `helm search repo wordpress`

```bash
helm search repo wordpress
```

---

## 7. Nechta helm repozitoriy bor?

**Savol:** How many helm chart repositories are there in the controlplane node now?

```bash
helm repo list
```

Chiqish:
```
NAME        URL
bitnami     https://charts.bitnami.com/bitnami
puppet      https://puppetlabs.github.io/puppetserver-helm-chart
hashicorp   https://helm.releases.hashicorp.com
```

**Javob:** `3`

---

## 8. Apache'ni o'rnatish

**Savol:** Deploy the Apache application on the cluster using the `apache` chart from the `bitnami` repository. Release name: `amaze-surf`

```bash
helm install amaze-surf bitnami/apache
```

Tekshirish:
```bash
helm list
```

Chiqish:
```
NAME        NAMESPACE  REVISION  STATUS    CHART          APP VERSION
amaze-surf  default    1         deployed  apache-11.3.2  2.4.63
```

---

## 9. O'rnatilgan Apache versiyasi

**Savol:** What version of apache did we just install on the cluster using the helm chart?

**Variantlar:** 2.4.7 / 2.4.63 / 2.2.9 / 2.4.1

**Javob:** `2.4.63` (APP VERSION ustunidan)

---

## 10. Nechta nginx release bor?

**Savol:** How many releases of `nginx` charts can you see installed in the cluster now?

```bash
helm list -A
```

Chiqish:
```
NAME          NAMESPACE  REVISION  STATUS    CHART          APP VERSION
amaze-surf    default    1         deployed  apache-11.3.2  2.4.63
crazy-web     default    1         deployed  nginx-19.0.0   1.27.4
happy-browse  default    1         deployed  nginx-19.0.0   1.27.4
```

**Javob:** `2` (crazy-web va happy-browse)

> `-A` (`--all-namespaces`) barcha namespace'lardagi release'larni ko'rsatadi.

---

## 11. Release'ni o'chirish

**Savol:** Uninstall the nginx chart release `happy-browse` from the cluster.

```bash
helm uninstall happy-browse
```

Tekshirish:
```bash
helm list
```

---

## 12. Repozitoriyni o'chirish

**Savol:** Remove the Hashicorp helm repository from the cluster.

```bash
helm repo remove hashicorp
```

Tekshirish:
```bash
helm repo list
```

---

## Foydali buyruqlar xulosasi

| Buyruq | Vazifa |
|---|---|
| `helm search hub <nom>` | Artifact Hub'dan chart qidirish |
| `helm search repo <nom>` | Lokal repolardan chart qidirish |
| `helm repo add <nom> <url>` | Repozitoriy qo'shish |
| `helm repo list` | Repozitoriylar ro'yxati |
| `helm repo remove <nom>` | Repozitoriyni o'chirish |
| `helm repo update` | Repolarni yangilash |
| `helm install <release> <repo>/<chart>` | Chart o'rnatish |
| `helm list` / `helm list -A` | Release'lar ro'yxati (barcha namespace: `-A`) |
| `helm uninstall <release>` | Release'ni o'chirish |
| `helm upgrade <release> <chart>` | Release'ni yangilash |
| `helm rollback <release> <revision>` | Oldingi versiyaga qaytarish |
