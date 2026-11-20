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

## Clip end cards (20 Nov 2026)
`endcards/card-<game>-social.png` (icon, name, "Free to play", search prompt, Devonicus mark) and `card-<game>-store.png` (icon, name and the mark only), 1080x1920 with transparency. No store or platform names: the owner's no-trademarks rule, and Apple and Google don't allow prices or calls to action in their own preview videos (use the store card there).
- Make a card: `node source/endcard.mjs OUT.png "<Game>" ICON.png social|store` (Fredoka Bold, flat mono mark).
- Put it on a clip: `sh source/apply_endcard.sh IN.mp4 CARD.png OUT.mp4 [3]` replaces the last 3 s with the card over a blurred still from just before them, keeping the audio and length (cuts 0.1 s early so an old baked-in card never shows).

## Text-free event art template (20 Nov 2026)
`source/event_art.py` renders one hero model (a game's .glb, or `demo`) on a backdrop in the game's colour, lit by a CC0 Poly Haven HDRI plus a key light from the upper left, into three text-free images: `-card-1920x1080` (App Store event card and Google Play promotional content), `-details-1080x1920` (App Store event details page) and `-feature-1024x500` (Play feature graphic). The subject is framed inside Play's promo safe zone (15% top, 20% left/right/bottom), so the same master passes both stores and no title ever needs painting out.
- `python3 event_art.py OUT_PREFIX HERO.glb|demo HDRI.hdr "#2c5a63" 256` (add `0.4` at the end for a quick preview)
- HDRI (CC0, no attribution needed): `curl -o studio_small_08_2k.hdr https://dl.polyhaven.org/file/ph-assets/HDRIs/hdr/2k/studio_small_08_2k.hdr`
- Export each game's hero (festive products, characters) to .glb from its own `studio/art` Blender scripts; check the card with the safe box drawn on before uploading.
