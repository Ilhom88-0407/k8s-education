#!/usr/bin/env python3
"""Darslik uchun barcha SVG sxemalarni yaratadi.

Har bir sxema alohida funksiya. Ishga tushirish:

    python3 skriptlar/sxemalarni_yaratish.py

Sxemalar tegishli bo'lim ichidagi `rasmlar/` papkasiga yoziladi.
Fayllar git'ga kommit qilinadi — bu skript ularni QAYTA yaratish uchun,
o'quvchiga uni ishga tushirish shart emas.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from sxema import Sxema, MATN2, PALITRA  # noqa: E402

KOK = PALITRA["control"][1]
YASHIL = PALITRA["pod"][1]
BINAFSHA = PALITRA["tarmoq"][1]
SARIQ = PALITRA["ogoh"][1]
QIZIL = PALITRA["xato"][1]


def pod_tuzilishi() -> Path:
    """Pod ichida nima bor va nima uchun u konteynerdan katta birlik."""
    s = Sxema(800, 452, "Pod ichki tuzilishi",
              "Pod bir yoki bir nechta konteynerni o'rab turadi. Konteynerlar bitta "
              "tarmoq namespace'ini bo'lishadi — ya'ni bitta IP manzil va bitta port "
              "maydoni — hamda umumiy volume orqali fayl almashadi. Shuning uchun "
              "Kubernetes konteynerni emas, Pod'ni rejalashtiradi va o'chiradi.")
    s.sarlavha_matni(28, 36, "Pod ichki tuzilishi",
                     "Nima uchun Kubernetes konteynerni emas, Pod'ni boshqaradi")

    s.panel(28, 82, 484, 344, "POD — web-app", rol="pod")
    s.matn(270, 118, "Kubernetes uchun eng kichik joylashtirish birligi",
           olcham=11.5, rang=MATN2)

    s.quti(48, 134, 220, 88, "konteyner: web",
           "nginx:1.27-alpine", "80-portda tinglaydi", rol="oq")
    s.quti(288, 134, 204, 88, "konteyner: log-agent",
           "fluent-bit:3.1", "loglarni yig'adi", rol="oq")

    s.quti(48, 240, 444, 82, "Umumiy tarmoq namespace",
           "Bitta IP: 10.244.0.7 — o'zaro localhost orqali gaplashadi",
           "Portlar Pod ichida takrorlanmasligi kerak", rol="tarmoq")

    s.quti(48, 336, 444, 78, "Umumiy volume: /var/log",
           "web yozadi, log-agent o'qiydi — bitta papka",
           "Pod o'chsa, emptyDir turidagi volume ham yo'qoladi", rol="ogoh")

    x = 536
    s.quti(x, 134, 236, 88, "Birga tug'iladi",
           "Konteynerlar bitta node'ga", "birga rejalashtiriladi", rol="oq")
    s.quti(x, 240, 236, 82, "Birga o'ladi",
           "Pod o'chirilsa, ichidagi barcha", "konteynerlar ham o'chadi", rol="oq")
    s.quti(x, 336, 236, 78, "Ko'paytirish = Pod nusxasi",
           "Bitta konteynerni emas,", "butun Pod'ni nusxalaysiz", rol="oq")

    s.strelka(512, 178, 530, 178, rang=YASHIL)
    s.strelka(512, 281, 530, 281, rang=YASHIL)
    s.strelka(512, 375, 530, 375, rang=YASHIL)
    return s.saqla("Podlar_asoslari/rasmlar/pod_tuzilishi.svg")


def deployment_ierarxiyasi() -> Path:
    """Deployment -> ReplicaSet -> Pod egalik zanjiri."""
    s = Sxema(800, 470, "Deployment, ReplicaSet va Pod o'rtasidagi bog'liqlik",
              "Siz Deployment yaratasiz. Deployment o'zi ReplicaSet yaratadi, "
              "ReplicaSet esa kerakli sondagi Pod'ni yaratadi va ularning sonini "
              "doim kuzatib turadi. Pod o'chirilsa, ReplicaSet darrov yangisini "
              "o'rniga qo'yadi. Image o'zgarsa, Deployment yangi ReplicaSet yaratadi "
              "va trafikni asta-sekin unga ko'chiradi.")
    s.sarlavha_matni(28, 36, "Deployment → ReplicaSet → Pod",
                     "Uchta obyekt, uchta vazifa — kim nima qiladi")

    s.quti(258, 78, 284, 66, "Deployment", "nginx-deploy", rol="control")
    s.quti(600, 74, 172, 74, "Siz yozasiz",
           "faqat shu obyektni", "tahrirlaysiz", rol="oq", radius=7,
           bosh_olcham=12)
    s.strelka(596, 111, 550, 111, rang=KOK)

    s.strelka(400, 144, 400, 184, rang=KOK)
    s.matn(412, 169, "yaratadi va boshqaradi", olcham=11, rang=KOK, markaz=False)

    s.quti(258, 186, 284, 66, "ReplicaSet", "nginx-deploy-5c689d4b9f",
           rol="control")
    s.quti(600, 182, 172, 74, "Sanoqni saqlaydi",
           "kam bo'lsa yangi Pod", "yaratadi", rol="oq", radius=7,
           bosh_olcham=12)
    s.strelka(596, 219, 550, 219, rang=KOK)

    for i, x in enumerate((92, 322, 552)):
        s.strelka(400, 252, x + 78, 298, rang=KOK)
        s.quti(x, 300, 156, 74, f"Pod {i + 1}",
               f"10.244.0.{i + 3}", "nginx:1.27", rol="pod")

    s.quti(92, 396, 616, 52, "Pod o'chirilsa yoki node yiqilsa — ReplicaSet "
                             "darhol yangi Pod yaratadi", rol="ogoh",
           bosh_olcham=12.5)
    return s.saqla("Deploymentlar/rasmlar/deployment_ierarxiyasi.svg")


def rolling_update() -> Path:
    """Rolling update bosqichma-bosqich."""
    s = Sxema(860, 430, "Rolling update qanday kechadi",
              "Image yangilanganda Deployment yangi ReplicaSet yaratadi va "
              "Pod'larni birdaniga emas, bittalab almashtiradi: avval bitta yangi "
              "Pod ko'tariladi, u tayyor bo'lgach bitta eski Pod o'chiriladi. "
              "Shu sababli yangilanish davomida ilova ishlab turadi.")
    s.sarlavha_matni(28, 36, "Rolling update — uzilishsiz yangilanish",
                     "Podlar birdaniga emas, bittalab almashtiriladi")

    bosqichlar = [
        ("1-bosqich", "Boshlang'ich holat", 3, 0, "Barcha podlar v1"),
        ("2-bosqich", "Yangi pod qo'shildi", 3, 1, "v2 tayyor bo'lishini kutamiz"),
        ("3-bosqich", "Eski pod o'chdi", 2, 2, "Almashtirish davom etadi"),
        ("4-bosqich", "Yakun", 0, 3, "Barcha podlar v2"),
    ]
    x = 28
    for nom, izoh, eski, yangi, tag in bosqichlar:
        s.panel(x, 82, 194, 296, nom, rol="control")
        s.matn(x + 97, 56 + 46, izoh, olcham=11.5, rang=MATN2)

        y = 128
        for i in range(eski):
            s.quti(x + 20, y, 154, 38, "Pod v1", rol="pod", radius=6, bosh_olcham=12)
            y += 46
        for i in range(yangi):
            s.quti(x + 20, y, 154, 38, "Pod v2", rol="tarmoq", radius=6, bosh_olcham=12)
            y += 46

        s.matn(x + 97, 356, tag, olcham=10.5, rang=MATN2)
        if x < 620:
            s.strelka(x + 196, 230, x + 218, 230, rang=MATN2)
        x += 208

    s.quti(28, 392, 804, 26, "maxSurge: qo'shimcha nechta pod ko'tarilishi mumkin"
                             "   ·   maxUnavailable: bir vaqtda nechta pod yo'q bo'lishi mumkin",
           rol="ogoh", radius=6, bosh_olcham=11.5)
    return s.saqla("Dasturni_yangilash/rasmlar/rolling_update.svg")








def servis_turlari() -> Path:
    """ClusterIP, NodePort va LoadBalancer — uchtasi yonma-yon."""
    s = Sxema(880, 470, "Service turlarini taqqoslash",
              "Uch xil Service turi bir xil ishni bajaradi — Pod'lar oldiga barqaror "
              "manzil qo'yadi — lekin ular turli masofadan ko'rinadi. ClusterIP faqat "
              "klaster ichidan, NodePort har node'ning IP manzili va 30000-32767 "
              "oralig'idagi port orqali, LoadBalancer esa bulut provayderi bergan "
              "haqiqiy tashqi IP orqali.")
    s.sarlavha_matni(28, 36, "Service turlari — kim qayerdan ko'ra oladi",
                     "Uchalasi ham Pod'lar oldiga barqaror manzil qo'yadi")

    ustunlar = [
        ("ClusterIP", "control", "Standart tur",
         ["Faqat klaster ICHIDAN", "ko'rinadi"],
         "10.96.0.15:80",
         ["Bir servis ikkinchisini", "chaqirganda ishlatiladi"]),
        ("NodePort", "tarmoq", "ClusterIP ustiga qo'shiladi",
         ["Har node'ning IP'si va", "30000-32767 porti orqali"],
         "192.168.49.2:31323",
         ["Sinov va demo uchun.", "Portni eslab qolish kerak"]),
        ("LoadBalancer", "pod", "NodePort ustiga qo'shiladi",
         ["Bulut bergan HAQIQIY", "tashqi IP orqali"],
         "203.0.113.10:80",
         ["Ishlab chiqarish uchun.", "Bulutda pul turadi"]),
    ]

    x = 28
    for nom, rol, tag, kim, manzil, izoh in ustunlar:
        s.panel(x, 80, 268, 376, nom, rol=rol)
        s.matn(x + 134, 126, tag, olcham=11, rang=MATN2)

        s.quti(x + 20, 140, 228, 42, "Mijoz", rol="oq", radius=6, bosh_olcham=12)
        s.strelka(x + 134, 182, x + 134, 206, rang=MATN2)
        s.quti(x + 20, 210, 228, 76, "Service", *kim, rol=rol, radius=6)
        s.matn(x + 134, 306, manzil, olcham=11.5, mono=True)
        s.strelka(x + 134, 314, x + 134, 336, rang=MATN2)

        for i in range(3):
            s.quti(x + 20 + i * 78, 338, 70, 46, f"Pod {i + 1}", rol="pod",
                   radius=6, bosh_olcham=11.5)

        s.quti(x + 20, 398, 228, 48, izoh[0], izoh[1], rol="oq", radius=6,
               bosh_olcham=11, qator_olcham=10.5)
        x += 284
    return s.saqla("Servislar/rasmlar/servis_turlari.svg")


def service_endpoints() -> Path:
    """Service -> Endpoints -> Pod: selektor qanday ishlaydi."""
    s = Sxema(860, 470, "Service Pod'larni qanday topadi",
              "Service Pod'ni nomi bilan emas, label selektori bilan topadi. "
              "Mos keluvchi har bir tayyor Pod'ning IP manzili EndpointSlice ga "
              "yoziladi. kube-proxy shu ro'yxatga qarab har node'da iptables "
              "qoidasini yozadi — shuning uchun Service IP'siga kelgan paket "
              "to'g'ridan-to'g'ri Pod'ga yo'naltiriladi.")
    s.sarlavha_matni(28, 36, "Service → EndpointSlice → Pod",
                     "Selektor mos kelgan Pod ro'yxatga tushadi, kelmagani tushmaydi")

    s.quti(28, 86, 186, 62, "Mijoz Pod", "curl http://web-svc", rol="oq")
    s.strelka(214, 117, 300, 117, "DNS so'rovi", rang=BINAFSHA, yorliq_ofset=-9)

    s.quti(304, 82, 246, 70, "Service: web-svc",
           "ClusterIP 10.96.0.15:80", "selector: app=web", rol="tarmoq")

    s.strelka(427, 152, 427, 186, rang=BINAFSHA)
    s.quti(304, 188, 246, 66, "EndpointSlice",
           "Selektorga mos TAYYOR Podlar", "IP ro'yxati", rol="tarmoq")

    s.quti(600, 82, 232, 172, "kube-proxy",
           "Har node'da ishlaydi.", "EndpointSlice o'zgarsa,",
           "iptables/IPVS qoidalarini", "qayta yozadi.", rol="control")
    s.strelka(596, 168, 554, 168, rang=KOK)

    s.matn(28, 296, "Klasterdagi Podlar:", olcham=12.5, qalin=True, markaz=False)

    podlar = [
        (28, "Pod A", "app=web", "10.244.0.3", True, "Ready"),
        (240, "Pod B", "app=web", "10.244.0.4", True, "Ready"),
        (452, "Pod C", "app=web", "10.244.0.5", False, "NOT Ready"),
        (664, "Pod D", "app=db", "10.244.0.6", False, "boshqa label"),
    ]
    for x, nom, label, ip, mos, holat in podlar:
        rol = "pod" if mos else "xato"
        s.quti(x, 314, 168, 92, nom, label, ip, holat, rol=rol)
        if mos:
            s.egri(f"M 427 254 C 427 282, {x + 84} 282, {x + 84} 312", rang=BINAFSHA)

    s.quti(28, 424, 804, 30,
           "Ro'yxatga faqat 10.244.0.3 va 10.244.0.4 tushadi — "
           "Pod C hali tayyor emas, Pod D esa boshqa label bilan",
           rol="ogoh", radius=6, bosh_olcham=11.5)
    return s.saqla("Servislar/rasmlar/service_endpoints.svg")


def manifest_anatomiyasi() -> Path:
    """YAML manifestning to'rt majburiy qismi."""
    s = Sxema(800, 552, "Kubernetes manifestining tuzilishi",
              "Har qanday Kubernetes manifesti to'rt qismdan iborat: apiVersion "
              "qaysi API guruhi ekanini, kind qanday obyekt ekanini, metadata "
              "obyektning nomi va labellarini, spec esa kerakli holatni "
              "belgilaydi. Klaster status maydonini o'zi to'ldiradi — uni siz "
              "yozmaysiz.")
    s.sarlavha_matni(28, 36, "Manifest anatomiyasi",
                     "To'rtta majburiy qism — hammasi shu")

    bloklar = [
        ("apiVersion: apps/v1", "control", "Qaysi API guruhi va versiyasi",
         "Deployment uchun apps/v1, Pod va Service uchun v1"),
        ("kind: Deployment", "control", "Qanday obyekt yaratilyapti",
         "Pod, Deployment, Service, ConfigMap ..."),
        ("metadata:", "tarmoq", "Obyektning kimligi",
         "name, namespace, labels, annotations"),
        ("spec:", "pod", "KERAKLI holat — siz nimani xohlaysiz",
         "replicas, template, selector, containers ..."),
    ]
    y = 84
    for kod, rol, bosh, izoh in bloklar:
        s.quti(28, y, 330, 76, kod, rol=rol, mono=True, bosh_olcham=14)
        s.strelka(358, y + 38, 396, y + 38, rang=MATN2)
        s.quti(400, y, 372, 76, bosh, izoh, rol="oq", bosh_olcham=12.5)
        y += 90

    s.quti(28, y, 744, 76, "status:",
           "Bu qismni SIZ yozmaysiz — klaster o'zi to'ldiradi va doim yangilab turadi.",
           "`kubectl get -o yaml` da ko'rinadi: nechta pod tayyor, oxirgi shart qanday.",
           rol="ogoh", mono=False, bosh_olcham=13.5)
    return s.saqla("YAML_yaratish/rasmlar/manifest_anatomiyasi.svg")




