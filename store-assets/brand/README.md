Devonicus brand set (20 Nov 2026), rendered in Blender Cycles. Colours: teal #18333a / #124650, brass #f2b33d, cranberry #a8324a, cream #fffdf6. Wordmark font: Fredoka Bold (SIL Open Font License).
- mark-1024.png: the brass D on its own (transparent)
- mark-tile-1024.png: the D on the rounded teal tile (transparent corners)
- profile-800.png / profile-400.png: social profile picture, circle-crop safe
- wordmark-2400.png: "Devonicus" (transparent)
- youtube-banner-2560x1440.png: logo and tagline inside YouTube's 1546x423 safe area
- youtube-watermark-150.png: YouTube video watermark

Source: `source/mark.py` (Blender Cycles scene: `python3 mark.py OUT.png SIZE SAMPLES tile|bare|word [GEM_X GEM_Y]`; final renders used 1600px at 256 samples with GEM_X 0.03, and the wordmark 3000px at 128) and `source/compose.py` (profile pictures, banner, watermark). Needs `pip install bpy` and Fredoka Bold (shelf-life `studio/fonts/fredoka-700.ttf`); fix the font path at the top of each script.

## Flat master (20 Nov 2026), use this for icons, favicons and watermarks
`flat/` holds the vector master: a brass D with a cranberry tile in its counter on teal, drawn from Fredoka Bold's real outline. Apple's icon guidance asks for flat, square, unmasked vector layers with no baked bevels or highlights, so the 3D render above is for banners and hero art only.
- `devonicus-mark.svg` / `-1024.png`: the master (square, unmasked)
- `icon-foreground.svg` and `icon-background.svg` (+ 1024 PNGs): icon layers
- `devonicus-mark-mono-cream.svg` / `-mono-teal.svg`: one-colour versions
- `favicon.svg`, `favicon.ico` (16/32/48), `favicon-16/32/48/180/192/512.png`
- `youtube-watermark-mono-150.png`: the one-colour watermark
Rebuild with `source/make_flat.py` then `source/render.mjs` (Playwright Chromium).
