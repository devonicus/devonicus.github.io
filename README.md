# devonicus.com

Static site for GitHub Pages.

- `index.html`: public studio home page. **No game links here.**
- `img/`: 256 px game icons (WebP).
- `style.css`: shared styles for every page.
- `app-ads.txt`: authorises your AdMob account to sell ads in your apps. **Must stay at the root of the site.**
- `privacy.html`: a copy of Biscuit's privacy policy at the old address. Google Play and released
  versions of the game link here, so **keep it, and keep it identical to the game folder's copy**
  until Play Console and the game both use the new address. Then it can become a redirect.
- `index2.html`: the games list: private, unlinked and kept out of search results (noindex). Game links go here, not on `index.html`.

## Games

| Folder | What's there | Source |
|---|---|---|
| `nap-spots/` | playable web build, privacy policy | `devonicus/nap-spots` `dist/index.html` |
| `harbour-knots/` | playable web build, privacy policy | `devonicus/harbour-knots` `dist/index.html` |
| `round-the-houses/` | playable web build, privacy policy | `devonicus/round-the-houses` `dist/index.html` |
| `shelf-life/` | playable web build, privacy policy | `devonicus/shelf-life` `dist/index.html` |
| `loop-line/` | playable web build | `devonicus/loop-line` `dist/index.html` |
| `biscuits-bookshop-mysteries/` | game page, icon, privacy policy | |
| `arrow-knots/`, `tilt/` | redirects only (renamed / retired games) | |

The hosted builds are the local target (no portal SDK; rewarded "ads" are simulated). To update one,
rebuild the game and copy its `dist/index.html` over the folder's `index.html`.

The Roblox games link straight to their Roblox pages (place ids are in each game's `docs/LIVE.md`).