def image_aylanmasi() -> Path:
    """Kod -> image -> registry -> klaster: to'liq aylanma."""
    s = Sxema(880, 400, "O'z ilovangiz klasterga qanday yetib boradi",
              "Kod Dockerfile bilan image'ga aylanadi, image registry'ga yuklanadi, "
              "Deployment esa registry'dan tortib olib Pod ichida ishga tushiradi. "
              "Yangi versiya chiqarish shu aylananing takrorlanishi: yangi teg bilan "
              "build, push, keyin kubectl set image.")
    s.sarlavha_matni(28, 36, "Kod → image → registry → klaster",
                     "Yangi versiya chiqarish shu aylananing takrorlanishi")

    qadamlar = [
        ("1. Kod", "oq", ["index.mjs", "package.json"], ""),
        ("2. Dockerfile", "ogoh", ["FROM node:22-alpine", "COPY . ."], "docker build"),
        ("3. Image", "control", ["mrpocker88/app:1.0.2", "lokal mashinada"], "docker push"),
        ("4. Registry", "tarmoq", ["Docker Hub", "yoki xususiy registry"], "kubectl apply"),
        ("5. Pod", "pod", ["Klaster image'ni", "tortib oladi va ishga tushiradi"], ""),
    ]
    x = 28
    for nom, rol, qatorlar, buyruq in qadamlar:
        s.quti(x, 110, 148, 96, nom, *qatorlar, rol=rol, bosh_olcham=13)
        if buyruq:
            s.strelka(x + 148, 158, x + 176, 158, rang=MATN2)
            s.matn(x + 162, 132, buyruq, olcham=10, rang=MATN2, mono=True)
        x += 176

    s.egri("M 800 210 C 800 262, 470 262, 470 262", rang=MATN2)
    s.egri("M 470 262 C 140 262, 102 262, 102 214", rang=MATN2)
    s.matn(440, 282, "Kod o'zgardi -> yangi TEG bilan qaytadan build va push",
           olcham=11.5, rang=MATN2)

    s.quti(28, 300, 824, 76, "Nima uchun har safar YANGI teg kerak",
           "Bir xil teg bilan qayta push qilsangiz, klaster image o'zgarganini bilmaydi —",
           "u kesh'dagi eskisini ishlatib yuboradi. `latest` tegi ham shu sababli xavfli.",
           rol="xato", bosh_olcham=13)
    return s.saqla("Custom_obrazlar_yaratish/rasmlar/image_aylanmasi.svg")


