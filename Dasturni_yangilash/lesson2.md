# NideJS dasturini yangilaymiz
NodeJS dasturini obnavleniya qilishdan oldin yangilanish protsesini ko'rib tursih uchun quidagi komandalarni kiritib olamiz:
```bash
kubectl rollout status deployment/k8s-web-hello
```
NodeJS dasturini yangilash uchun quidagi komandani kirgizamiz:
```bash
kubectl set image deployment k8s-web-hello k8s=mrpocker88/k8s:ver2
```
