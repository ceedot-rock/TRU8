"""
TRU8 public demo core — Slid Phi Labs
Token paths only. Production residual is licensed separately.
"""
from __future__ import annotations
import struct
from typing import Tuple

# Token map
T_ZERO       = 0x00  # dormant run → 8 B
T_DICT       = 0x01  # 1 KB exact hit → 8 B ptr
T_SPARSE     = 0x03  # 128² sparse (public stub)
T_TRISUM_HOT = 0x10  # hot trigram → 1 B id

# 32-symbol alphabet for TriSum (5-bit)
ALPHABET = b" etaoinsrhdlcumwfgypbvkjxqz.,!?\n"
CHAR_TO_5 = {c: i for i, c in enumerate(ALPHABET)}
BIT5_TO_CHAR = {i: c for i, c in enumerate(ALPHABET)}

def tri_to_sum(tri: bytes) -> int:
    """3B tri → 15-bit sum (fits in 2B)."""
    if len(tri) < 3:
        tri = tri.ljust(3, b" ")
    c0 = CHAR_TO_5.get(tri[0], 0)
    c1 = CHAR_TO_5.get(tri[1], 0)
    c2 = CHAR_TO_5.get(tri[2], 0)
    return (c0 << 10) | (c1 << 5) | c2

def sum_to_tri(s: int) -> bytes:
    c0 = (s >> 10) & 31
    c1 = (s >> 5) & 31
    c2 = s & 31
    return bytes([BIT5_TO_CHAR[c0], BIT5_TO_CHAR[c1], BIT5_TO_CHAR[c2]])

def pack_zero_run(length: int) -> bytes:
    """T_ZERO + u32 length + pad → 8 B total."""
    return struct.pack("<B I", T_ZERO, length) + b"\x00\x00\x00"

def pack_dict_ptr(dict_id: int, offset: int) -> bytes:
    """T_DICT + dict_id u16 + offset u32 + pad → 8 B."""
    return struct.pack("<B H I", T_DICT, dict_id & 0xFFFF, offset) + b"\x00"

def pack_trisum_hot(hot_id: int) -> bytes:
    """T_TRISUM_HOT + 1B id."""
    return bytes([T_TRISUM_HOT, hot_id & 0xFF])

def demo_zeros(n: int = 1_000_000) -> dict:
    raw = n
    packed = pack_zero_run(n)
    return {
        "name": "zeros",
        "raw_bytes": raw,
        "tru8_bytes": len(packed),
        "ratio": raw / len(packed),
        "token": "T_ZERO",
        "packed_hex": packed.hex(),
    }

def demo_trigram(word: bytes = b"the", count: int = 1000) -> dict:
    raw = len(word) * count
    s = tri_to_sum(word)
    tru8 = 2 + count  # 2B def once + count * 1B ids
    return {
        "name": "trisum_hot",
        "raw_bytes": raw,
        "tru8_bytes": tru8,
        "sum": s,
        "sum_hex": f"0x{s:04x}",
        "ratio_saving_pct": (1 - tru8 / raw) * 100,
        "token": "T_TRISUM_HOT",
    }

def demo_dict_block(block_size: int = 1024, hits: int = 100) -> dict:
    raw = block_size * hits
    packed_one = pack_dict_ptr(0, 0)
    tru8 = len(packed_one) * hits
    return {
        "name": "dict_1kb",
        "raw_bytes": raw,
        "tru8_bytes": tru8,
        "ratio": raw / tru8,
        "token": "T_DICT",
    }