def ikki_deployment() -> Path:
    """Ikki ilova bir-biri bilan Service DNS nomi orqali gaplashadi."""
    s = Sxema(860, 430, "Ikki deployment o'zaro qanday gaplashadi",
              "Tashqi so'rov LoadBalancer servis orqali birinchi ilovaga keladi. "
              "Birinchi ilova ikkinchisini IP manzili bilan emas, Service'ning DNS "
              "nomi bilan chaqiradi. Shuning uchun ikkinchi ilovaning Pod'lari "
              "o'chib-yonsa ham, birinchi ilovaning kodini o'zgartirish kerak emas.")
    s.sarlavha_matni(28, 36, "Servis DNS nomi orqali chaqirish",
                     "Pod IP'lari o'zgaraveradi, DNS nomi esa o'zgarmaydi")

    s.quti(28, 96, 150, 60, "Foydalanuvchi", "brauzer", rol="oq")
    s.strelka(178, 126, 214, 126, rang=MATN2)
    s.quti(218, 96, 168, 60, "LoadBalancer", "203.0.113.10:80", rol="tarmoq")

    s.panel(28, 178, 796, 232, "KLASTER ICHIDA", rol="control")

    s.quti(52, 214, 214, 84, "web-to-nginx", "Deployment (3 replica)",
           "Express ilova", rol="pod")
    s.strelka(302, 126, 302, 210, rang=MATN2)

    s.quti(52, 316, 214, 76, "/ yo'li", "o'z javobini qaytaradi", rol="oq",
           bosh_olcham=12)

    s.strelka(266, 256, 330, 256, "/nginx so'rovi", rang=BINAFSHA, yorliq_ofset=-10)
    s.quti(334, 214, 190, 84, "Service: nginx", "ClusterIP",
           "http://nginx  <- DNS nomi", rol="tarmoq")
    s.strelka(524, 256, 588, 256, rang=BINAFSHA)
    s.quti(592, 214, 208, 84, "nginx", "Deployment (5 replica)",
           "javobni qaytaradi", rol="pod")

    s.quti(334, 316, 466, 76, "Kod ichida IP emas, nom yoziladi",
           "fetch('http://nginx')  — Kubernetes DNS uni ClusterIP'ga aylantiradi",
           "Pod'lar almashsa ham nom o'zgarmaydi", rol="ogoh", bosh_olcham=12.5)
    return s.saqla("Ikkita_deployment_YAML/rasmlar/ikki_deployment.svg")


