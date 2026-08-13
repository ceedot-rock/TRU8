"""T_ZERO blackbox — dormant runs → 8 B. No engine internals exposed."""
from __future__ import annotations
import struct

MAGIC = b"TRU8Z"
T_ZERO = 0x00

class ZeroBox:
    MAGIC = MAGIC

    def pack_run(self, length: int, byte: int = 0) -> bytes:
        if length < 1:
            raise ValueError("length >= 1")
        return struct.pack("<B I", T_ZERO, length) + bytes([byte & 0xFF, 0, 0])

    def unpack_run(self, blob: bytes) -> tuple[int, int]:
        if len(blob) < 8 or blob[0] != T_ZERO:
            raise ValueError("not a T_ZERO run")
        _tok, length = struct.unpack_from("<B I", blob, 0)
        fill = blob[5]
        return length, fill

    def expand(self, blob: bytes) -> bytes:
        n, fill = self.unpack_run(blob)
        return bytes([fill]) * n
