# NodeJS dasturini docker imigini yaratish va uni yangilash
endi bo'lsa biz NodeJS dasturini index.jms fayliga o'zgartirish kiritamiz va uni yangilaymiz. index.js faylini ochamiz va uni ichidagi VERSION 1: matinini VERSION 2: ga o'zgartiramiz va saqlaymiz. 
```bash
docker tag k8s-web-hello:1.0.2 <dockerhub_username>/k8s-web-hello:1.0.2 # imige yaratish uchun
manda dokcer desktop bo'lgani uchun komandasidan foydalandim
docker buildx build --platform linux/amd64,linux/arm64 -t <dockerhub_username>/k8s-web-hello:1.0.2 .
va 
docker push <dockerhub_username>/k8s-web-hello:1.0.0 # DockerHub ga yuklash uchun
yoki 
docker push <dockerhub_username>/k8s-web-hello --all-tags  
```

ketma ketlikda o'zimni proyektimda:
```bash
docker build -t k8s-web-hello:1.0.2 .
docker tag k8s-web-hello:1.0.2 mrpocker88/k8s-web-hello:1.0.2
docker push mrpocker88/k8s-web-hello:1.0.2 
```