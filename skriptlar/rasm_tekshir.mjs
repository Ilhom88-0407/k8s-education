/**
 * rasm_tekshir.mjs — SVG sxemalarni sifat tekshiruvidan o'tkazadi.
 *
 * Har bir *.svg faylni Chromium'da ikki marta ochadi: GitHub'ning yorug'
 * (#ffffff) va qorong'i (#0d1117) fonida. Natijani yonma-yon PNG qilib
 * saqlaydi, shunda sxema ikkala temada ham o'qilishini ko'z bilan
 * tekshirish mumkin bo'ladi.
 *
 * Bu qurilish (build) bosqichi EMAS — repoga PNG qo'shilmaydi. Faqat
 * tekshiruv vositasi.
 *
 * Ishlatish:  node skriptlar/rasm_tekshir.mjs [chiqish-papkasi]
 */
import { createRequire } from 'node:module';
import { readdirSync, statSync, mkdirSync, readFileSync } from 'node:fs';
import { execSync } from 'node:child_process';
import { join, relative } from 'node:path';

// Playwright global o'rnatilgan bo'lishi mumkin (npm i -g playwright), shuning
// uchun ESM import o'rniga uni global papkadan qidiramiz.
const require = createRequire(import.meta.url);
let chromium;
try {
  ({ chromium } = require('playwright'));
} catch {
  const global = execSync('npm root -g', { encoding: 'utf8' }).trim();
  ({ chromium } = require(join(global, 'playwright')));
}

const ILDIZ = process.cwd();
const CHIQISH = process.argv[2] ?? '/tmp/svg-tekshiruv';
const FONLAR = { yorug: '#ffffff', qorongi: '#0d1117' };

/** Repo bo'ylab barcha .svg fayllarni rekursiv topadi (.git dan tashqari). */
function svgTop(papka, natija = []) {
  for (const nom of readdirSync(papka)) {
    if (nom === '.git' || nom === 'node_modules') continue;
    const yol = join(papka, nom);
    if (statSync(yol).isDirectory()) svgTop(yol, natija);
    else if (nom.endsWith('.svg')) natija.push(yol);
  }
  return natija;
}

const fayllar = svgTop(ILDIZ);
if (fayllar.length === 0) {
  console.log('SVG fayl topilmadi.');
  process.exit(0);
}

mkdirSync(CHIQISH, { recursive: true });
const brauzer = await chromium.launch();
let ogohlantirish = 0;

for (const fayl of fayllar) {
  const nisbiy = relative(ILDIZ, fayl);
  const matn = readFileSync(fayl, 'utf8');

  // Statik tekshiruvlar: USLUB.md dagi qoidalarga mos keladimi?
  const muammolar = [];
  if (/<style[\s>]|@media|var\(--/.test(matn))
    muammolar.push('<style>/@media/var(--) ishlatilgan — tema bo\'yicha sinadi');
  if (!/<title[\s>]/.test(matn)) muammolar.push('<title> yo\'q (ekran o\'quvchi uchun)');
  if (!/<desc[\s>]/.test(matn)) muammolar.push('<desc> yo\'q');
  if (!/<rect[^>]*\sx="0"[^>]*\sy="0"/.test(matn))
    muammolar.push('butun kanvasni qoplaydigan fon <rect> yo\'q — qorong\'i temada ko\'rinmaydi');

  for (const [nom, fon] of Object.entries(FONLAR)) {
    const sahifa = await brauzer.newPage();
    await sahifa.setContent(
      `<body style="margin:0;padding:24px;background:${fon}">${matn}</body>`,
      { waitUntil: 'load' },
    );
    const el = await sahifa.$('svg');
    await el.screenshot({ path: join(CHIQISH, `${nisbiy.replace(/[\/\\]/g, '_')}.${nom}.png`) });
    await sahifa.close();
  }

  if (muammolar.length) {
    ogohlantirish++;
    console.log(`\n  ${nisbiy}`);
    for (const m of muammolar) console.log(`     ${m}`);
  } else {
    console.log(`  ${nisbiy}`);
  }
}

await brauzer.close();
console.log(`\n${fayllar.length} ta SVG tekshirildi, ${ogohlantirish} tasida muammo bor.`);
console.log(`Skrinshotlar: ${CHIQISH}`);
process.exit(ogohlantirish > 0 ? 1 : 0);
