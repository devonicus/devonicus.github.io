// config.json (plain, kept on the PC only) -> config.bin (signed, then sealed).
// node sign.mjs <key folder> <config.json> <out config.bin>
import nacl from 'tweetnacl';
import { readFileSync, writeFileSync } from 'node:fs';
import { join } from 'node:path';
const [dir, src, out] = process.argv.slice(2);
if (!out) throw new Error('usage: node sign.mjs <key folder> <config.json> <config.bin>');
const key = (n) => new Uint8Array(Buffer.from(readFileSync(join(dir, n), 'utf8').trim(), 'base64'));
const cfg = JSON.parse(readFileSync(src, 'utf8'));
if (cfg.v !== 1 || !cfg.issued || !cfg.stats) throw new Error('config needs v:1, issued and stats');
cfg.issued = new Date().toISOString();
const signed = nacl.sign(new TextEncoder().encode(JSON.stringify(cfg)), key('sign.secret.key'));
const nonce = nacl.randomBytes(24);
const sealed = nacl.secretbox(signed, nonce, key('box.key'));
const blob = new Uint8Array(nonce.length + sealed.length); blob.set(nonce); blob.set(sealed, 24);
writeFileSync(out, Buffer.from(blob).toString('base64'));
console.log('config.bin written, issued', cfg.issued);
