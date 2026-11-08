# Read this first (for every chat, session and project that touches this site)

devonicus.com is public. Since 8 November 2026 these rules apply:

1. **Never put a playable game build on this site unencrypted.** Not in a game folder, not anywhere.
   Players must only get the games through GameDistribution, CrazyGames, Roblox or the app stores,
   where the ads are real. Open builds let people play for free or copy the game.
2. **Test builds** go only in `test-40690d9538/<game>/`, encrypted with StatiCrypt and the shared
   tester password (the owner has it; don't write it here or in any repo). How: see README.md.
3. **`index.html` has no game links.** It's the studio page only. Game links go in `index2.html`,
   which is unlinked and kept out of search results (noindex). Links there point at the locked test
   builds, or at the portal and store pages once a game is live.
4. Game folders keep only what stores need: `privacy.html` (Google Play and Apple link to these).
5. **This repository's history was rewritten** on 8 November 2026 to remove the old unlocked builds.
   Any older clone or copy (for example `C:\cl\games\devonicus-site` before that date) must not be
   pushed or copied back over the site. Start from a fresh clone of `devonicus/devonicus.github.io`.

If a game's submission pack or a skill says to host a build on devonicus.com, follow these rules
instead: host only an encrypted test build.
