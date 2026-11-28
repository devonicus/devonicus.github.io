// Makes the remote-config keys once. Writes them to the folder given (never prints them).
// node keygen.mjs C:\cl\keys\bonus
import nacl from 'tweetnacl';
import { writeFileSync, existsSync, mkdirSync } from 'node:fs';
import { join } from 'node:path';
const dir = process.argv[2];
if (!dir) throw new Error('usage: node keygen.mjs <key folder>');
if (existsSync(join(dir, 'sign.secret.key'))) throw new Error('keys already exist there; not overwriting');
mkdirSync(dir, { recursive: true });
const sign = nacl.sign.keyPair();
const box = nacl.randomBytes(32);
const b64 = (u) => Buffer.from(u).toString('base64');
writeFileSync(join(dir, 'sign.secret.key'), b64(sign.secretKey));
writeFileSync(join(dir, 'box.key'), b64(box));
// pieces for the apps: public key plus the box key split into 4 xor shares
const shares = [nacl.randomBytes(32), nacl.randomBytes(32), nacl.randomBytes(32)];
const last = box.map((b, i) => b ^ shares[0][i] ^ shares[1][i] ^ shares[2][i]);
shares.push(last);
writeFileSync(join(dir, 'app-keys.ts'),
`// remote-config keys for the games (private: copy into each game's src/platform, never into a public repo)
export const RC_PUBLIC = '${b64(sign.publicKey)}';
export const RC_PIECES = [${shares.map((s) => `'${b64(s)}'`).join(', ')}];
`);
console.log('keys written to', dir);
