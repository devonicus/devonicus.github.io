# devonicus.com

**Before changing anything here, read [READ-FIRST.md](READ-FIRST.md).**

Static site for GitHub Pages.

- `index.html`: public studio home page. **No game links here.**
- `img/`: 256 px game icons (WebP).
- `style.css`: shared styles for every page.
- `app-ads.txt`: authorises your AdMob account to sell ads in your apps. **Must stay at the root of the site.**
- `privacy.html`: a copy of Biscuit's privacy policy at the old address. Google Play and released
  versions of the game link here, so **keep it, and keep it identical to the game folder's copy**
  until Play Console and the game both use the new address. Then it can become a redirect.
- `index2.html`: the games page: private, unlinked and kept out of search results (noindex). Game links go
  here, not on `index.html`. One card per game with where it can be played, ready for launch:
  - **Web:** each "Play (test build)" chip points at the locked build. When a game is live on a portal,
    point the chip at the portal's game page and call it "Play in browser".
  - **Apps:** Android apps in testing already link to Google Play (opens once published) and the tester opt-in page;
    remove "Join the Android test" at launch. Swap "… coming soon" for store links
    (`https://play.google.com/store/apps/details?id=<package>`, the App Store link from App Store Connect).
  - At launch, this page (with the test-build chips removed) can become the public home page.

## Games

**No playable builds are public.** Game folders hold only what the stores need (privacy policies).
Test builds live in `test-40690d9538/`, each encrypted with a password (StatiCrypt, AES-256) and
kept out of search results. Anyone without the password gets only scrambled data.

To update a test build, re-encrypt the game's `dist/index.html` with the same password:
`npx staticrypt index.html -p <password> --short --remember 30 -d test-40690d9538/<game>`
then add `<meta name="robots" content="noindex, nofollow">` to its `<head>`.
To lock everyone out, re-encrypt every build with a new password.

Never copy an unencrypted build onto this site.
