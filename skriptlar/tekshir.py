#!/usr/bin/env python3
"""tekshir.py — k8s-education darsligining avtomatik sifat tekshiruvi.

Darslik 123 ta markdown fayl va yuzlab manifestdan iborat. Bu skript
USLUB.md da yozilgan qoidalarning mashina tekshira oladigan qismini
tekshiradi: buzuq markdown, imlo, til aralashuvi, o'lik havolalar,
ishlamaydigan YAML va h.k.

Klaster ham, internet ham talab qilinmaydi — faqat Python 3 va pyyaml.

Ishlatish:
    python3 skriptlar/tekshir.py            # to'liq tekshiruv
    python3 skriptlar/tekshir.py --qisqa    # faqat XATO larni ko'rsatish
    python3 skriptlar/tekshir.py --kod F002 # bitta tekshiruvni ishga tushirish

Chiqish kodi: XATO topilsa 1, aks holda 0. OGOHLANTIRISH chiqish kodiga
ta'sir qilmaydi.
"""
from __future__ import annotations

import argparse
import re
import sys
import unicodedata
from collections import defaultdict
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover
    sys.exit("pyyaml kerak:  pip install pyyaml")

ILDIZ = Path(__file__).resolve().parent.parent

# Tekshiruvdan butunlay chetlab o'tiladigan yo'llar
CHETLAB = {".git", "node_modules", ".github"}

# Bu fayllar xatolarni ATAYLAB sanab o'tadi, shuning uchun imlo va
# til tekshiruvidan ozod qilinadi.
IMLO_OZOD = {"USLUB.md", "skriptlar/imlo-qora-royxat.txt", "skriptlar/tekshir.py"}

# ```<teg> — ruxsat etilgan til teglari
RUXSAT_TEG = {
    "", "bash", "sh", "shell", "console", "text", "yaml", "yml", "json",
    "mermaid", "dockerfile", "javascript", "js", "python", "ruby", "toml",
    "ini", "html", "css", "xml", "diff", "sql", "go", "hcl", "properties",
    "markdown", "md", "env", "conf", "log", "jsonc", "tsv", "csv",
}

# --------------------------------------------------------------------------


class Hisobot:
    """Topilgan muammolarni yig'adi va tartibli chop etadi."""

    def __init__(self) -> None:
        self.yozuvlar: list[tuple[str, str, int, str, str]] = []

    def xato(self, kod: str, fayl: Path, qator: int, xabar: str) -> None:
        self.yozuvlar.append(("XATO", kod, qator, str(fayl), xabar))

    def ogoh(self, kod: str, fayl: Path, qator: int, xabar: str) -> None:
        self.yozuvlar.append(("OGOH", kod, qator, str(fayl), xabar))

    def chop(self, qisqa: bool = False) -> int:
        xatolar = [y for y in self.yozuvlar if y[0] == "XATO"]
        ogohlar = [y for y in self.yozuvlar if y[0] == "OGOH"]

        for daraja, ro_yxat in (("XATO", xatolar), ("OGOHLANTIRISH", ogohlar)):
            if qisqa and daraja != "XATO":
                continue
            if not ro_yxat:
                continue
            print(f"\n{'=' * 70}\n{daraja} ({len(ro_yxat)})\n{'=' * 70}")
            guruh: dict[str, list] = defaultdict(list)
            for _, kod, qator, fayl, xabar in ro_yxat:
                guruh[kod].append((fayl, qator, xabar))
            for kod in sorted(guruh):
                yozuvlar = guruh[kod]
                print(f"\n[{kod}] — {len(yozuvlar)} ta")
                for fayl, qator, xabar in sorted(yozuvlar)[:40]:
                    joy = f"{fayl}:{qator}" if qator else fayl
                    print(f"  {joy}: {xabar}")
                if len(yozuvlar) > 40:
                    print(f"  ... va yana {len(yozuvlar) - 40} ta")

        print(f"\n{'=' * 70}")
        print(f"Natija: {len(xatolar)} xato, {len(ogohlar)} ogohlantirish")
        print("=" * 70)
        return 1 if xatolar else 0


