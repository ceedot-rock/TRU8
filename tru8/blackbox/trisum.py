"""T_TRISUM_HOT blackbox — hot trigram → 1 B id + 2 B packed def."""
from __future__ import annotations

MAGIC = b"TRU8T"
T_TRISUM_HOT = 0x10
ALPHABET = b" etaoinsrhdlcumwfgypbvkjxqz.,!?\n"
CHAR_TO_5 = {c: i for i, c in enumerate(ALPHABET)}

def tri_to_sum(tri: bytes) -> int:
    if len(tri) < 3:
        tri = tri.ljust(3, b" ")
    c0 = CHAR_TO_5.get(tri[0], 0)
    c1 = CHAR_TO_5.get(tri[1], 0)
    c2 = CHAR_TO_5.get(tri[2], 0)
    return (c0 << 10) | (c1 << 5) | c2

class TrisumBox:
    MAGIC = MAGIC

    def pack_hot(self, hot_id: int) -> bytes:
        return bytes([T_TRISUM_HOT, hot_id & 0xFF])

    def pack_def(self, tri: bytes) -> bytes:
        s = tri_to_sum(tri)
        return s.to_bytes(2, "little")

    def unpack_hot(self, blob: bytes) -> int:
        if len(blob) < 2 or blob[0] != T_TRISUM_HOT:
            raise ValueError("not a T_TRISUM_HOT id")
        return blob[1]
