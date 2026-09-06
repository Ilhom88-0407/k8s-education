"""sxema.py — darslik sxemalarini chizish uchun kichik SVG kutubxonasi.

Nima uchun kutubxona kerak? Yigirmata sxemani qo'lda yozganda ranglar,
shriftlar va otstuplar sekin-asta bir-biridan uzoqlashadi. Bu yerda ular
bir joyda belgilangan.

USLUB.md dagi qoidalarga amal qiladi:
  * har sxema o'z fon to'rtburchagini olib yuradi — GitHub'ning yorug'
    va qorong'i temasida bir xil o'qiladi;
  * <style>, @media, var(--...) va tashqi shrift ishlatilmaydi;
  * har sxemada <title> va <desc> bo'ladi (ekran o'quvchilar uchun).

Ishlatish:
    from sxema import Sxema, PALITRA
    s = Sxema(720, 400, "Sarlavha", "Tavsif")
    s.quti(40, 40, 200, 60, "kube-apiserver", "izoh", rol="control")
    s.strelka(240, 70, 400, 70, "so'rov")
    s.saqla("rasmlar/misol.svg")
"""
from __future__ import annotations

from html import escape
from pathlib import Path

SHRIFT = "system-ui,-apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif"
MONO = "ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"

#: Rol -> (fon, chegara). USLUB.md dagi jadval bilan bir xil.
PALITRA = {
    "kanvas":   ("#FBFBFA", "#D8D6D1"),
    "oq":       ("#FFFFFF", "#D8D6D1"),
    "control":  ("#DCE9F7", "#2C6FB5"),   # control plane, apiserver
    "pod":      ("#DDF0E5", "#2A7D53"),   # pod, workload
    "tarmoq":   ("#E5E2F7", "#5B4FBE"),   # service, tarmoq
    "ogoh":     ("#FBEBD2", "#B5761A"),   # ogohlantirish
    "xato":     ("#F8DFDF", "#B33A3A"),   # xato, nosozlik
}
MATN = "#1A1A18"
MATN2 = "#5C5A55"


