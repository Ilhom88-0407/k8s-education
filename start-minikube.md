##
## minikube start  ##-->> zapusk minikube 
## minikube help   ##-->> pokazivayt komandi vozmojniy

### Создания Аалиаса ####
## dlya sozdaniya aliasa v terminale nabiramy komandu
```bash
> alias k=kubectl
> k kluster-info ##> pokajit informasiyu

> kubectl get namespaces  ##> pokajit namespasi

> kubectl get --namespaces=kube-system  ##> pokajit pod vnutri namspase kube-system

> kubectl get pods ----namespaces=kube-system  ##> kube-system ni ichidagi podlarni ko'rish uchun
```

####   17 dars   #####
##___ podlarni yaratish ___##

>  kubectl run my-nginx-pod --image=nginx
 - my-nginx-pod   podning nomlanishi
 - --image qaysi imagedan foydalanadi