def konteynerga_kirish() -> Path:
    """exec, logs va port-forward — uchtasi nima qiladi."""
    s = Sxema(860, 390, "Ishlab turgan Pod bilan ishlashning uch usuli",
              "kubectl exec konteyner ichida buyruq bajaradi, kubectl logs "
              "konteynerning standart chiqishini o'qiydi, kubectl port-forward esa "
              "lokal portni Pod portiga ulaydi. Uchalasi ham apiserver orqali "
              "o'tadi — ya'ni node'ga SSH qilish shart emas.")
    s.sarlavha_matni(28, 36, "exec, logs va port-forward",
                     "Uchalasi ham apiserver orqali ishlaydi — SSH kerak emas")

    s.quti(340, 84, 180, 54, "kube-apiserver", rol="control")
    s.quti(340, 300, 180, 62, "Pod: web-app", "konteyner: nginx", rol="pod")
    s.strelka(430, 138, 430, 296, rang=MATN2, ikki_tomon=True)
    s.matn(442, 224, "kubelet orqali", olcham=10.5, rang=MATN2, markaz=False)

    usullar = [
        (28, "kubectl exec -it", ["Konteyner ichida", "buyruq bajaradi"],
         "-- /bin/sh", "control"),
        (596, "kubectl logs -f", ["Konteynerning chiqishini", "o'qiydi"],
         "--tail=50", "tarmoq"),
    ]
    for x, nom, qatorlar, bayroq, rol in usullar:
        s.quti(x, 84, 236, 88, nom, *qatorlar, rol=rol, mono=False,
               bosh_olcham=13)
        s.matn(x + 118, 190, bayroq, olcham=11, rang=MATN2, mono=True)

    s.strelka(264, 128, 336, 128, rang=KOK)
    s.strelka(592, 128, 524, 128, rang=BINAFSHA)

    s.quti(28, 214, 236, 88, "kubectl port-forward", "Lokal portni Pod portiga",
           "ulaydi", rol="ogoh", bosh_olcham=13)
    s.matn(146, 320, "localhost:8080 -> pod:80", olcham=11, rang=MATN2, mono=True)
    s.egri("M 264 258 C 310 258, 310 320, 336 320", rang=SARIQ)

    s.quti(596, 214, 236, 148, "Nima uchun SSH kerak emas",
           "Uchala buyruq ham apiserver", "orqali o'tadi. Node'ga to'g'ridan-",
           "to'g'ri kirish huquqi bo'lmasa ham", "ular ishlaydi.", rol="oq",
           bosh_olcham=12.5)
    s.strelka(592, 288, 528, 300, rang=MATN2)
    return s.saqla("Konteynerlar_bilan_ishlash/rasmlar/konteynerga_kirish.svg")


