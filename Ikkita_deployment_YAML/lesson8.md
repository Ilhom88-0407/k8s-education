# Docker Hub ga yangilangan image ni push qilish
## Docker Hub ga yangilangan image ni push qilish uchun quyidagi buyruqlarni bajarishimiz kerak:

```bash 
docker build -t your_dockerhub_username/your_image_name:tag .
docker push your_dockerhub_username/your_image_name:tag
```
## Bu buyruqlar `Dockerfile` dan yangilangan image ni yaratadi va `Docker Hub` ga push qiladi. Siz `your_dockerhub_username`, `your_image_name`, va `tag` ni o'zingizning ma'lumotlaringiz bilan almashtirishingiz kerak.
## Endi siz `Docker Hub` da yangilangan image ni ko'rishingiz mumkin.   
# Endi biz `Kubernetes` klasterida yangilangan image ni ishlatish uchun `YAML` faylni yangilaymiz. Quyidagi `YAML` faylni yaratamiz:

```yaml
apiVersion: v1
kind: Pod   
metadata:
    name: my-pod
spec:
    containers: 
    - name: my-container
      image: your_dockerhub_username/your_image_name:tag
      ports:
      - containerPort: 80
```
### agarda biz image ni bitta versiyadan ikkinchi versiyaga yangilashni istasak biz docker hub ga yangilangan image ni push qilamiz va `YAML` faylni yangilaymiz. Masalan, agar biz `my-image:1.0` dan `my-image:2.0` ga yangilashni istasak, biz quyidagi buyruqlarni bajarishimiz kerak:

```bash
docker build -t your_dockerhub_username/my-image:1.0  -t your_dockerhub_username/my-image:2.0
docker push your_dockerhub_username/my-image --all-tags
``` 
