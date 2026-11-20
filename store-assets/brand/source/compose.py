"""Lay out the Devonicus social set from the rendered mark and wordmark.
usage: python3 compose.py SRC_DIR OUT_DIR   (SRC_DIR holds mark-tile.png, mark-bare.png, wordmark.png)"""
import sys, os, random
from PIL import Image, ImageDraw, ImageFilter, ImageFont

src, out = sys.argv[1], sys.argv[2]
os.makedirs(out, exist_ok=True)
FONT = '/home/claude/brand/fredoka-700.ttf'
TEAL_DEEP, TEAL, CREAM, BRASS = (14, 38, 44), (24, 70, 80), (255, 248, 232), (242, 179, 61)

tile = Image.open(f'{src}/mark-tile.png').convert('RGBA')
bare = Image.open(f'{src}/mark-bare.png').convert('RGBA')
word = Image.open(f'{src}/wordmark.png').convert('RGBA')

def crop_alpha(im, pad=0):
    x0, y0, x1, y1 = im.getbbox()
    return im.crop((max(0, x0 - pad), max(0, y0 - pad), min(im.width, x1 + pad), min(im.height, y1 + pad)))

bare, word, tile = crop_alpha(bare, 8), crop_alpha(word, 8), crop_alpha(tile, 4)

def backdrop(w, h, centre=(0.5, 0.42), seed=7, tiles=True):
    """Deep teal with a soft lift behind the logo, faint scattered tiles and fine grain."""
    bg = Image.new('RGB', (w, h), TEAL_DEEP)
    glow = Image.new('L', (w, h), 0)
    r = int(max(w, h) * 0.55)
    cx, cy = int(w * centre[0]), int(h * centre[1])
    ImageDraw.Draw(glow).ellipse((cx - r, cy - r * 0.8, cx + r, cy + r * 0.8), fill=255)
    glow = glow.filter(ImageFilter.GaussianBlur(r * 0.45))
    bg = Image.composite(Image.new('RGB', (w, h), TEAL), bg, glow)
    if tiles:
        layer = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(layer)
        rnd = random.Random(seed)
        for _ in range(int(w * h / 90000)):
            s = rnd.randint(int(h * 0.025), int(h * 0.06)); x = rnd.randint(-s, w); y = rnd.randint(-s, h)
            col = rnd.choice([(255, 248, 232, 10), (242, 179, 61, 12), (168, 50, 74, 12)])
            d.rounded_rectangle((x, y, x + s, y + s), radius=s * 0.28, fill=col)
        bg = Image.alpha_composite(bg.convert('RGBA'), layer.filter(ImageFilter.GaussianBlur(1.2))).convert('RGB')
    noise = Image.effect_noise((w, h), 9).convert('RGB')
    return Image.blend(bg, noise, 0.025)

def fit(im, max_w, max_h):
    k = min(max_w / im.width, max_h / im.height)
    return im.resize((max(1, round(im.width * k)), max(1, round(im.height * k))), Image.LANCZOS)

def paste_c(base, im, cx, cy):
    base.alpha_composite(im, (round(cx - im.width / 2), round(cy - im.height / 2)))

# profile picture: bare mark on the backdrop, sized to sit well inside the circle crop
for name, size in (('profile-800.png', 800), ('profile-400.png', 400)):
    p = backdrop(size, size, centre=(0.5, 0.45), tiles=False).convert('RGBA')
    m = fit(bare, size * 0.64, size * 0.64)
    paste_c(p, m, size / 2, size / 2)
    p.convert('RGB').save(f'{out}/{name}', optimize=True)

# icon versions of the tile mark (app-icon style, transparent corners)
fit(tile, 1024, 1024).save(f'{out}/mark-tile-1024.png', optimize=True)
fit(bare, 1024, 1024).save(f'{out}/mark-1024.png', optimize=True)
fit(word, 2400, 2400).save(f'{out}/wordmark-2400.png', optimize=True)
fit(tile, 150, 150).save(f'{out}/youtube-watermark-150.png', optimize=True)

# YouTube banner: 2560x1440, everything that matters inside the 1546x423 centre safe area
W, H, SW, SH = 2560, 1440, 1546, 423
b = backdrop(W, H, centre=(0.5, 0.5)).convert('RGBA')
top, left = (H - SH) // 2, (W - SW) // 2
m = fit(bare, SH * 0.84, SH * 0.84)
wm = fit(word, (SW - m.width - 70) * 0.86, SH * 0.46)
f = ImageFont.truetype(FONT, int(SH * 0.13))
tag = 'Cosy puzzle and mystery games for phones'
tw = f.getlength(tag)
block_w = m.width + 70 + max(wm.width, tw)
x0 = (W - block_w) / 2
paste_c(b, m, x0 + m.width / 2, H / 2)
tx = x0 + m.width + 70
b.alpha_composite(wm, (round(tx), round(H / 2 - wm.height * 0.78)))
ImageDraw.Draw(b).text((tx + wm.height * 0.06, H / 2 + wm.height * 0.38), tag, font=f, fill=CREAM + (235,))
b.convert('RGB').save(f'{out}/youtube-banner-2560x1440.png', optimize=True)

# guide copy with the safe areas drawn, for checking only
g = b.copy(); d = ImageDraw.Draw(g)
d.rectangle((left, top, left + SW, top + SH), outline=(255, 0, 0, 255), width=4)  # all devices
d.rectangle(((W - 2560) // 2, (H - 423) // 2, (W + 2560) // 2, (H + 423) // 2), outline=(0, 255, 0, 255), width=3)  # desktop max
g.convert('RGB').resize((1280, 720)).save(f'{out}/_check-banner.jpg', quality=88)
print('ok', m.size, wm.size, round(tw))
