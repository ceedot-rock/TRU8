"""
TRU8 Chamber Smart Shell v3 (public demo path)
Combines: TRU8 public surface + φ-split chamber lock.

Flow:
  raw → compress (zlib stand-in for licensed residual)
    → φ-split → lock (xor) → k_words + r_words + nonce + tag
  unlock: both streams + password → HMAC check → restore → raw

AEAD mindset: encrypt-then-split, HMAC verified before open.
Production residual / full _call_core remains licensed.
"""
from __future__ import annotations
import hashlib
import hmac
import os
import zlib
from typing import List, Tuple

PHI = 0.6180339887498948
INV_PHI = 1.0 - PHI

WORDLIST = [
    "chamber", "lock", "vault", "sigil", "ward", "veil", "spire", "gate",
    "oath", "cloak", "shard", "mark", "seal", "key", "writ", "aegis",
    "bind", "rune", "echo", "hush",
]


class BitStream:
    @staticmethod
    def undress(data: bytes) -> List[int]:
        bits: List[int] = []
        for b in data:
            for i in range(7, -1, -1):
                bits.append((b >> i) & 1)
        return bits

    @staticmethod
    def dress(bits: List[int]) -> bytes:
        out = bytearray()
        for i in range(0, len(bits), 8):
            byte = 0
            chunk = bits[i : i + 8]
            for j, bit in enumerate(chunk):
                byte |= (bit & 1) << (7 - j)
            out.append(byte)
        return bytes(out)


def _phi_split_bytes(data: bytes) -> Tuple[bytes, bytes]:
    if not data:
        return b"", b""
    cut = max(1, int(len(data) * PHI))
    return data[:cut], data[cut:]


def _xor_stream(data: bytes, key: bytes) -> bytes:
    return bytes(d ^ key[i % len(key)] for i, d in enumerate(data))


def _words_from(seed: bytes, n: int = 8) -> List[str]:
    h = hashlib.sha256(seed).digest()
    return [WORDLIST[h[i] % len(WORDLIST)] for i in range(n)]


class ChamberShell:
    """Public chamber shell. zlib stand-in for licensed TRU8 residual."""

    MAGIC = b"TRU8CHMB"

    def pack(self, raw: bytes, password: bytes = b"tru8") -> dict:
        compressed = zlib.compress(raw, 9)
        nonce = os.urandom(16)
        key = hashlib.sha256(password + nonce).digest()

        k_raw, r_raw = _phi_split_bytes(compressed)
        k_locked = _xor_stream(k_raw, key)
        r_locked = _xor_stream(r_raw, key[::-1])

        tag = hmac.new(key, k_locked + r_locked + nonce, hashlib.sha256).digest()[:16]
        return {
            "magic": self.MAGIC.decode(),
            "nonce": nonce.hex(),
            "tag": tag.hex(),
            "k_words": _words_from(k_locked + nonce),
            "r_words": _words_from(r_locked + tag),
            "k_blob": k_locked.hex(),
            "r_blob": r_locked.hex(),
            "raw_len": len(raw),
            "compressed_len": len(compressed),
            "k_len": len(k_locked),
            "r_len": len(r_locked),
        }

    def unpack(self, chamber: dict, password: bytes = b"tru8") -> bytes:
        nonce = bytes.fromhex(chamber["nonce"])
        tag = bytes.fromhex(chamber["tag"])
        k_locked = bytes.fromhex(chamber["k_blob"])
        r_locked = bytes.fromhex(chamber["r_blob"])
        key = hashlib.sha256(password + nonce).digest()

        expect = hmac.new(key, k_locked + r_locked + nonce, hashlib.sha256).digest()[:16]
        if not hmac.compare_digest(expect, tag):
            raise ValueError("HMAC tag mismatch — chamber sealed or wrong key")

        k_raw = _xor_stream(k_locked, key)
        r_raw = _xor_stream(r_locked, key[::-1])
        return zlib.decompress(k_raw + r_raw)


def demo() -> None:
    shell = ChamberShell()
    raw = b"TRU8 chamber demo - less is more. " * 50
    ch = shell.pack(raw)
    print("TRU8 Chamber Smart Shell (public path)")
    print(f"  raw:      {ch['raw_len']} B")
    print(f"  packed:   {ch['compressed_len']} B (stand-in)")
    print(f"  k_words:  {' '.join(ch['k_words'][:4])} ...")
    print(f"  r_words:  {' '.join(ch['r_words'][:4])} ...")
    print(f"  nonce:    {ch['nonce'][:16]}...")
    restored = shell.unpack(ch)
    print(f"  restore:  {restored == raw}")


if __name__ == "__main__":
    demo()