def md_fayllar() -> list[Path]:
    """Repozitoriyadagi barcha markdown fayllar (chetlab o'tiladiganlarsiz)."""
    return sorted(
        p for p in ILDIZ.rglob("*.md")
        if not CHETLAB & set(p.relative_to(ILDIZ).parts)
    )


def nisbiy(p: Path) -> Path:
    return p.relative_to(ILDIZ)


def fence_qatorlari(matn: str) -> list[tuple[int, int, str]]:
    """Har bir fence qatori uchun (qator, backtick soni, teg) qaytaradi.

    Markdown ichma-ich blokka ruxsat beradi: tashqi blok ichkisidan ko'proq
    backtick bilan ochiladi (```` ichida ``` ). Shuning uchun backtick sonini
    ham qaytaramiz — usiz USLUB.md kabi fayllar noto'g'ri "toq" deb sanaladi.
    """
    natija = []
    for i, qator in enumerate(matn.splitlines(), 1):
        m = re.match(r"^[ \t]*(`{3,})[ \t]*(.*)$", qator)
        if m:
            natija.append((i, len(m.group(1)), m.group(2).strip()))
    return natija


def kodsiz(matn: str) -> str:
    """Kod bloklari va `inline kod` ichini bo'shliqqa almashtiradi.

    Qator raqamlari saqlanadi. Havola va alt-matn tekshiruvlari uchun kerak:
    kod ichida yozilgan `![alt](rasm.png)` — bu namuna, haqiqiy havola emas.
    """
    qatorlar = matn.splitlines()
    ichi = set()
    boshi = None
    for qator_no, _teg, ochilish in ochiq_bloklar(matn):
        if qator_no == -1:
            continue
        if ochilish:
            boshi = qator_no
        elif boshi is not None:
            ichi.update(range(boshi, qator_no + 1))
            boshi = None
    natija = []
    for i, q in enumerate(qatorlar, 1):
        if i in ichi:
            natija.append("")
        else:
            natija.append(re.sub(r"`[^`]*`", lambda m: " " * len(m.group(0)), q))
    return "\n".join(natija)


def ochiq_bloklar(matn: str):
    """Fence larni stek bilan yuradi, (qator, teg, ochilishmi) beradi."""
    stek: list[int] = []
    for qator_no, uzunlik, teg in fence_qatorlari(matn):
        if stek and uzunlik >= stek[-1] and not teg:
            stek.pop()
            yield qator_no, teg, False
        elif not stek:
            stek.append(uzunlik)
            yield qator_no, teg, True
        # stek to'la va yangi ochilish -> ichki blok, e'tibor bermaymiz
    if stek:
        yield -1, "", True


# ============================ TEKSHIRUVLAR ================================


def f001_blok_balansi(h: Hisobot) -> None:
    """F001 — har faylda ``` belgilari juft bo'lishi kerak."""
    for p in md_fayllar():
        matn = p.read_text(encoding="utf-8", errors="replace")
        oxirgi = list(ochiq_bloklar(matn))
        if oxirgi and oxirgi[-1][0] == -1:
            ochilgan = [q for q, _, ochilish in oxirgi[:-1] if ochilish]
            h.xato("F001", nisbiy(p), ochilgan[-1] if ochilgan else 0,
                   "kod bloki ochilgan, lekin yopilmagan")


def f002_blok_teglari(h: Hisobot) -> None:
    """F002 — ochilish tegi ruxsat etilgan tillar ro'yxatidan bo'lsin.

    ```NAME  READY  STATUS  kabi holatlarda birinchi qator til tegi deb
    qabul qilinadi va renderda yo'qoladi.
    """
    for p in md_fayllar():
        matn = p.read_text(encoding="utf-8", errors="replace")
        for qator_no, teg, ochilish in ochiq_bloklar(matn):
            if not ochilish or qator_no == -1:
                continue
            birinchi = teg.split()[0].lower() if teg else ""
            if birinchi not in RUXSAT_TEG:
                h.xato("F002", nisbiy(p), qator_no,
                       f"noto'g'ri blok tegi: ```{teg[:50]}")


