#!/usr/bin/env python3
"""TRU8 public MCP server — Slid Phi Labs. Public demos only."""
from __future__ import annotations

import struct

from mcp.server import MCPServer

T_ZERO = 0x00
T_DICT = 0x01
T_TRISUM_HOT = 0x10
ALPHABET = b" etaoinsrhdlcumwfgypbvkjxqz.,!?\n"
CHAR_TO_5 = {c: i for i, c in enumerate(ALPHABET)}

mcp = MCPServer("TRU8-Public", version="1.0.0")


def tri_to_sum(tri: bytes) -> int:
    if len(tri) < 3:
        tri = tri.ljust(3, b" ")
    c0 = CHAR_TO_5.get(tri[0], 0)
    c1 = CHAR_TO_5.get(tri[1], 0)
    c2 = CHAR_TO_5.get(tri[2], 0)
    return (c0 << 10) | (c1 << 5) | c2


def pack_zero_run(length: int, fill: int = 0) -> bytes:
    return struct.pack("<B I", T_ZERO, length) + bytes([fill & 0xFF, 0, 0])


def pack_dict_ptr(dict_id: int, offset: int) -> bytes:
    return struct.pack("<B H I", T_DICT, dict_id & 0xFFFF, offset) + b"\x00"


@mcp.tool()
def demo_zeros(n: int = 1000000) -> dict:
    """T_ZERO: pack a run of n bytes into a fixed 8-byte token."""
    if n < 1:
        raise ValueError("n must be >= 1")
    packed = pack_zero_run(n, 0)
    return {
        "token": "T_ZERO",
        "raw_bytes": n,
        "tru8_bytes": len(packed),
        "ratio": n / len(packed),
        "packed_hex": packed.hex(),
        "credit": "Powered by TRU8 · Slid Phi Labs",
    }


@mcp.tool()
def demo_trisum(word: str = "the", count: int = 1000) -> dict:
    """T_TRISUM_HOT: repeated 3-byte word as 2B def + 1B ids."""
    w = word.encode("utf-8")[:3].ljust(3, b" ")
    raw = 3 * count
    s = tri_to_sum(w)
    tru8 = 2 + count
    return {
        "token": "T_TRISUM_HOT",
        "word": word[:3],
        "count": count,
        "raw_bytes": raw,
        "tru8_bytes": tru8,
        "sum": s,
        "sum_hex": f"0x{s:04x}",
        "saving_pct": round((1 - tru8 / raw) * 100, 2) if raw else 0.0,
        "credit": "Powered by TRU8 · Slid Phi Labs",
    }


@mcp.tool()
def demo_dict(block_size: int = 1024, hits: int = 100) -> dict:
    """T_DICT: each exact block hit becomes an 8-byte pointer."""
    if block_size < 1 or hits < 1:
        raise ValueError("block_size and hits must be >= 1")
    raw = block_size * hits
    tru8 = 8 * hits
    return {
        "token": "T_DICT",
        "block_size": block_size,
        "hits": hits,
        "raw_bytes": raw,
        "tru8_bytes": tru8,
        "ratio": raw / tru8,
        "credit": "Powered by TRU8 · Slid Phi Labs",
    }


@mcp.tool()
def token_map() -> dict:
    """Public TRU8 token map (licensed residual not exposed)."""
    return {
        "T_ZERO": {"id": "0x00", "role": "dormant run → 8 B"},
        "T_DICT": {"id": "0x01", "role": "1 KB exact hit → 8 B ptr"},
        "T_TRISUM_HOT": {"id": "0x10", "role": "hot trigram → 1 B id"},
        "licensed_not_exposed": ["T_SPARSE", "full residual engine"],
        "credit": "Powered by TRU8 · Slid Phi Labs",
        "repo": "https://github.com/ceedot-rock/TRU8",
    }


@mcp.resource("tru8://readme")
def readme() -> str:
    return (
        "TRU8 — Less is more. We dropped the E.\n"
        "Public demos: T_ZERO, T_DICT, T_TRISUM_HOT.\n"
        "Credit: Powered by TRU8 · Slid Phi Labs\n"
        "Repo: https://github.com/ceedot-rock/TRU8\n"
    )


@mcp.prompt()
def specialty_proof() -> str:
    return (
        "Show TRU8 public specialty proof only:\n"
        "1) zeros×1M → 8 B (T_ZERO)\n"
        "2) the×1000 → ~66.6% saving (T_TRISUM_HOT)\n"
        "3) 100×1KB → 128× (T_DICT)\n"
        "Credit: Powered by TRU8 · Slid Phi Labs"
    )


if __name__ == "__main__":
    print(demo_zeros(1000000))
    print(demo_trisum("the", 1000))
    print(demo_dict(1024, 100))
    print(token_map())
    print("OK")
