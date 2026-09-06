# 🔍 Podlarni tekshirish

Yaratilgan Pod ishlayaptimi? `get`, `describe` va `logs` — Kubernetes'da eng ko'p ishlatiladigan uchta tekshiruv buyrug'i.

```mermaid
graph LR
    A["kubectl get pods"] --> B["kubectl describe pod"]
    B --> C["kubectl logs"]
    C --> D["Pod IP manzili va tarmoq"]
```

## 📚 Darslar tartibi

| # | Fayl | Mavzu |
|---|---|---|
| 1 | [lesson.md](lesson.md) | NGINX Pod faoliyatini tekshirish: get, describe, logs va Pod IP |

## 💡 Qanday o'qish kerak

1. Darslarni jadvaldagi tartibda o'qing — har biri oldingisiga tayanadi.
2. Buyruqlarni o'z klasteringizda qaytaring. O'qish emas, qilish esda qoladi.
3. `amaliyot/` papkasidagi tayyor fayllardan foydalaning — qo'lda ko'chirish shart emas.
4. Har dars oxiridagi `🧪 Mustaqil topshiriqlar` ni yechimni ochishdan oldin bajaring.

## 🔗 Manbalar

- [Kubernetes rasmiy hujjatlari](https://kubernetes.io/docs/home/)
- [kubectl Cheat Sheet](https://kubernetes.io/docs/reference/kubectl/quick-reference/)

➡️ **Keyingi bo'lim:** [Konteynerlar_bilan_ishlash](../Konteynerlar_bilan_ishlash/)

---
⬅️ [Kurs bosh sahifasi](../README.md) · 📖 [Uslub qo'llanmasi](../USLUB.md)