def f003_imlo(h: Hisobot, nomlar: set[str]) -> None:
    """F003 — qora ro'yxatdagi so'zlar darslikda uchramasligi kerak.

    Haqiqiy fayl nomlari (masalan `deploymant3.md`) chetlab o'tiladi —
    ular qayta nomlanmagan, shuning uchun ularga havola qonuniy.
    """
    # (xato, to'g'ri, faqat_kod_blokida)
    qora: list[tuple[str, str, bool]] = []
    royxat = ILDIZ / "skriptlar" / "imlo-qora-royxat.txt"
    for qator in royxat.read_text(encoding="utf-8").splitlines():
        qator = qator.strip()
        if not qator or qator.startswith("#") or "\t" not in qator:
            continue
        qismlar = qator.split("\t")
        faqat_kod = qismlar[0] == "KOD"
        if faqat_kod:
            qismlar = qismlar[1:]
        if len(qismlar) < 2:
            continue
        qora.append((qismlar[0].strip(), qismlar[1].strip(), faqat_kod))

    for p in md_fayllar():
        if str(nisbiy(p)) in IMLO_OZOD:
            continue
        matn = p.read_text(encoding="utf-8", errors="replace")
        # Qaysi qatorlar kod bloki ichida ekanini oldindan hisoblaymiz
        kod_ichi: set[int] = set()
        boshi = None
        for qator_no, _teg, ochilish in ochiq_bloklar(matn):
            if qator_no == -1:
                continue
            if ochilish:
                boshi = qator_no
            elif boshi is not None:
                kod_ichi.update(range(boshi, qator_no + 1))
                boshi = None
        for i, qator in enumerate(matn.splitlines(), 1):
            past = qator.lower()
            for xato, togri, faqat_kod in qora:
                if faqat_kod and i not in kod_ichi:
                    continue
                boshi = 0
                while (j := past.find(xato.lower(), boshi)) != -1:
                    boshi = j + 1
                    # Atrofdagi to'liq tokenni ajratamiz
                    a, b = j, j + len(xato)
                    while a > 0 and (qator[a - 1].isalnum() or qator[a - 1] in "_-."):
                        a -= 1
                    while b < len(qator) and (qator[b].isalnum() or qator[b] in "_-."):
                        b += 1
                    token = qator[a:b]
                    if token in nomlar:          # haqiqiy fayl nomi — qonuniy
                        continue
                    h.xato("F003", nisbiy(p), i, f"'{xato}' -> '{togri}'")


