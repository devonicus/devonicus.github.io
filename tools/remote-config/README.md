# Remote config tools

Makes `r/config.bin`, the signed and sealed settings file the games read (statistics switch and bonus codes). Spec: project doc "Bonus links - spec".

- `npm install` once.
- `node keygen.mjs C:\cl\keys\bonus` once (never prints keys; refuses to overwrite).
- Edit `config.json` on the PC only (start from `config.example.json`; never commit it), then
  `node sign.mjs C:\cl\keys\bonus config.json ..\..\r\config.bin` and commit `r/config.bin`.
- Games: copy `open.ts` and the private `app-keys.ts` from the key folder.