def troubleshooting_daraxti() -> Path:
    """Nosozlikni qaysi qatlamdan qidirish kerak."""
    s = Sxema(880, 500, "Nosozlikni qidirish tartibi",
              "Muammo paydo bo'lganda qaysi qatlamdan boshlash kerakligini "
              "ko'rsatuvchi qaror daraxti: avval ilovaning o'zi, keyin node, "
              "keyin control plane, oxirida tarmoq. Har qatlam uchun birinchi "
              "beriladigan buyruq ham ko'rsatilgan.")
    s.sarlavha_matni(28, 36, "Nosozlikni qaysi qatlamdan qidirish kerak",
                     "Yuqoridan pastga: eng ko'p uchraydiganidan boshlanadi")

    s.quti(330, 84, 220, 52, "Muammo bor", "foydalanuvchi shikoyati", rol="xato")
    s.strelka(440, 136, 440, 158, rang=MATN2)

    qatlamlar = [
        (166, "1. Ilova (eng ko'p uchraydi)", "pod",
         "kubectl get pods · describe pod · logs",
         "Pod Pending / CrashLoopBackOff / ImagePullBackOff"),
        (244, "2. Worker node", "ogoh",
         "kubectl get nodes · systemctl status kubelet",
         "Node NotReady, kubelet to'xtagan yoki sertifikat eskirgan"),
        (322, "3. Control plane", "control",
         "kubectl -n kube-system get pods · crictl ps",
         "scheduler yoki controller-manager podi ko'tarilmayapti"),
        (400, "4. Tarmoq", "tarmoq",
         "kubectl get svc,endpoints · nslookup",
         "Service Endpoints bo'sh, DNS ishlamayapti, CNI o'rnatilmagan"),
    ]
    for y, nom, rol, buyruq, belgi in qatlamlar:
        s.quti(28, y, 380, 66, nom, belgi, rol=rol, bosh_olcham=13)
        s.strelka(408, y + 33, 444, y + 33, rang=MATN2)
        s.quti(448, y, 404, 66, "Birinchi buyruq", buyruq, rol="oq",
               bosh_olcham=11.5, qator_olcham=11.5)
        if y < 400:
            s.matn(218, y + 76, "topilmadi ↓", olcham=10, rang=MATN2)
    return s.saqla("14_Troubleshooting/rasmlar/qaror_daraxti.svg")


