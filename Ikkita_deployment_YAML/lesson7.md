# YAML malumotlarini yaratish bo'yicha yakuniy dars

## Bu darsda biz kichik bir `YAML` fayl yaratishni o'rganamiz.
## `YAML` fayl yaratish uchun biz oddiy matn muharriridan foydalanamiz. Masalan, `Notepad` yoki `VS Code`.
## Quyidagi `YAML` faylni yaratamiz:

```yaml
apiVersion: v1
kind: Pod
metadata:
    name: my-pod        
spec:
    containers:
    - name: my-container
      image: nginx
      ports:
      - containerPort: 80   
``` 
## Bu `YAML` fayl `Kubernetes` uchun `Pod` resursini yaratadi.
## `apiVersion` - bu resursning API versiyasini ko'rsatadi.
## `kind` - bu resursning tipini ko'rsatadi. 
## `metadata` - bu resursning metadata qismini ko'rsatadi. Bu yerda biz `name` maydonini `my-pod` deb belgilaymiz.
## `spec` - bu resursning spetsifikatsiyasini ko'rsatadi. Bu yerda biz `containers` maydonini belgilaymiz.
## `containers` - bu resursning konteynerlarini ko'rsatadi. Bu yerda biz bitta konteyner yaratamiz.
## `name` - bu konteynerning nomini ko'rsatadi. Bu yerda biz `my-container` deb belgilaymiz.
## `image` - bu konteynerning image'ini ko'rsatadi. Bu yerda biz `nginx` image'ini ishlatamiz.
## `ports` - bu konteynerning portlarini ko'rsatadi. Bu yerda biz `containerPort` maydonini `80` deb belgilaymiz.
## Endi biz bu `YAML` faylni saqlaymiz. Masalan  `my-pod.yaml` nomi bilan saqlaymiz.
## Endi biz  bu `YAML` faylni `Kubernetes` klasteriga qo'llaymiz. Buning uchun quyidagi buyruqni bajarishimiz kerak:

```bash
kubectl apply -f my-pod.yaml
``` 
# Bu buyruq `my-pod.yaml` faylini `Kubernetes` klasteriga qo'llaydi va `Pod` resursini yaratadi.
# Endi biz `Pod` resursining holatini tekshirishimiz mumkin. Buning uchun quyidagi buyruqni bajarishimiz kerak:

```bash
kubectl get pods
```     
# Bu buyruq `Kubernetes` klasteridagi barcha `Pod` resurslarini ko'rsatadi. Siz `my-pod` nomli `Pod` resursini ko'rishingiz kerak.
# Agar siz `my-pod` resursining holatini batafsil ko'rishni istasangiz, quyidagi buyruqni bajarishingiz mumkin:

```bash
kubectl describe pod my-pod
```     
# Bu buyruq `my-pod` resursining holatini ko'rsatadi.   
# Endi biz `my-pod` resursini o'chirishimiz mumkin. Buning uchun quyidagi buyruqni bajarishimiz kerak:

```bash
kubectl delete pod my-pod
```
# Bu buyruq `my-pod` resursini `Kubernetes` klasteridan o'chiradi.
# Endi biz `my-pod` resursining holatini tekshirishimiz mumkin. Buning uchun quyidagi buyruqni bajarishimiz kerak:

```bash
kubectl get pods
```
# Bu buyruq `Kubernetes` klasteridagi barcha `Pod` resurslarini ko'rsatadi. Siz `my-pod` nomli `Pod` resursini ko'rmasligingiz kerak, chunki u o'chirilgan.
# Bu darsda biz `YAML` malumotlarini yaratish va `Kubernetes` klasteriga qo'llashni o'rgandik. Endi siz `YAML` fayllarini yaratish va `Kubernetes` resurslarini boshqarish bo'yicha asosiy bilimlarga egasiz. Keyingi darslarda biz yanada murakkab `YAML` fayllarini yaratishni o'rganamiz.
