# 🧩 Pod asoslari

Kubernetes'dagi eng kichik joylashtirish birligi — Pod. Nima uchun Kubernetes konteynerni emas, aynan Pod'ni boshqaradi va Pod'ning hayot sikli qanday kechadi.

```mermaid
graph LR
    A["Pod nima"] --> B["Pod va konteyner farqi"]
    B --> C["Pod hayot sikli"]
    C --> D["Birinchi Pod yaratish"]
```

## 📚 Darslar tartibi

| # | Fayl | Mavzu |
|---|---|---|
| 1 | [lesson.md](lesson.md) | Pod nima, konteynerdan farqi, hayot sikli va birinchi Pod |

## 💡 Qanday o'qish kerak

1. Darslarni jadvaldagi tartibda o'qing — har biri oldingisiga tayanadi.
2. Buyruqlarni o'z klasteringizda qaytaring. O'qish emas, qilish esda qoladi.
3. `amaliyot/` papkasidagi tayyor fayllardan foydalaning — qo'lda ko'chirish shart emas.
4. Har dars oxiridagi `🧪 Mustaqil topshiriqlar` ni yechimni ochishdan oldin bajaring.

## 🔗 Manbalar

- [Kubernetes rasmiy hujjatlari](https://kubernetes.io/docs/home/)
- [kubectl Cheat Sheet](https://kubernetes.io/docs/reference/kubectl/quick-reference/)

➡️ **Keyingi bo'lim:** [Podlarni_tekshirish](../Podlarni_tekshirish/)

---
⬅️ [Kurs bosh sahifasi](../README.md) · 📖 [Uslub qo'llanmasi](../USLUB.md)