def base_overlay() -> Path:
    """Kustomize base va overlay qanday birlashadi."""
    s = Sxema(880, 440, "Kustomize: base va overlay qanday birlashadi",
              "base katalogda barcha muhitlar uchun umumiy manifestlar turadi. "
              "Har bir overlay base'ni resources orqali import qiladi va faqat "
              "o'ziga kerakli farqni patch sifatida yozadi. kubectl apply -k "
              "ishga tushganda Kustomize ikkalasini birlashtirib, yakuniy "
              "manifestni hosil qiladi.")
    s.sarlavha_matni(28, 36, "base + overlay = yakuniy manifest",
                     "base o'zgarmaydi, farq esa overlay'da yoziladi")

    s.quti(28, 96, 236, 128, "base/", "kustomization.yaml",
           "nginx-depl.yaml (replicas: 1)", "service.yaml",
           "Barcha muhitlar uchun umumiy", rol="control", mono=False)

    muhitlar = [
        (96, "overlays/dev/", "replicas: 2", "pod"),
        (204, "overlays/staging/", "replicas: 3", "ogoh"),
        (312, "overlays/production/", "replicas: 10 + grafana", "tarmoq"),
    ]
    for y, nom, patch, rol in muhitlar:
        s.quti(336, y, 250, 88, nom, "resources: ../../base", patch,
               rol=rol, bosh_olcham=12.5)
        s.egri(f"M 264 160 C 300 160, 300 {y + 44}, 332 {y + 44}", rang=MATN2)
        s.strelka(586, y + 44, 626, y + 44, rang=MATN2)
        s.quti(630, y, 222, 88, "Yakuniy manifest",
               "base + shu overlay'ning patchi", rol="oq", bosh_olcham=12.5)

    s.quti(28, 250, 280, 150, "Nima uchun shunday",
           "base'dagi bitta o'zgarish uchala", "muhitga birdan yetib boradi.",
           "Muhitga xos farq esa faqat o'sha", "overlay'da qoladi —",
           "nusxa ko'chirish kerak emas.", rol="ogoh", bosh_olcham=13)

    s.quti(28, 412, 824, 24, "kubectl apply -k overlays/dev   ·   "
                             "kubectl kustomize overlays/dev (klasterga tegmasdan ko'rish)",
           rol="oq", radius=6, bosh_olcham=11.5, mono=True)
    return s.saqla("13_Kustomize_asoslari/rasmlar/base_overlay.svg")


