"""Flat Devonicus mark: a brass D with a cranberry tile in its counter.
Writes square 1024 SVGs (unmasked, no baked effects) into the current folder; render.mjs turns them into PNGs."""
D = open('/home/claude/brand/D_path.txt').read()
TEAL, BRASS, CRAN, CREAM = '#18333a', '#f2b33d', '#a8324a', '#fffdf6'
GX0, GX1, GY0, GY1 = 28, 641, -8, 692           # glyph bounds, font units
CX, CY, CW = 325, 341, 150                       # counter centre and tile size, font units


def mark(h=600, cx=512, cy=512, letter=BRASS, tile=CRAN, knock=False):
    """The D (glyph height h px) centred on (cx, cy), with its counter tile."""
    s = h / (GY1 - GY0)
    tx = cx - (GX0 + GX1) / 2 * s
    ty = cy + (GY0 + GY1) / 2 * s
    w = CW * s; px, py = tx + CX * s, ty - CY * s
    rect = f'<rect x="{px - w / 2:.1f}" y="{py - w / 2:.1f}" width="{w:.1f}" height="{w:.1f}" rx="{w * 0.26:.1f}" fill="{tile}"/>'
    glyph = f'<path d="{D}" fill="{letter}" transform="translate({tx:.2f} {ty:.2f}) scale({s:.5f} {-s:.5f})"/>'
    if knock:   # one-colour version: tile cut out of nothing, drawn as letter colour inside the counter
        return glyph + rect.replace(f'fill="{tile}"', f'fill="{letter}"')
    return glyph + rect


def svg(body, bg=None, size=1024):
    back = f'<rect width="{size}" height="{size}" fill="{bg}"/>' if bg else ''
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024" width="{size}" height="{size}">{back}{body}</svg>\n'


files = {
    'devonicus-mark.svg': svg(mark(), TEAL),                       # master: brass D on teal, square, unmasked
    'icon-foreground.svg': svg(mark()),                            # icon layer 1 (transparent)
    'icon-background.svg': svg('', TEAL),                          # icon layer 2
    'devonicus-mark-mono-cream.svg': svg(mark(letter=CREAM, knock=True)),   # one colour, for watermarks on dark
    'devonicus-mark-mono-teal.svg': svg(mark(letter=TEAL, knock=True)),     # one colour, for light backgrounds
    'favicon.svg': svg(mark(h=760), TEAL),                          # tighter crop for 16-48 px
}
for name, text in files.items():
    open(name, 'w').write(text)
print('\n'.join(files))
