// Reference reader for the games (copy into src/platform/remote-config.ts).
// Needs tweetnacl; RC_PUBLIC and RC_PIECES come from the private app-keys.ts.
import nacl from 'tweetnacl';
import { RC_PUBLIC, RC_PIECES } from './app-keys';

const bytes = (s: string) => Uint8Array.from(atob(s), (c) => c.charCodeAt(0));

function boxKey(): Uint8Array {
  const parts = RC_PIECES.map(bytes);
  return parts[0].map((_, i) => parts.reduce((x, p) => x ^ p[i], 0));
}

/** Returns the config, or null if the file was tampered with or sealed with other keys. */
export function openConfig(blob: string): any | null {
  try {
    const all = bytes(blob.trim());
    const signed = nacl.secretbox.open(all.subarray(24), all.subarray(0, 24), boxKey());
    if (!signed) return null;
    const plain = nacl.sign.open(signed, bytes(RC_PUBLIC));
    if (!plain) return null;
    const cfg = JSON.parse(new TextDecoder().decode(plain));
    return cfg && cfg.v === 1 ? cfg : null;
  } catch { return null; }
}