def helm_oqimi() -> Path:
    """Chart -> values -> release -> revision."""
    s = Sxema(880, 420, "Helm: chart, values va release",
              "Chart — bu qolip. values.yaml qolipga qo'yiladigan qiymatlar. "
              "helm install ikkalasini birlashtirib klasterga yuboradi va natijani "
              "release deb ataydi. Har bir upgrade yangi revision yaratadi, "
              "shuning uchun helm rollback bilan orqaga qaytish mumkin.")
    s.sarlavha_matni(28, 36, "Chart + values = release",
                     "Har upgrade yangi revision yaratadi — shuning uchun rollback ishlaydi")

    s.quti(28, 96, 200, 104, "Chart", "templates/*.yaml", "Chart.yaml",
           "Qolip — o'zgarmaydi", rol="control")
    s.quti(28, 216, 200, 104, "values.yaml", "replicaCount: 3",
           "image.tag: 1.2.0", "Qiymatlar — muhitga qarab", rol="ogoh")

    s.strelka(228, 148, 288, 190, rang=MATN2)
    s.strelka(228, 268, 288, 226, rang=MATN2)
    s.quti(292, 168, 176, 80, "helm install", "qolip + qiymat", rol="tarmoq")
    s.strelka(468, 208, 528, 208, rang=MATN2)

    s.quti(532, 96, 320, 112, "Release: my-app", "Klasterdagi tirik obyektlar",
           "Deployment, Service, ConfigMap ...", rol="pod")

    s.matn(532, 244, "Revision tarixi:", olcham=12.5, qalin=True, markaz=False)
    revisions = [("rev 1", "1.2.0", "control"), ("rev 2", "1.3.0", "control"),
                 ("rev 3", "1.4.0 (joriy)", "pod")]
    x = 532
    for nom, tag, rol in revisions:
        s.quti(x, 256, 100, 56, nom, tag, rol=rol, radius=6, bosh_olcham=12)
        x += 110
    s.strelka(632, 284, 642, 284, rang=MATN2)
    s.strelka(742, 284, 752, 284, rang=MATN2)

    s.quti(28, 336, 824, 62, "helm rollback my-app 2",
           "Har revision saqlanadi, shuning uchun oldingi holatga qaytish bitta buyruq. "
           "kubectl bilan qo'lda qaytarishda esa qaysi fayl qanday edi — o'zingiz eslashingiz kerak.",
           rol="ogoh", bosh_olcham=13)
    return s.saqla("12_Helm_asoslari/rasmlar/helm_oqimi.svg")


def ha_control_plane() -> Path:
    """Bitta control plane vs uchta: nima farqi bor."""
    s = Sxema(880, 450, "Yuqori mavjudlik (HA): nega uchta control plane kerak",
              "Bitta control plane node yiqilsa, klasterni boshqarish to'xtaydi. "
              "Uchta node bo'lsa, bittasi yiqilganda qolgan ikkitasi etcd uchun "
              "kvorum (2 dan 3) hosil qiladi va klaster ishlashda davom etadi. "
              "Shuning uchun control plane nodelar soni doim toq bo'lishi kerak.")
    s.sarlavha_matni(28, 36, "Nega control plane nodelar soni TOQ bo'ladi",
                     "etcd qaror qabul qilishi uchun ko'pchilik ovoz kerak")

    s.panel(28, 84, 396, 340, "BITTA NODE — xavfli", rol="xato")
    s.quti(52, 128, 348, 76, "control plane 1", "apiserver + etcd + scheduler",
           rol="control")
    s.quti(52, 224, 348, 76, "Node yiqildi", "❌ klasterni boshqarib bo'lmaydi",
           rol="xato")
    s.matn(226, 336, "Ishlab turgan podlar yashaydi,", olcham=11.5, rang=MATN2)
    s.matn(226, 354, "lekin yangi pod yaratib bo'lmaydi,", olcham=11.5, rang=MATN2)
    s.matn(226, 372, "o'lganini ham hech kim tiklamaydi.", olcham=11.5, rang=MATN2)
    s.matn(226, 400, "kubectl javob bermaydi", olcham=11.5, rang=QIZIL, mono=True)

    s.panel(456, 84, 396, 340, "UCHTA NODE — HA", rol="pod")
    for i, y in enumerate((128, 200, 272)):
        buzuq = i == 2
        s.quti(480, y, 348, 60,
               f"control plane {i + 1}" + ("  ❌ yiqildi" if buzuq else ""),
               "etcd a'zosi" + ("" if not buzuq else " — ovoz bermaydi"),
               rol="xato" if buzuq else "control", radius=6, bosh_olcham=12.5)
    s.quti(480, 344, 348, 60, "Kvorum: 3 dan 2 ta tirik ✅",
           "Klaster normal ishlashda davom etadi", rol="pod", radius=6,
           bosh_olcham=12.5)
    return s.saqla("10_Klaster_dizayni/rasmlar/ha_control_plane.svg")


