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

**No playable builds are public.** Game folders hold only what the stores need (privacy policies).
Test builds live in `test-40690d9538/`, each encrypted with a password (StatiCrypt, AES-256) and
kept out of search results. Anyone without the password gets only scrambled data.

To update a test build, re-encrypt the game's `dist/index.html` with the same password:
`npx staticrypt index.html -p <password> --short --remember 30 -d test-40690d9538/<game>`
then add `<meta name="robots" content="noindex, nofollow">` to its `<head>`.
To lock everyone out, re-encrypt every build with a new password.

Never copy an unencrypted build onto this site.
