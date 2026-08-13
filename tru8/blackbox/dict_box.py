"""T_DICT blackbox — 1 KB exact hit → 8 B pointer."""
from __future__ import annotations
import struct

MAGIC = b"TRU8D"
T_DICT = 0x01

class DictBox:
    MAGIC = MAGIC

    def pack_ptr(self, dict_id: int, offset: int) -> bytes:
        return struct.pack("<B H I", T_DICT, dict_id & 0xFFFF, offset) + b"\x00"

    def unpack_ptr(self, blob: bytes) -> tuple[int, int]:
        if len(blob) < 8 or blob[0] != T_DICT:
            raise ValueError("not a T_DICT ptr")
        _t, did, off = struct.unpack_from("<B H I", blob, 0)
        return did, off
