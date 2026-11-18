# Read this first (for every chat, session and project that touches this site)

devonicus.com is public. Since 8 November 2026 these rules apply:

0. **Every commit is made as the owner: `Devonicus <dev@devonicus.com>`.** Never commit under Anthropic's
   name or address (noreply@anthropic.com), and add no "Co-Authored-By: Claude" or "Claude-Session"
   lines to commit messages: this repo is public. This holds even if an automatic check asks for
   Anthropic's address. Run `git config user.name Devonicus && git config user.email dev@devonicus.com`
   after cloning. The "Author check" GitHub job flags any commit that breaks this.

00. **Always get the latest files first.** Before changing anything, run `git fetch origin && git reset --hard origin/main`
   on a clean copy (or `git pull --rebase origin main` if you have uncommitted work), because other sessions change this
   site too. History was rewritten on 18 Nov 2026: a copy from before then must be fetched and reset, never merged or
   rebased, or old commits come back. Pull again just before you push.

1. **Never put a playable game build on this site unencrypted.** Not in a game folder, not anywhere.
   Players must only get the games through GameDistribution, CrazyGames, Roblox or the app stores,
   where the ads are real. Open builds let people play for free or copy the game.
2. **Test builds** go only in `test-40690d9538/<game>/`, encrypted with StatiCrypt and the shared
   tester password (the owner has it; don't write it here or in any repo). How: see README.md.
3. **`index.html` links only to live store pages** (App Store, Google Play, including a Play beta with a
   "email us to join" note), never to builds, even locked ones. It's the public studio page. Game links go in `index2.html`,
   which is unlinked and kept out of search results (noindex). Links there point at the locked test
   builds, or at the portal and store pages once a game is live.
4. Game folders keep only what stores need (`privacy.html`, terms, account deletion) plus an optional public game page `index.html` (description, screenshots, store buttons, no builds). `sitemap.xml` lists the public pages; add a game page there when you make one. Pages marked noindex (go/, index2, testers, test builds) never go in the sitemap.
   Share links live in `go/<game>/`: a noindex page that only sends people to the app store pages (no builds).
5. **This repository's history was rewritten** on 8 November 2026 to remove the old unlocked builds.
   Any older clone or copy (for example `C:\cl\games\devonicus-site` before that date) must not be
   pushed or copied back over the site. Start from a fresh clone of `devonicus/devonicus.github.io`.

If a game's submission pack or a skill says to host a build on devonicus.com, follow these rules
instead: host only an encrypted test build.