def expose_loadbalancer() -> Path:
    """kubectl expose --type=LoadBalancer nima yaratadi va trafik qanday keladi."""
    s = Sxema(880, 470, "kubectl expose --type=LoadBalancer nima qiladi",
              "Bitta buyruq uchta qatlamni birdan yoqadi. LoadBalancer turidagi "
              "Service NodePort'ni, NodePort esa ClusterIP'ni o'z ichiga oladi — "
              "ya'ni ilovaga uch xil manzildan kirish mumkin bo'lib qoladi. "
              "minikube'da haqiqiy tashqi IP yo'q, shuning uchun uni minikube "
              "tunnel taqlid qiladi.")
    s.sarlavha_matni(28, 36, "LoadBalancer uchta qatlamni birdan yoqadi",
                     "kubectl expose deploy web --type=LoadBalancer --port=80")

    s.quti(28, 92, 200, 54, "Tashqi mijoz", "brauzer yoki curl", rol="oq")
    s.strelka(228, 119, 288, 119, rang=MATN2)

    s.panel(288, 84, 564, 250, "Service: web  (type: LoadBalancer)", rol="tarmoq")

    qatlamlar = [
        (124, "3. Tashqi IP", "203.0.113.10:80",
         ("Bulut provayderi beradi.", "minikube'da — minikube tunnel"), "pod"),
        (192, "2. NodePort", "<har-node-IP>:31323",
         ("30000-32767 oralig'idan", "avtomatik tanlanadi"), "ogoh"),
        (260, "1. ClusterIP", "10.96.0.15:80",
         ("Faqat klaster ichidan ko'rinadi", "— asos shu"), "control"),
    ]
    for y, nom, manzil, izoh, rol in qatlamlar:
        s.quti(308, y, 236, 56, nom, manzil, rol=rol, radius=6, bosh_olcham=12.5)
        s.quti(566, y, 266, 56, izoh[0], izoh[1], rol="oq", radius=6,
               bosh_olcham=11, qator_olcham=10.5)

    s.strelka(426, 180, 426, 190, rang=MATN2)
    s.strelka(426, 248, 426, 258, rang=MATN2)

    s.strelka(428, 334, 428, 362, rang=MATN2)
    for i, x in enumerate((188, 388, 588)):
        s.quti(x, 364, 152, 62, f"Pod {i + 1}", "app=web", rol="pod")
        if x != 388:
            s.egri(f"M 428 348 C 428 356, {x + 76} 356, {x + 76} 362", rang=MATN2)

    s.quti(28, 364, 148, 62, "selector: app=web",
           "trafik shu label'li", "podlarga bo'linadi", rol="oq",
           bosh_olcham=11, qator_olcham=10)
    return s.saqla("Servislar/rasmlar/expose_loadbalancer.svg")


#: Barcha sxemalar. Yangi sxema qo'shsangiz, funksiyani shu ro'yxatga kiriting.
SXEMALAR = [
    pod_tuzilishi,
    deployment_ierarxiyasi,
    rolling_update,
    servis_turlari,
    service_endpoints,
    manifest_anatomiyasi,
    image_aylanmasi,
    ikki_deployment,
    konteynerga_kirish,
    troubleshooting_daraxti,
    base_overlay,
    helm_oqimi,
    ha_control_plane,
    expose_loadbalancer,
]


def main() -> int:
    """Barcha sxemalarni qayta yaratadi."""
    for fn in SXEMALAR:
        print(f"  ✔ {fn()}")
    print(f"\n{len(SXEMALAR)} ta sxema yaratildi.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