class Sxema:
    """Bitta SVG sxema. Elementlar chaqirilgan tartibda ustma-ust chiziladi."""

    def __init__(self, kengligi: int, balandligi: int, sarlavha: str,
                 tavsif: str, fon: str = "kanvas") -> None:
        self.w, self.h = kengligi, balandligi
        self.sarlavha, self.tavsif = sarlavha, tavsif
        self.qismlar: list[str] = []
        f, c = PALITRA[fon]
        self.qismlar.append(
            f'<rect x="0" y="0" width="{kengligi}" height="{balandligi}" rx="14" '
            f'fill="{f}" stroke="{c}" stroke-width="1"/>')

    # ---------------------------------------------------------------- matn
    def matn(self, x: int, y: int, s: str, *, olcham: float = 12.5,
             qalin: bool = False, rang: str = MATN, markaz: bool = True,
             mono: bool = False) -> "Sxema":
        """Bitta qator matn. `markaz=True` bo'lsa x — matnning markazi."""
        atrlar = [f'x="{x}"', f'y="{y}"']
        if markaz:
            atrlar.append('text-anchor="middle"')
        atrlar.append(f'font-size="{olcham}"')
        if qalin:
            atrlar.append('font-weight="600"')
        if mono:
            atrlar.append(f'font-family="{MONO}"')
        atrlar.append(f'fill="{rang}"')
        self.qismlar.append(f'<text {" ".join(atrlar)}>{escape(s)}</text>')
        return self

    def sarlavha_matni(self, x: int, y: int, bosh: str, izoh: str = "") -> "Sxema":
        """Sxemaning yuqori chap burchagidagi sarlavha va izoh."""
        self.matn(x, y, bosh, olcham=20, qalin=True, markaz=False)
        if izoh:
            self.matn(x, y + 23, izoh, olcham=12.5, rang=MATN2, markaz=False)
        return self

    # ---------------------------------------------------------------- shakl
    def quti(self, x: int, y: int, w: int, h: int, bosh: str, *qatorlar: str,
             rol: str = "oq", punktir: bool = False, radius: int = 8,
             bosh_olcham: float = 13.5, mono: bool = False,
             qator_olcham: float = 11) -> "Sxema":
        """Sarlavhali to'rtburchak; ixtiyoriy izoh qatorlari sarlavha ostida.

        Sarlavha va izohlar bitta blok sifatida qutining o'rtasiga
        joylashtiriladi — shuning uchun qancha qator qo'shsangiz ham
        ular bir-birining ustiga tushmaydi.
        """
        f, c = PALITRA[rol]
        chiziq = ' stroke-dasharray="5 3"' if punktir else ""
        self.qismlar.append(
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{radius}" '
            f'fill="{f}" stroke="{c}" stroke-width="1.5"{chiziq}/>')
        mx = x + w // 2
        qatorlar = tuple(q for q in qatorlar if q)
        qator_balandligi = qator_olcham + 4
        blok = bosh_olcham + len(qatorlar) * qator_balandligi
        bosh_y = y + (h - blok) / 2 + bosh_olcham
        self.matn(mx, round(bosh_y), bosh, olcham=bosh_olcham, qalin=True, mono=mono)
        for i, q in enumerate(qatorlar):
            self.matn(mx, round(bosh_y + (i + 1) * qator_balandligi + 2), q,
                      olcham=qator_olcham, rang=MATN2)
        return self

    def panel(self, x: int, y: int, w: int, h: int, bosh: str,
              *, rol: str = "control") -> "Sxema":
        """Ichiga boshqa qutilar joylanadigan katta ramka."""
        f, c = PALITRA[rol]
        # Panel foni asosiy rangdan ochiqroq bo'lsin: oq bilan aralashtiramiz
        ochiq = _ochiqlash(f, 0.55)
        self.qismlar.append(
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" '
            f'fill="{ochiq}" stroke="{c}" stroke-width="1.5"/>')
        self.matn(x + 16, y + 24, bosh, olcham=13.5, qalin=True, rang=c, markaz=False)
        return self

    # -------------------------------------------------------------- strelka
    def strelka(self, x1: int, y1: int, x2: int, y2: int, yorliq: str = "",
                *, rang: str = MATN2, ikki_tomon: bool = False,
                punktir: bool = False, yorliq_ofset: int = -8) -> "Sxema":
        """To'g'ri strelka. `ikki_tomon` ikkala uchida ham uchi bo'ladi."""
        marker = _marker_id(rang)
        chiziq = ' stroke-dasharray="5 4"' if punktir else ""
        boshi = f' marker-start="url(#{marker})"' if ikki_tomon else ""
        self.qismlar.append(
            f'<path d="M {x1} {y1} L {x2} {y2}" stroke="{rang}" stroke-width="2" '
            f'fill="none"{chiziq}{boshi} marker-end="url(#{marker})"/>')
        if yorliq:
            self.matn((x1 + x2) // 2, (y1 + y2) // 2 + yorliq_ofset, yorliq,
                      olcham=11, rang=rang)
        return self

    def egri(self, d: str, yorliq: str = "", *, rang: str = MATN2,
             yorliq_xy: tuple[int, int] | None = None) -> "Sxema":
        """Ixtiyoriy egri chiziq (SVG path `d` sintaksisi)."""
        self.qismlar.append(
            f'<path d="{d}" stroke="{rang}" stroke-width="2" fill="none" '
            f'marker-end="url(#{_marker_id(rang)})"/>')
        if yorliq and yorliq_xy:
            self.matn(yorliq_xy[0], yorliq_xy[1], yorliq, olcham=11, rang=rang)
        return self

    def ajratgich(self, x1: int, y: int, x2: int) -> "Sxema":
        self.qismlar.append(
            f'<line x1="{x1}" y1="{y}" x2="{x2}" y2="{y}" '
            f'stroke="{PALITRA["kanvas"][1]}" stroke-width="1"/>')
        return self

    # ---------------------------------------------------------------- saqla
    def svg(self) -> str:
        ranglar = {MATN2, MATN} | {c for _, c in PALITRA.values()}
        markerlar = "\n".join(
            f'    <marker id="{_marker_id(r)}" viewBox="0 0 10 10" refX="9" refY="5"\n'
            f'            markerWidth="7" markerHeight="7" orient="auto-start-reverse">\n'
            f'      <path d="M 0 0 L 10 5 L 0 10 z" fill="{r}"/>\n'
            f'    </marker>' for r in sorted(ranglar))
        tana = "\n  ".join(self.qismlar)
        return (
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.w} {self.h}" '
            f'width="{self.w}"\n'
            f'     role="img" aria-labelledby="sarlavha izoh" font-family="{SHRIFT}">\n'
            f'  <title id="sarlavha">{escape(self.sarlavha)}</title>\n'
            f'  <desc id="izoh">{escape(self.tavsif)}</desc>\n'
            f'  <defs>\n{markerlar}\n  </defs>\n'
            f'  {tana}\n</svg>\n')

    def saqla(self, yol: str | Path) -> Path:
        p = Path(yol)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(self.svg(), encoding="utf-8")
        return p


def _marker_id(rang: str) -> str:
    return "ok" + rang.lstrip("#")


def _ochiqlash(hex_rang: str, ulush: float) -> str:
    """Rangni oq bilan aralashtirib ochiqroq qiladi (panel foni uchun)."""
    r, g, b = (int(hex_rang[i:i + 2], 16) for i in (1, 3, 5))
    aral = lambda v: round(v + (255 - v) * ulush)
    return f"#{aral(r):02X}{aral(g):02X}{aral(b):02X}"