def f004_belgilar(h: Hisobot) -> None:
    """F004 — kirill harflari va egri apostroflar bo'lmasin.

    Darslik faqat o'zbek lotin yozuvida. ASCII apostrof ' ishlatiladi.
    """
    egri = "‘’ʻʼ´`"
    for p in md_fayllar():
        if str(nisbiy(p)) in IMLO_OZOD:
            continue
        for i, qator in enumerate(p.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
            kir = [c for c in qator if "Ѐ" <= c <= "ӿ"]
            if kir:
                h.xato("F004", nisbiy(p), i,
                       f"kirill harflari: {''.join(sorted(set(kir)))[:20]}")
            eg = [c for c in qator if c in egri and c != "`"]
            if eg:
                nom = ", ".join(sorted({unicodedata.name(c, hex(ord(c))) for c in eg}))
                h.xato("F004", nisbiy(p), i, f"egri apostrof ({nom}) — ASCII ' ishlating")


def f005_sarlavhalar(h: Hisobot) -> None:
    """F005 — sarlavha ierarxiyasi to'g'ri bo'lsin."""
    for p in md_fayllar():
        matn = p.read_text(encoding="utf-8", errors="replace")
        h1 = 0
        oldingi = 0
        blok_qatorlar = set()
        joriy = None
        for qator_no, teg, ochilish in ochiq_bloklar(matn):
            if qator_no == -1:
                continue
            if ochilish:
                joriy = qator_no
            elif joriy is not None:
                blok_qatorlar.update(range(joriy, qator_no + 1))
                joriy = None
        for i, qator in enumerate(matn.splitlines(), 1):
            if i in blok_qatorlar or not qator.startswith("#"):
                continue
            if re.match(r"^#{1,6}[ \t]+#{1,6}[ \t]", qator):
                h.xato("F005", nisbiy(p), i,
                       f"sarlavha ichida ikkinchi # belgisi: {qator[:60]}")
                continue
            m = re.match(r"^(#{1,6})[ \t]+\S", qator)
            if not m:
                continue
            daraja = len(m.group(1))
            if daraja == 1:
                h1 += 1
            if oldingi and daraja > oldingi + 1:
                h.ogoh("F005", nisbiy(p), i,
                       f"H{oldingi} dan keyin darrov H{daraja} — daraja tashlab ketilgan")
            oldingi = daraja
        if h1 == 0:
            h.xato("F005", nisbiy(p), 0, "faylda H1 (# ) sarlavha yo'q")
        elif h1 > 1:
            h.ogoh("F005", nisbiy(p), 0, f"{h1} ta H1 sarlavha — bittasi bo'lishi kerak")


def f006_havolalar(h: Hisobot) -> None:
    """F006 — ichki havolalar va rasmlar diskda mavjud bo'lsin."""
    naqsh = re.compile(r"!?\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
    for p in md_fayllar():
        for i, qator in enumerate(kodsiz(p.read_text(encoding="utf-8", errors="replace")).splitlines(), 1):
            for manzil in naqsh.findall(qator):
                if re.match(r"^(https?:|mailto:|#|data:)", manzil):
                    continue
                yol = manzil.split("#")[0]
                if not yol:
                    continue
                from urllib.parse import unquote
                nishon = (p.parent / unquote(yol)).resolve()
                if not nishon.exists():
                    h.xato("F006", nisbiy(p), i, f"havola topilmadi: {manzil}")


def f007_yetim_rasmlar(h: Hisobot) -> None:
    """F007 — hech qaysi darsdan havola qilinmagan rasmlar (ogohlantirish)."""
    ishlatilgan: set[Path] = set()
    naqsh = re.compile(r"!?\[[^\]]*\]\(([^)\s]+)\)")
    for p in md_fayllar():
        for manzil in naqsh.findall(kodsiz(p.read_text(encoding="utf-8", errors="replace"))):
            if re.match(r"^(https?:|mailto:|#|data:)", manzil):
                continue
            from urllib.parse import unquote
            ishlatilgan.add((p.parent / unquote(manzil.split("#")[0])).resolve())
    for kengaytma in ("*.png", "*.jpg", "*.jpeg", "*.svg", "*.gif"):
        for rasm in ILDIZ.rglob(kengaytma):
            if CHETLAB & set(rasm.relative_to(ILDIZ).parts):
                continue
            if rasm.resolve() not in ishlatilgan:
                kb = rasm.stat().st_size // 1024
                h.ogoh("F007", nisbiy(rasm), 0,
                       f"hech qayerdan havola qilinmagan ({kb} KB)")


def f008_amaliyot_yaml(h: Hisobot) -> None:
    """F008 — amaliyot/ dagi har YAML haqiqiy Kubernetes obyekti bo'lsin."""
    for y in sorted(ILDIZ.rglob("amaliyot/**/*.yaml")):
        matn = y.read_text(encoding="utf-8", errors="replace")
        if re.search(r"^\s*\.\.\.\s*$", matn, re.M) and "---" not in matn:
            h.xato("F008", nisbiy(y), 0, "faylda '...' qoldiruvchi bor — apply bo'lmaydi")
        try:
            hujjatlar = [d for d in yaml.safe_load_all(matn) if d]
        except yaml.YAMLError as e:
            h.xato("F008", nisbiy(y), 0, f"YAML sintaksis xatosi: {str(e)[:80]}")
            continue
        if not hujjatlar:
            h.xato("F008", nisbiy(y), 0, "bo'sh YAML fayl")
        for d in hujjatlar:
            if not isinstance(d, dict):
                h.xato("F008", nisbiy(y), 0, "yuqori daraja obyekt emas")
            elif y.name == "kustomization.yaml":
                if d.get("kind") != "Kustomization":
                    h.xato("F008", nisbiy(y), 0, "kind: Kustomization bo'lishi kerak")
            elif not ("apiVersion" in d and "kind" in d):
                h.xato("F008", nisbiy(y), 0, "apiVersion yoki kind yo'q")


def f009_image_qadalgan(h: Hisobot) -> None:
    """F009 — amaliyot/ dagi image va FROM versiya bilan qadalgan bo'lsin.

    `image: nginx` bugun bir versiyani, ertaga boshqasini tortadi — dars
    takrorlanmaydigan bo'lib qoladi.
    """
    for f in sorted(ILDIZ.rglob("amaliyot/**/*")):
        if not f.is_file() or f.name == "package-lock.json":
            continue
        if f.suffix not in {".yaml", ".yml", ""} and f.name != "Dockerfile":
            continue
        for i, qator in enumerate(f.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
            m = re.match(r"^\s*(?:-\s*)?image:\s*[\"']?([^\s\"']+)", qator)
            if not m:
                m = re.match(r"^\s*FROM\s+([^\s]+)", qator, re.I)
            if not m:
                continue
            ref = m.group(1)
            if ref.startswith(("$", "{")):
                continue
            oxirgi = ref.rsplit("/", 1)[-1]
            if ":" not in oxirgi and "@" not in oxirgi:
                h.xato("F009", nisbiy(f), i, f"image versiyasiz: {ref}")
            elif oxirgi.endswith(":latest"):
                # `latest` texnik jihatdan teg, lekin u ham har safar boshqa
                # image tortishi mumkin — shuning uchun ogohlantiramiz.
                h.ogoh("F009", nisbiy(f), i,
                       f"`:latest` tegi — aniq versiya afzalroq: {ref}")


def f010_amaliyot_moslik(h: Hisobot) -> None:
    """F010 — amaliyot/<nom>/ papkasi shu nomdagi darsga mos kelsin."""
    for amaliyot in sorted(ILDIZ.rglob("amaliyot")):
        if not amaliyot.is_dir() or CHETLAB & set(amaliyot.relative_to(ILDIZ).parts):
            continue
        bolim = amaliyot.parent
        darslar = {p.stem for p in bolim.glob("*.md")}
        for ichki in amaliyot.iterdir():
            if not ichki.is_dir() or ichki.name in darslar:
                continue
            # Ilova manbasi (Dockerfile / package.json bor) — bu dars laboratoriyasi
            # emas, shuning uchun nomi darsga mos kelishi shart emas.
            if (ichki / "Dockerfile").exists() or (ichki / "package.json").exists():
                continue
            h.ogoh("F010", nisbiy(ichki), 0,
                   f"'{ichki.name}.md' darsi yo'q — papka nomi darsga mos emas")


def f011_shablon(h: Hisobot) -> None:
    """F011 — dars USLUB.md dagi shablon bo'limlarini tutadimi (ogohlantirish)."""
    kerakli = {
        "🎯 maqsad": r">\s*🎯",
        "❓ Savol-Javob": r"^##\s*❓",
        "📖 Asosiy atamalar": r"^##\s*📖",
        "🔗 Manbalar": r"^##\s*🔗",
        "🧪 topshiriqlar": r"^##\s*🧪",
    }
    jami = defaultdict(int)
    darslar = 0
    for p in md_fayllar():
        n = nisbiy(p)
        if p.name == "README.md" or n.parts[0] in {"skriptlar", "rasmlar"}:
            continue
        if len(n.parts) < 2:
            continue
        darslar += 1
        matn = p.read_text(encoding="utf-8", errors="replace")
        yoq = [nom for nom, naqsh in kerakli.items()
               if not re.search(naqsh, matn, re.M)]
        for nom, naqsh in kerakli.items():
            if re.search(naqsh, matn, re.M):
                jami[nom] += 1
        if yoq:
            h.ogoh("F011", n, 0, "yo'q bo'limlar: " + ", ".join(yoq))
    if darslar:
        print(f"\nShablonga moslik ({darslar} ta darsdan):")
        for nom in kerakli:
            ulush = jami[nom]
            foiz = 100 * ulush // darslar
            print(f"  {nom:<22} {ulush:>3}/{darslar}  {'█' * (foiz // 5):<20} {foiz}%")


def f012_svg(h: Hisobot) -> None:
    """F012 — SVG sxemalar USLUB.md dagi tema qoidalariga mos bo'lsin."""
    for s in sorted(ILDIZ.rglob("*.svg")):
        if CHETLAB & set(s.relative_to(ILDIZ).parts):
            continue
        matn = s.read_text(encoding="utf-8", errors="replace")
        n = nisbiy(s)
        if re.search(r"<style[\s>]|@media|var\(--", matn):
            h.xato("F012", n, 0, "<style>/@media/var(--) — tema bo'yicha sinadi")
        if not re.search(r'<rect[^>]*\sx="0"[^>]*\sy="0"', matn):
            h.xato("F012", n, 0, "butun kanvasni qoplaydigan fon <rect> yo'q")
        if "<title" not in matn:
            h.ogoh("F012", n, 0, "<title> yo'q (ekran o'quvchi uchun)")
        if "<desc" not in matn:
            h.ogoh("F012", n, 0, "<desc> yo'q")


def f013_alt_matn(h: Hisobot) -> None:
    """F013 — rasmlarda mazmunli alt-matn bo'lsin."""
    yomon = {"alt text", "image", "rasm", "screenshot", "picture", ""}
    naqsh = re.compile(r"!\[([^\]]*)\]\(([^)\s]+)")
    for p in md_fayllar():
        if str(nisbiy(p)) in IMLO_OZOD:
            continue
        for i, qator in enumerate(kodsiz(p.read_text(encoding="utf-8", errors="replace")).splitlines(), 1):
            for alt, manzil in naqsh.findall(qator):
                if alt.strip().lower() in yomon:
                    h.xato("F013", nisbiy(p), i,
                           f"mazmunsiz alt-matn '{alt}' ({manzil})")


TEKSHIRUVLAR = {
    "F001": f001_blok_balansi,
    "F002": f002_blok_teglari,
    "F004": f004_belgilar,
    "F005": f005_sarlavhalar,
    "F006": f006_havolalar,
    "F007": f007_yetim_rasmlar,
    "F008": f008_amaliyot_yaml,
    "F009": f009_image_qadalgan,
    "F010": f010_amaliyot_moslik,
    "F011": f011_shablon,
    "F012": f012_svg,
    "F013": f013_alt_matn,
}


def main() -> int:
    p = argparse.ArgumentParser(description="k8s-education sifat tekshiruvi")
    p.add_argument("--qisqa", action="store_true", help="faqat xatolarni ko'rsatish")
    p.add_argument("--kod", help="bitta tekshiruvni ishga tushirish, masalan F002")
    argv = p.parse_args()

    h = Hisobot()
    # Haqiqiy fayl VA papka nomlari — imlo tekshiruvi ularga tegmaydi.
    # Masalan `Custom_obrazlar_yaratish` papkasi "obraz" so'zini saqlaydi,
    # lekin u qayta nomlanmagan, shuning uchun unga havolalar qonuniy.
    nomlar = {f.name for f in ILDIZ.rglob("*")}
    nomlar |= {f.stem for f in ILDIZ.rglob("*.md")}

    if argv.kod:
        kod = argv.kod.upper()
        if kod == "F003":
            f003_imlo(h, nomlar)
        elif kod in TEKSHIRUVLAR:
            TEKSHIRUVLAR[kod](h)
        else:
            sys.exit(f"noma'lum tekshiruv kodi: {kod}")
    else:
        f003_imlo(h, nomlar)
        for fn in TEKSHIRUVLAR.values():
            fn(h)

    return h.chop(qisqa=argv.qisqa)


if __name__ == "__main__":
    sys.exit(main())
