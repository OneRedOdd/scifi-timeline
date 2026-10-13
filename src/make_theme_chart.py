"""Draw charts/score_by_theme.png (square 'Score by theme' chart, used in the talk slides)
from data/predictions.csv. Score counts 'sort of' as half; only rows with scored = yes."""
import csv, os, collections
from PIL import Image, ImageDraw, ImageFont
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RP = lambda *a: os.path.join(REPO, *a)
FONT = '/usr/share/fonts/truetype/sand-box/google/Open Sans/OpenSans-VariableFont_wdth,wght.ttf'
def font(sz, bold=False):
    try:
        f = ImageFont.truetype(FONT, sz)
        try: f.set_variation_by_name('Bold' if bold else 'Regular')
        except Exception: pass
        return f
    except OSError:
        return ImageFont.truetype('DejaVuSans-Bold.ttf' if bold else 'DejaVuSans.ttf', sz)

rows_in = [r for r in csv.DictReader(open(RP('data', 'predictions.csv'), encoding='utf-8')) if r['scored'] == 'yes']
pts = {'came true': 1.0, 'sort of': 0.5, "didn't": 0.0}
by = collections.defaultdict(list)
for r in rows_in: by[r['theme']].append(r['verdict'])
overall = round(100 * sum(pts[r['verdict']] for r in rows_in) / len(rows_in), 1)
rows = sorted(((t, len(v), round(100 * sum(pts[x] for x in v) / len(v), 1), round(100 * v.count('came true') / len(v)))
               for t, v in by.items()), key=lambda r: -r[2])

W, H = 1736, 1672
BG = (11, 18, 32); FG = (230, 237, 245); MU = (138, 155, 180); Y = (255, 213, 79); C = (79, 195, 247); O = (255, 138, 101)
im = Image.new('RGB', (W, H), BG); d = ImageDraw.Draw(im)
d.text((60, 40), 'Score by theme', font=font(64, True), fill=FG)
d.text((60, 125), f'{len(rows_in)} scored predictions; score counts sort of as half', font=font(34), fill=MU)
x0, x1, top = 470, 1600, 230; rowh = (H - top - 170) // len(rows); scale = (x1 - x0) / 62
for v in range(0, 61, 10):
    xx = x0 + v * scale; d.line((xx, top, xx, top + rowh * len(rows)), fill=(30, 42, 64), width=2)
    d.text((xx, top + rowh * len(rows) + 10), str(v), font=font(28), fill=MU, anchor='ma')
for i, (nm, n, sc, ct) in enumerate(rows):
    yy = top + i * rowh + 16; bh = (rowh - 40) // 2
    d.text((x0 - 20, yy + bh - 4), nm, font=font(36, i == 0), fill=FG, anchor='rm')
    d.text((x0 - 20, yy + bh + 34), f'n = {n}', font=font(28), fill=MU, anchor='rm')
    d.rectangle((x0, yy, x0 + sc * scale, yy + bh), fill=Y)
    d.text((x0 + sc * scale + 14, yy + bh / 2), f'{sc:.1f}%', font=font(34, True), fill=FG, anchor='lm')
    d.rectangle((x0, yy + bh + 4, x0 + max(ct * scale, 2), yy + 2 * bh + 4), fill=C)
    d.text((x0 + ct * scale + 14, yy + bh * 1.5 + 4), f'{ct}%', font=font(28), fill=MU, anchor='lm')
xa = x0 + overall * scale
for yy in range(top - 20, top + rowh * len(rows), 24): d.line((xa, yy, xa, yy + 12), fill=O, width=4)
d.text((xa + 12, top - 34), f'all themes {overall:.1f}%', font=font(30), fill=O)
ly = H - 95
d.rectangle((60, ly, 96, ly + 30), fill=Y); d.text((110, ly + 15), 'score (sort of = half)', font=font(30), fill=FG, anchor='lm')
d.rectangle((560, ly, 596, ly + 30), fill=C); d.text((610, ly + 15), '% came true outright', font=font(30), fill=FG, anchor='lm')
d.text((60, H - 40), 'Source: predictions.csv, stats_summary.md. Most themes have n < 30.', font=font(24), fill=MU)
for out in (RP('charts', 'score_by_theme.png'), RP('docs', 'charts', 'score_by_theme.png')):
    im.save(out)
print('wrote charts/score_by_theme.png and docs/charts/score_by_theme.png')
